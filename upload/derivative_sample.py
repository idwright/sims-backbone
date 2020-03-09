import sys
from copy import deepcopy

import logging

import openapi_client
from openapi_client.rest import ApiException

from base_entity import BaseEntity


class DerivativeSampleProcessor(BaseEntity):

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)
        self._dao = dao
        self._event_set = event_set
        self._derivative_sample_cache = {}
        self._studies_cache = {}

    def create_derivative_sample_from_values(self, values, original_sample):

        if not original_sample:
            return None

        d_sample = openapi_client.DerivativeSample(None,
                                                   original_sample_id=original_sample.original_sample_id)

        idents = []
        if 'derivative_sample_id' in values:
            idents.append(openapi_client.Attr('derivative_sample_id', values['derivative_sample_id'],
                                              self._event_set))

        if 'derivative_sample_source' in values:
            idents.append(openapi_client.Attr('derivative_sample_source',
                                              values['derivative_sample_source'],
                                              self._event_set))

        if 'sanger_sample_id' in values:
            idents.append(openapi_client.Attr('sanger_sample_id',
                                              values['sanger_sample_id'],
                                              self._event_set))

        if 'sequencescape_id' in values:
            idents.append(openapi_client.Attr('sequencescape_id',
                                              values['sequencescape_id'],
                                              self._event_set))

        if 'sample_lims_id' in values and values['sample_lims_id']:
            idents.append(openapi_client.Attr('sanger_lims_id', values['sample_lims_id'],
                                              self._event_set))

        if 'plate_position' in values and values['plate_position']:
            idents.append(openapi_client.Attr('plate_position',
                                              values['plate_position'],
                                              self._event_set))

        if 'plate_name' in values and values['plate_name']:
            idents.append(openapi_client.Attr('plate_name', values['plate_name'],
                                              self._event_set))

        if 'dna_prep' in values:
            d_sample.dna_prep = values['dna_prep']

        if 'parent_unique_ds_id' in values:
            pds = openapi_client.DerivativeSample(None)
            parent = self.lookup_derivative_sample(pds, {
                'unique_ds_id': values['parent_unique_ds_id']
            })
            if parent:
                d_sample.parent_derivative_sample_id = parent.derivative_sample_id
                d_sample.original_sample_id = parent.original_sample_id
            else:
                self.report(f"Failed to find parent {values['unique_ds_id']} {values['parent_unique_ds_id']}", values)

        d_sample.attrs = idents

        return d_sample

    def load_attr_cache(self, study_id, values):

        if study_id and study_id not in self._studies_cache:
            cache = {
                'sample_lims_id': {},
                'sanger_sample_id': {}
            }
            try:
                found_events = self._dao.download_derivative_samples_by_study(study_id)
                for found in found_events.derivative_samples:
                    for attr in found.attrs:
                        if attr.attr_type in cache:
                            cache[attr.attr_type][attr.attr_value] = found
                self._studies_cache[study_id] = cache
            except ApiException as err:
                #self._logger.debug("Error looking for {}".format(ident))
                #print("Not found")
                    pass

    def attr_cache_lookup(self, study_id, existing, values, ident):

        cache = None

        if study_id and study_id in self._studies_cache:
            cache = self._studies_cache[study_id]
        if cache and ident.attr_type in cache:
            if ident.attr_value in cache[ident.attr_type]:
                found = cache[ident.attr_type][ident.attr_value]
                if existing and existing.derivative_sample_id != found.derivative_sample_id:
                    msg = ("Merging into {} using {}".format(existing.derivative_sample_id, ident.attr_type), values)
                    #print(msg)
                    found = self.merge_derivative_samples(existing, found, values)
                existing = found
                        #print ("found: {} {}".format(samp, found))
        return existing

    def lookup_derivative_sample(self, samp, values):

        existing = None

        if 'unique_ds_id' in values:
            # print(f"Looking in cache for unique_ds_id {values['unique_ds_id']}")
            if values['unique_ds_id'] in self._derivative_sample_cache:
                existing_sample_id = self._derivative_sample_cache[values['unique_ds_id']]
                existing = self._dao.download_derivative_sample(existing_sample_id)
                return existing

        study_id = None
        if 'study_id' in values:
            study_id = values['study_id']
            if study_id[:4] == '0000':
                study_id = None

        self.load_attr_cache(study_id, values)

        individual_lookup = False
        # print("not in cache: {} {}".format(samp, values))
        if samp.attrs:
            #print("Checking attrs {}".format(samp.attrs))
            for ident in samp.attrs:
                existing = self.attr_cache_lookup(study_id, existing, values, ident)

                cache_existing = existing
                # print(f'Existing {existing} from cache')
                if not existing:
                    individual_lookup = True

                if individual_lookup or not study_id:
                    try:
                        #print("Looking for {} {}".format(ident.attr_type, ident.attr_value))

                        if ident.attr_type == 'plate_name':
                            found_events = self._dao.download_derivative_samples_by_attr(ident.attr_type,
                                                                                         ident.attr_value)
                            for found in found_events.derivative_samples:
                                for samp_attr in samp.attrs:
                                    if samp_attr.attr_type == 'plate_position':
                                        for ds_attr in found.attrs:
                                            if ds_attr.attr_type == 'plate_position' and \
                                                ds_attr.attr_value == samp_attr.attr_value:
                                                existing = found
                            continue
                        if ident.attr_type == 'plate_position':
                            continue

                        if ident.attr_type == 'sequencescape_id':
                            # Not guaranteed to be unique
                            continue

                        found_events = self._dao.download_derivative_samples_by_attr(ident.attr_type,
                                                                                     ident.attr_value)

                        for found in found_events.derivative_samples:
                            if existing and existing.derivative_sample_id != found.derivative_sample_id:
                                msg = ("Merging into {} using {}"
                                       .format(existing.sampling_event_id,
                                               ident.attr_type), values)
                                #print(msg)
                                found = self.merge_derivative_samples(
                                    existing, found, values)
                            existing = found
                            #print ("found: {} {}".format(samp, found))
                    except ApiException as err:
                        #self._logger.debug("Error looking for {}".format(ident))
                        #print("Not found")
                        pass

        #if not existing:
        #    print('Not found {}'.format(samp))
        return existing

    def process_derivative_sample(self, samp, existing, original_sample, values):

        #print('process_derivative_sample {} {} {}'.format(values, samp, existing))

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if 'sanger_lims_id' in values and values['sanger_lims_id']:
            if not existing:
                self.report("Could not find not adding derivative sample", values)
                return None

        if existing:
            ret = self.merge_derivative_samples(existing, samp, values)
        else:
            #print("Creating {}".format(samp))
            if len(samp.attrs) == 0:
                return None

            try:
                if original_sample:
                    samp.original_sample_id = original_sample.original_sample_id
                created = self._dao.create_derivative_sample(samp, user)

                ret = created

            except ApiException as err:
                print("Error adding sample {} {}".format(samp, err))
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

        if 'unique_ds_id' in values:
            self._derivative_sample_cache[values['unique_ds_id']] = ret.derivative_sample_id

        return ret

    def merge_derivative_samples(self, existing, parsed, values):

        if not parsed:
            return existing

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if parsed.derivative_sample_id:
            #print('Merging via service {} {}'.format(existing, parsed))
            try:

                ret = self._dao.merge_derivative_samples(existing.derivative_sample_id,
                                                         parsed.derivative_sample_id,
                                                         user)

            except ApiException as err:
                msg = "Error updating merged derivative sample {} {} {} {}".format(
                    values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

            return ret

        existing, changed = self.merge_derivative_sample_objects(existing, parsed,
                                                                 values)
        ret = existing

        if changed:

            #print("Updating {} to {}".format(parsed, existing))
            try:
                existing = self._dao.update_derivative_sample(
                    existing.derivative_sample_id, existing, user)
            except ApiException as err:
                msg = "Error updating merged derivative sample {} {} {} {}".format(
                    values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

        else:
            #self.report("Merge os didn't change anything {} {}".format(existing, parsed), None)
            pass

        return existing

    def merge_derivative_sample_objects(self, existing, samp, values):

        orig = deepcopy(existing)
        changed = False

        change_reasons = []

        for new_ident in samp.attrs:
            found = False
            for existing_ident in existing.attrs:
                # Depending on the DAO used the attr can have a different type
                # so can't use ==
                if existing_ident.attr_source == new_ident.attr_source and \
                   existing_ident.attr_type == new_ident.attr_type and \
                   existing_ident.attr_value == new_ident.attr_value and \
                   existing_ident.study_name == new_ident.study_name:
                    found = True
            if not found:
                changed = True
                change_reasons.append("Adding ident {}".format(new_ident))
                existing.attrs.append(new_ident)

        if samp.original_sample_id != existing.original_sample_id:
            # print(existing)
            # print(samp)
            if existing.original_sample_id:
                se_existing = self._dao.download_original_sample(
                    existing.original_sample_id)
                if samp.original_sample_id:
                    se_samp = self._dao.download_original_sample(
                        samp.original_sample_id)
                    #se = self.merge_original_samples(se_samp, se_existing, values)
                    print('Need to merge original samples? {} {} {}'.format(se_samp, se_existing,
                                                                            values))
                    # print(se)
            else:
                existing.original_sample_id = samp.original_sample_id
            changed = True
            change_reasons.append('Set SamplingEvent')

        # print('\n'.join(change_reasons))

        return existing, changed

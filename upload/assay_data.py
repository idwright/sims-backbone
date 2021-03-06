import sys
import logging

import openapi_client
from openapi_client.rest import ApiException

from base_entity import BaseEntity

class AssayDataProcessor(BaseEntity):

    _assay_datum_cache = {}

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)

        self._lookup_attrs = ['assay_datum_id', 'irods_path']
        self.attrs = [
            {
                'from': 'assay_datum_id'
            },
            {
                'from': 'assay_datum_source'
            },
            {
                'from': 'irods_path'
            },
            {
                'from': 'tag_index'
            },
            {
                'from': 'manual_qc'
            },
            {
                'from': 'qc_complete'
            },
            {
                'from': 'id_run'
            },
            {
                'from': 'position'
            },
            {
                'from': 'legacy_library_id'
            },
            {
                'from': 'flowcell_barcode'
            },
            {
                'from': 'ebi_run_acc_alt'
            },
            {
                'from': 'reads'
            }
        ]

    def create_assay_datum_from_values(self, values, derivative_sample):

        if not derivative_sample:
            return None

        d_sample = openapi_client.AssayDatum(None,
                                             derivative_sample_id=derivative_sample.derivative_sample_id)

        d_sample.attrs = self.attrs_from_values(values)

        if 'ebi_run_acc' in values:
            d_sample.ebi_run_acc = values['ebi_run_acc']
        elif not d_sample.attrs:
            return None

        return d_sample

    def lookup_assay_datum(self, samp, values):

        if not samp:
            return None

        existing = None

        if 'unique_ad_id' in values:
            if values['unique_ad_id'] in self._assay_datum_cache:
                existing_sample_id = self._assay_datum_cache[values['unique_ad_id']]
                existing = self._dao.download_assay_datum(existing_sample_id)
                return existing


        #print ("not in cache: {}".format(samp))
        if len(samp.attrs) > 0:
            #print("Checking attrs {}".format(samp.attrs))
            for ident in samp.attrs:
                if ident.attr_type not in self._lookup_attrs:
                    continue
                try:
                    #print("Looking for {} {}".format(ident.attr_type, ident.attr_value))

                    found_events = self._dao.download_assay_data_by_attr(ident.attr_type,
                                                                              ident.attr_value)

                    for found in found_events.assay_data:
                        if existing and existing.assay_datum_id != found.assay_datum_id:
                            msg = ("Merging into {} using {}"
                                   .format(existing.sampling_event_id,
                                           ident.attr_type), values)
                            #print(msg)
                            found = self.merge_assay_data(existing, found, values)
                        existing = found
                        #print ("found: {} {}".format(samp, found))
                except ApiException as err:
                    #self._logger.debug("Error looking for {}".format(ident))
                    #print("Not found")
                        pass

        #if not existing:
        #    print('Not found {}'.format(samp))
        return existing

    def process_assay_datum(self, samp, existing, derivative_sample, values):

        if not samp:
            return None

        #
        #if 'reads' in values:
        #    if values['reads'] < 0:
        #        return None

# There are 4 samples in mlwh where irods_path is not unique
# These are:
        if 'irods_path' in values and\
           values['irods_path'] in ['5970_1_nonhuman.bam', '5970_2_nonhuman.bam', '5970_3_nonhuman.bam', '5970_5_nonhuman.bam']:
            if values['reads'] < 0:
                return None

        # print('process_assay data {} {} {} {}'.format(samp, existing, derivative_sample, values))

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if existing:
            ret = self.merge_assay_data(existing, samp, values)
        else:
            # print("Creating {}".format(samp))

            try:
                created = self._dao.create_assay_datum(samp, user)

                ret = created

            except ApiException as err:
                print("Error adding sample {} {}".format(samp, err))
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

            if 'unique_ad_id' in values:
                self._assay_datum_cache[values['unique_ad_id']] = created.assay_datum_id

        return ret

    def merge_assay_data(self, existing, parsed, values):

        if not parsed:
            return existing

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if parsed.assay_datum_id:
            #print('Merging via service {} {}'.format(existing, parsed))
            try:

                ret = self._dao.merge_assay_data(existing.assay_datum_id,
                                                 parsed.assay_datum_id,
                                                 user)

            except ApiException as err:
                msg = "Error updating merged assay data {} {} {} {}".format(values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

            return ret

        existing, changed = self.merge_assay_datum_objects(existing, parsed, values)
        ret = existing

        if changed:

            #print("Updating {} to {}".format(parsed, existing))
            try:
                existing = self._dao.update_assay_datum(existing.assay_datum_id, existing, user)
            except ApiException as err:
                msg = "Error updating merged assay data {} {} {} {}".format(values, parsed, existing, err)
                print(msg)
                self._logger.error(msg)
                sys.exit(1)

        else:
            #self.report("Merge os didn't change anything {} {}".format(existing, parsed), None)
            pass

        return existing

    def merge_assay_datum_objects(self, existing, samp, values):

        changed = False

        change_reasons = []

        changed = self.merge_attrs(samp, existing, change_reasons)

        if samp.derivative_sample_id != existing.derivative_sample_id:
            #print(existing)
            #print(samp)
            if existing.derivative_sample_id:
                se_existing = self._dao.download_derivative_sample(existing.derivative_sample_id)
                if samp.derivative_sample_id:
                    se_samp = self._dao.download_derivative_sample(samp.derivative_sample_id)
                    #se = self.merge_derivative_samples(se_samp, se_existing, values)
                    print('Need to merge derivative samples? {} {} {}'.format(se_samp, se_existing,
                                                                         values))
                    #print(se)
            else:
                existing.derivative_sample_id = samp.derivative_sample_id
            changed = True
            change_reasons.append('Set derivative sample')

        #print('\n'.join(change_reasons))

        return existing, changed

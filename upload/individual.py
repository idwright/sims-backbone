import sys
from copy import deepcopy

import logging

import openapi_client
from openapi_client.rest import ApiException

from base_entity import BaseEntity

class IndividualProcessor(BaseEntity):

    _individual_cache = {}

    def __init__(self, dao, event_set):
        super().__init__(dao, event_set)
        self._logger = logging.getLogger(__name__)
        self._lookup_attrs = [
            'patient_id',
            'donor_source_code'
        ]
        self.attrs = [
            {
                'from': 'patient_id',
                'use_study': True
            },
            {
                'from': 'donor_source_code',
                'use_study': True
            }
        ]



    def create_individual_from_values(self, values):
        study_id = None
        if 'study_id' in values:
            study_id = values['study_id']

        o_sample = openapi_client.Individual(None)

        o_sample.attrs = self.attrs_from_values(values, study_id)

        return o_sample

    def lookup_individual(self, samp, values):

        existing = None

        if 'unique_indiv_id' in values:
            if values['unique_indiv_id'] in self._individual_cache:
                existing_individual_id = self._individual_cache[values['unique_indiv_id']]
                existing = self._dao.download_individual(existing_individual_id)
                return existing

        study_id = None
        if 'study_id' in values:
            study_id = values['study_id']

        #print ("not in cache: {}".format(samp))
        if samp.attrs:
            #print("Checking attrs {}".format(samp.attrs))
            for ident in samp.attrs:

                if ident.attr_type not in self._lookup_attrs:
                    continue
                try:
                    #print("Looking for {} {}".format(ident.attr_type, ident.attr_value))

                    found_events = self._dao.download_individuals(f'attr:{ident.attr_type}:{ident.attr_value}',
                                                                  study_name=study_id)

                    for found in found_events.individuals:

                        if existing and existing.individual_id != found.individual_id:
                            msg = ("Merging into {} using {}".format(existing.individual_id,
                                                                     ident.attr_type), values)
                            #print(msg)
                            found = self.merge_individuals(existing, found, values)
                        existing = found
                        #print ("found: {} {}".format(samp, found))
                except ApiException as err:
                    #self._logger.debug("Error looking for {}".format(ident))
                    #print("Not found")
                    pass

        #if not existing:
        #    print('Not found {}'.format(samp))
        return existing

    def process_individual(self, values, samp, existing):

        ret = None

        #print('process individual {} {} {}'.format(values, samp, existing))

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if existing:

            ret = self.merge_individuals(existing, samp, values)

        else:
            #print("Creating {}".format(samp))
            if len(samp.attrs) == 0:
                return None

            try:
                created = self._dao.create_individual(samp, user)

                ret = created

            except ApiException as err:
                print("Error adding Individual {} {}".format(samp, err))
                self._logger.error("Error inserting {}".format(samp))
                sys.exit(1)

            if 'unique_os_id' in values:
                self._individual_cache[values['unique_os_id']] = created.individual_id

        return ret

    def merge_individuals(self, existing, parsed, values):

        if not parsed:
            return existing

        user = None
        if 'updated_by' in values:
            user = values['updated_by']

        if parsed.individual_id:
            #print('Merging via service {} {}'.format(existing, parsed))
            ret = existing
            try:

                ret = self._dao.merge_individuals(existing.individual_id,
                                                  parsed.individual_id, user)

            except ApiException as err:
                msg = "Error updating merged individual {} {} {} {}".format(values, parsed, existing, err)
                self._logger.error(msg)
                #sys.exit(1)

            return ret

        existing, changed = self.merge_individual_objects(existing, parsed,
                                                          values)
        ret = existing

        if changed:

            #print("Updating {} to {}".format(parsed, existing))
            try:
                existing = self._dao.update_individual(existing.individual_id,
                                                       existing, user)
            except ApiException as err:
                msg = "Error updating merged original sample {} {} {} {}".format(values, parsed, existing, err)
                self._logger.error(msg)
                sys.exit(1)

        else:
            #self.report("Merge os didn't change anything {} {}".format(existing, parsed), None)
            pass

        return existing

    def merge_individual_objects(self, existing, samp, values):

        # print('Merging individual {} {} {}'.format(existing, samp, values))
        new_ident_value = False

        change_reasons = []

        new_ident_value = self.merge_attrs(samp, existing, change_reasons)

        return existing, new_ident_value

import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date

import uuid

class TestStudies(TestBase):


    """
    """
    def test_download_studies(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)
        study_api = swagger_client.StudyApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10),
                                                doc_accuracy = 'month',
                                                partner_species = 'P. falciparum')
            created = api_instance.create_sampling_event(samp)

            studies = study_api.download_studies()

            found = False
            for study in studies.studies:
                if study.name == '0000-MD-UP' and study.code == '0000':
                    found = True

            self.assertTrue(found, 'Study does not exist')

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)



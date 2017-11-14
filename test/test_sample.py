import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase
from datetime import date

import uuid

class TestSample(TestBase):


    """
    """
    def test_create(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10))
            created = api_instance.create_sampling_event(samp)
            fetched = api_instance.download_sampling_event(created.sampling_event_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(samp, fetched, "upload != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_delete(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10))
            created = api_instance.create_sampling_event(samp)
            api_instance.delete_sampling_event(created.sampling_event_id)
            with self.assertRaises(Exception) as context:
                fetched = api_instance.download_sampling_event(created.sampling_event_id)
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_delete: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_delete_missing(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                api_instance.delete_sampling_event(str(uuid.uuid4()))
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_delete_missing: Exception when calling SamplingEventApi->delete_sampling_event: %s\n" % error)

    """
    """
    def test_duplicate_key(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10))
            samp.identifiers = [
                swagger_client.Identifier ('oxford', '1234')
            ]
            created = api_instance.create_sampling_event(samp)

            with self.assertRaises(Exception) as context:
                created = api_instance.create_sampling_event(samp)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_duplicate_partner_key(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10))
            samp.identifiers = [
                swagger_client.Identifier ('partner_id', '1234')
            ]
            created = api_instance.create_sampling_event(samp)

            created1 = api_instance.create_sampling_event(samp)


            api_instance.delete_sampling_event(created.sampling_event_id)
            api_instance.delete_sampling_event(created1.sampling_event_id)

            self.assertNotEqual(created.sampling_event_id, created1.sampling_event_id)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


    """
    """
    def test_identifier_lookup(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10))
            samp.identifiers = [
                swagger_client.Identifier ('oxford', '1234')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_event_by_identifier('oxford', '1234')

            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)

            self.assertEqual(created, fetched, "create response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(samp, fetched, "upload != download response")
            api_instance.delete_sampling_event(created.sampling_event_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_update(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10))
            samp.identifiers = [
                swagger_client.Identifier ('oxford', '1234')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_event_by_identifier('oxford', '1234')
            new_samp = swagger_client.SamplingEvent(None, '0001-MD-UP', date(2018, 11, 11))
            updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)
            fetched = api_instance.download_sampling_event(looked_up.sampling_event_id)
            self.assertEqual(updated, fetched, "update response != download response")
            fetched.sampling_event_id = None
            self.assertEqual(new_samp, fetched, "update != download response")
            api_instance.delete_sampling_event(looked_up.sampling_event_id)

        except ApiException as error:
            self.fail("test_update: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_update_duplicate(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            samp = swagger_client.SamplingEvent(None, '0000-MD-UP', date(2017, 10, 10))
            samp.identifiers = [
                swagger_client.Identifier ('oxford', '1234')
            ]
            created = api_instance.create_sampling_event(samp)
            looked_up = api_instance.download_sampling_event_by_identifier('oxford', '1234')
            new_samp = swagger_client.SamplingEvent(None, '0001-MD-UP', date(2018, 10, 10))
            new_samp.identifiers = [
                swagger_client.Identifier ('oxford', '12345')
            ]
            new_created = api_instance.create_sampling_event(new_samp)
            with self.assertRaises(Exception) as context:
                updated = api_instance.update_sampling_event(looked_up.sampling_event_id, new_samp)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_sampling_event(looked_up.sampling_event_id)
            api_instance.delete_sampling_event(new_created.sampling_event_id)

        except ApiException as error:
            self.fail("test_update_duplicate: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

    """
    """
    def test_update_missing(self):

        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            new_samp = swagger_client.SamplingEvent(None, '0001-MD-UP', date(2018, 11, 11))
            fake_id = uuid.uuid4()
            new_samp.sampling_event_id = str(fake_id)
            with self.assertRaises(Exception) as context:
                updated = api_instance.update_sampling_event(new_samp.sampling_event_id, new_samp)

            self.assertEqual(context.exception.status, 404)


        except ApiException as error:
            self.fail("test_update_missing: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)


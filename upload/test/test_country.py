from test_base import TestBase

import difflib
import urllib

import datetime
import json

from uploader import Uploader
from set_country import SetCountry
from upload_ssr import Upload_SSR

import swagger_client
from swagger_client.rest import ApiException

class TestCountry(TestBase):

    """
    """
    @classmethod
    def setUpClass(self):

        super(TestCountry, self).setUpClass()

        sd = Uploader(self._config_file)
        json_data = json.loads('''
{
    "values": {
        "unique_id": {
            "column": 2,
            "type": "string"
        },
        "sample_oxford_id": {
            "column": 3,
            "type": "string"
        },
        "sample_alternate_oxford_id": {
            "column": 4,
            "type": "string"
        },
        "sample_source_id": {
            "column": 6,
            "type": "string"
        },
        "sample_source_type": {
            "column": 8,
            "type": "string"
        },
        "species": {
            "column": 11,
            "type": "string"
        }
    }
}
        ''')
        sd.load_data_file(json_data, 'oxford_country.tsv')


        self.setUpSSR()

        sd = Uploader(self._config_file)
        json_data = json.loads('''{
    "values":
    {
        "sample_oxford_id": {
            "column": 0,
            "type": "string",
            "id": true
        },
        "study_id": {
            "column": 1,
            "type": "string"
        },
        "sample_partner_id": {
            "column": 2,
            "type": "string"
        },
        "location_name": {
            "column": 13,
            "type": "string"
        },
        "latitude": {
            "column": 14,
            "type": "float",
            "regex": "^\\\\s*([-0-9]*\\\\.?\\\\d{0,7})"
        },
        "longitude": {
            "column": 14,
            "type": "float",
            "regex": "([-0-9]*\\\\.?\\\\d{0,7})(\\\\d*)$"
        },
        "country": {
            "column": 5,
            "type": "string",
            "replace": [
                        [ "Madagascar", "MDG" ]
                    ]

        },
        "proxy_country": {
            "column": 5,
            "type": "string",
            "replace": [
                        [ "Madagascar", "MDG" ]
                    ]

        },
        "proxy_location_name": {
            "column": 6,
            "type": "string"
        },
        "proxy_latitude": {
            "column": 7,
            "type": "float",
            "regex": "^\\\\s*([-0-9]*\\\\.?\\\\d{0,7})"
        },
        "proxy_longitude": {
            "column": 7,
            "type": "float",
            "regex": "([-0-9]*\\\\.?\\\\d{0,7})\\\\d*$"
        },
        "doc": {
            "column": 8,
            "type": "datetime",
            "date_format": "%Y-%m-%d"
        }

    }
}''')

        sd.load_data_file(json_data, 'countries.tsv')

        sd = SetCountry(self._config_file)
        sd.use_message_buffer = True
        sd._countries_file = '../' + sd._countries_file

        id_type = 'oxford_id'
        input_file = 'oxford_country.tsv'
        id_column = 3
        country_column = 10
        ssr = 'TestSSR.xls'
        sd.load_location_cache()
        sd.set_countries(input_file, id_type, id_column, country_column)

        sheets = None
        sd.load_data_file(ssr, sheets)

        self._messages = sd.message_buffer
        #print('\n'.join(self._messages))
    """
    """
    @classmethod
    def tearDownClass(self):

        self.deleteStudies(['9052', '0000', '9060'])
        self.deleteEventSets(['countries', 'oxford_country'])

        self.tearDownSSR()
        self.tearDownLocations()


    """
    """
    def test_country_specific(self):
        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_events_by_identifier('partner_id',
                                                                           urllib.parse.quote_plus('MDG/TST_0001'))

            looked_up = looked_up.sampling_events[0]

            #print(looked_up)
            self.assertEqual(looked_up.proxy_location.country, 'MDG')
            self.assertEqual(looked_up.proxy_location.latitude, -19.0)
            self.assertEqual(looked_up.proxy_location.longitude, 47.0)
            self.assertEqual(looked_up.proxy_location.identifiers[0].identifier_value, 'Madagascar')
            self.assertEqual(looked_up.location.country, 'MDG')
            self.assertEqual(looked_up.location.latitude, -16.94223)
            self.assertEqual(looked_up.location.longitude, 46.83144)
            self.assertEqual(looked_up.location.identifiers[0].identifier_value, 'Maevatanana')
            self.assertEqual(looked_up.study_name[:4], '9050')

            if looked_up.location_id not in self._locations:
                self._locations.append(looked_up.location_id)
            if looked_up.proxy_location_id not in self._locations:
                self._locations.append(looked_up.proxy_location_id)

        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_events_by_identifier {}"
                        .format(error))

    """
    """
    def test_country_from_oxford(self):
        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_events_by_identifier('oxford_id',
                                                                           urllib.parse.quote_plus('CT0003-C'))

            looked_up = looked_up.sampling_events[0]
#            print(looked_up)
            self.assertEqual(looked_up.location.country, 'MDG')
            self.assertEqual(looked_up.location.latitude, -18.766947)
            self.assertEqual(looked_up.location.longitude, 46.869107)
            self.assertEqual(looked_up.study_name[:4], '0000')
            if looked_up.location_id not in self._locations:
                self._locations.append(looked_up.location_id)
        except ApiException as error:
            self.fail("test_location_duplicate_name: Exception when calling download_sampling_events_by_identifier {}"
                        .format(error))

    """
    """
    def test_country_from_ssr(self):
        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:
            looked_up = api_instance.download_sampling_events_by_identifier('oxford_id',
                                                                           urllib.parse.quote_plus('CT0002-C'))

            looked_up = looked_up.sampling_events[0]
#            print(looked_up)
            self.assertEqual(looked_up.location.country, 'MDG')
            self.assertEqual(looked_up.location.latitude, -18.766947)
            self.assertEqual(looked_up.location.longitude, 46.869107)
            self.assertEqual(looked_up.study_name[:4], '9051')
            if looked_up.location_id not in self._locations:
                self._locations.append(looked_up.location_id)
        except ApiException as error:
            self.fail("test_country_from_ssr: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

    """
    """
    def test_country_mismatch(self):
        api_instance = swagger_client.SamplingEventApi(self._api_client)

        try:

            looked_up = api_instance.download_sampling_events_by_identifier('partner_id',
                                                                           urllib.parse.quote_plus('MDG/TST_0004'))

            looked_up = looked_up.sampling_events[0]
            self.assertEqual(looked_up.proxy_location.country, 'MDG')
            self.assertEqual(looked_up.proxy_location.latitude, -19.0)
            self.assertEqual(looked_up.proxy_location.longitude, 47.0)
            self.assertEqual(looked_up.proxy_location.identifiers[0].identifier_value, 'Madagascar')

            msg = "Country conflict not updated IN vs MDG in {'identifier_source': 'oxford_country', 'identifier_type': 'alt_oxford_id', 'identifier_value': '905094', 'study_name': None}\t{'identifier_source': 'countries', 'identifier_type': 'oxford_id', 'identifier_value': 'CT0004-C', 'study_name': None}\t{'identifier_source': 'oxford_country', 'identifier_type': 'oxford_id', 'identifier_value': 'CT0004-C', 'study_name': None}\t{'identifier_source': 'countries', 'identifier_type': 'partner_id', 'identifier_value': 'MDG/TST_0004', 'study_name': None}\t{'identifier_source': 'oxford_country', 'identifier_type': 'partner_id', 'identifier_value': 'MDG/TST_0004', 'study_name': None} for oxford_country.tsv"

            self.assertIn(msg, self._messages)

            msg = "Country conflict not updated in proxy IN vs MDG in {'identifier_source': 'oxford_country', 'identifier_type': 'alt_oxford_id', 'identifier_value': '905094', 'study_name': None}\t{'identifier_source': 'countries', 'identifier_type': 'oxford_id', 'identifier_value': 'CT0004-C', 'study_name': None}\t{'identifier_source': 'oxford_country', 'identifier_type': 'oxford_id', 'identifier_value': 'CT0004-C', 'study_name': None}\t{'identifier_source': 'countries', 'identifier_type': 'partner_id', 'identifier_value': 'MDG/TST_0004', 'study_name': None}\t{'identifier_source': 'oxford_country', 'identifier_type': 'partner_id', 'identifier_value': 'MDG/TST_0004', 'study_name': None} for oxford_country.tsv"
            
            self.assertIn(msg, self._messages)
            self.assertEqual(looked_up.location.country, 'MDG')
            self.assertEqual(looked_up.location.latitude, -16.94223)
            self.assertEqual(looked_up.location.longitude, 46.83144)
            self.assertEqual(looked_up.location.identifiers[0].identifier_value, 'Maevatanana')
            self.assertEqual(looked_up.study_name[:4], '9052')
            if looked_up.location_id not in self._locations:
                self._locations.append(looked_up.location_id)
        except ApiException as error:
            self.fail("test_country_mismatch: Exception when calling download_sampling_event_by_identifier {}"
                        .format(error))

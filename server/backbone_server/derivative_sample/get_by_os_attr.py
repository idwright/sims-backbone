from openapi_server.models.derivative_sample import DerivativeSample
from openapi_server.models.derivative_samples import DerivativeSamples

from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.derivative_sample.fetch import DerivativeSampleFetch

import logging

class DerivativeSampleGetByOsAttr():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def get(self, attr_type, attr_value):

        with self._connection:
            with self._connection.cursor() as cursor:

                locations = {}

                stmt = '''SELECT DISTINCT ds.id FROM derivative_samples ds
                JOIN original_sample_attrs osa ON osa.original_sample_id=ds.original_sample_id
                JOIN attrs ON attrs.id = osa.attr_id
                WHERE attr_type = %s AND attr_value = %s'''
                args = (attr_type, attr_value)

                cursor.execute(stmt, args)

                derivative_samples = DerivativeSamples(derivative_samples=[], count=0)
                event_ids = []

                for derivative_sample_id in cursor:
                    event_ids.append(derivative_sample_id)

                for derivative_sample_id in event_ids:
                    derivative_sample = DerivativeSampleFetch.fetch(cursor, derivative_sample_id, locations)
                    derivative_samples.derivative_samples.append(derivative_sample)
                    derivative_samples.count = derivative_samples.count + 1


                derivative_samples.attr_types = []

                stmt = '''SELECT DISTINCT da.attr_type FROM derivative_samples ds
                JOIN original_sample_attrs osa ON osa.original_sample_id=ds.original_sample_id
                JOIN attrs oa ON oa.id = osa.attr_id
                JOIN derivative_sample_attrs dsa ON dsa.derivative_sample_id = ds.id
                JOIN attrs da ON da.id = dsa.attr_id
                WHERE oa.attr_type = %s AND oa.attr_value = %s'''
                args = (attr_type, attr_value)

                cursor.execute(stmt, args)

                for (attr,) in cursor:
                    derivative_samples.attr_types.append(attr)

#Allow for when partner ident is used in different studies
#        if derivative_samples.count > 1:
#            raise MissingKeyException("Too many derivative_samples not found {} {}".format(attr_type,
#                                                                      attr_value))

        return derivative_samples

from openapi_server.models.log_items import LogItems
from openapi_server.models.log_item import LogItem
from backbone_server.errors.missing_key_exception import MissingKeyException
from openapi_server.models.sampling_event import SamplingEvent  # noqa: E501
from openapi_server.models.sampling_events import SamplingEvents  # noqa: E501
from openapi_server import util

import logging

from openapi_server.encoder import JSONEncoder
import json

class History():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn


    def get(self, record_type, record_id, record_types):

        resp = LogItems()
        resp.log_items = []

        with self._connection:
            with self._connection.cursor() as cursor:

                stmt = f'''select action_id, input_value, output_value, action_date, result_code
                from archive where action_id like '%%{record_type}%%' and output_value ->> '{record_type}_id' = %s'''

                cursor.execute(stmt, (record_id,))

                for (action_id, input_value, output_value, action_date,
                     result_code) in cursor:
                    if record_types and record_types != 'all':
                        if not ('create' in action_id or 'update' in action_id):
                                continue
                    log_item = LogItem()
                    log_item.action = action_id
                    log_item.input_value = str(input_value)
                    log_item.output_value = json.dumps(output_value,
                                                       cls=JSONEncoder)
#                    if record_type == 'sampling_event':
#                        log_item.output_value = SamplingEvent.from_dict(output_value)
                    log_item.action_date = action_date
                    log_item.result = result_code
                    resp.log_items.append(log_item)

                if not resp.log_items:
                    raise MissingKeyException("No history {} {}".format(record_type, record_id))


        return resp
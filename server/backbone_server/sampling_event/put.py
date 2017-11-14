from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException

from backbone_server.sampling_event.edit import SamplingEventEdit

from swagger_server.models.sampling_event import SamplingEvent

import mysql.connector
from mysql.connector import errorcode
import psycopg2

import logging

class SamplingEventPut():

    def __init__(self, conn):
        self._logger = logging.getLogger(__name__)
        self._connection = conn

    def __del__(self):
        if self._connection:
            self._connection.close()


    def put(self, sample_id, sample):

        cursor = self._connection.cursor()

        stmt = '''SELECT id FROM samples WHERE  id = %s'''
        cursor.execute( stmt, (sample_id,))

        existing_sample = None

        for (sample_id, ) in cursor:
            existing_sample = SamplingEvent(sample_id)

        if not existing_sample:
            cursor.close()
            raise MissingKeyException("Could not find sample to update {}".format(sample_id))

        study_id = SamplingEventEdit.fetch_study_id(cursor, sample)
        partner_species = SamplingEventEdit.fetch_partner_species(cursor, sample, study_id)
        stmt = '''UPDATE samples 
                    SET study_id = %s, doc = %s, doc_accuracy = %s,
                    location_id = %s, proxy_location_id = %s, partner_species_id = %s
                    WHERE id = %s'''
        args = (study_id, sample.doc, sample.doc_accuracy, sample.location_id, sample.proxy_location_id, partner_species, sample_id)

        try:
            cursor.execute(stmt, args)
            rc = cursor.rowcount

            cursor.execute('DELETE FROM identifiers WHERE sample_id = %s', (sample_id,))

            SamplingEventEdit.add_identifiers(cursor, sample_id, sample)

        except mysql.connector.Error as err:
            cursor.close()
            if err.errno == errorcode.ER_DUP_ENTRY:
                raise DuplicateKeyException("Error updating sample {}".format(sample)) from err
            else:
                self._logger.fatal(repr(error))
        except psycopg2.IntegrityError as err:
            cursor.close()
            raise DuplicateKeyException("Error updating sample {}".format(sample)) from err
        except DuplicateKeyException as err:
            cursor.close()
            raise err

        self._connection.commit()

        cursor.close()

        if rc != 1:
            raise MissingKeyException("Error updating sample {}".format(sample_id))

        sample.sampling_event_id = sample_id

        return sample

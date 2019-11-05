from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.nested_edit_exception import NestedEditException

from backbone_server.location.fetch import LocationFetch
import uuid

class OriginalSampleEdit():


    @staticmethod
    def fetch_study_id(cursor, study_name, create):
        study_id = None

        if not study_name:
            return study_id

        cursor.execute('''SELECT id FROM studies WHERE study_code = %s''', (study_name[:4],))
        result = cursor.fetchone()

        if result:
            study_id = result[0]
        else:
            if not create:
                return None
            study_id = uuid.uuid4()
            cursor.execute('''INSERT INTO studies (id, study_code, study_name) VALUES (%s, %s,
                           %s)''', (study_id, study_name[:4], study_name))
        return study_id

    @staticmethod
    def fetch_partner_species(cursor, original_sample, study_id):
        partner_species = None

        if not original_sample.partner_species:
            return partner_species

        cursor.execute('''SELECT id FROM partner_species_identifiers WHERE study_id = %s AND
                       partner_species = %s''',
                           (study_id, original_sample.partner_species))
        result = cursor.fetchone()

        if result:
            partner_species = result[0]
        else:
            partner_species = uuid.uuid4()
            cursor.execute('''INSERT INTO partner_species_identifiers (id, study_id,
                           partner_species) VALUES (%s, %s, %s)''',
                           (partner_species, study_id, original_sample.partner_species))
        return partner_species

    @staticmethod
    def add_attrs(cursor, uuid_val, original_sample):
        if original_sample.attrs:
            for ident in original_sample.attrs:
                if not (ident.attr_type == 'partner_id' or \
                        ident.attr_type == 'individual_id'):
                    cursor.execute('''SELECT * FROM attrs
                                   JOIN original_sample_attrs ON original_sample_attrs.attr_id =
                                   attrs.id
                                   WHERE attr_type = %s AND attr_value = %s AND
                                   attr_source = %s''',
                                   (ident.attr_type, ident.attr_value,
                                    ident.attr_source))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting original_sample attr {} {}"
                                                    .format(ident.attr_type, original_sample))

                    cursor.execute('''SELECT * FROM attrs
                                   JOIN original_sample_attrs ON original_sample_attrs.attr_id =
                                   attrs.id
                                   WHERE attr_type = %s AND attr_value = %s AND
                                   original_sample_id != %s''',
                                   (ident.attr_type, ident.attr_value,
                                    uuid_val))
                    if cursor.fetchone():
                        raise DuplicateKeyException("Error inserting original_sample attr {} {}"
                                                    .format(ident.attr_type, original_sample))

                attr_id = uuid.uuid4()
                stmt = '''INSERT INTO attrs
                    (id, attr_type, attr_value, attr_source)
                    VALUES (%s, %s, %s, %s)'''
                cursor.execute(stmt, (attr_id, ident.attr_type, ident.attr_value,
                                      ident.attr_source))

                stmt = '''INSERT INTO original_sample_attrs
                    (original_sample_id, attr_id)
                    VALUES (%s, %s)'''
                cursor.execute(stmt, (uuid_val, attr_id))

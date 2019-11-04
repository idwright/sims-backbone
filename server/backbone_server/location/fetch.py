from openapi_server.models.location import Location
from openapi_server.models.attr import Attr
from backbone_server.errors.missing_key_exception import MissingKeyException

import logging

class LocationFetch():


    @staticmethod
    def fetch(cursor, location_id):

        if not location_id:
            return None

        stmt = '''SELECT id, ST_X(location) as latitude, ST_Y(location) as longitude,
        accuracy, curated_name, curation_method, country, notes, proxy_location_id
                       FROM locations WHERE id = %s'''
        cursor.execute( stmt, (location_id,))

        location = None

        for (loc_id, latitude, longitude, accuracy, curated_name,
             curation_method, country, notes, proxy_location_id) in cursor:
            if proxy_location_id:
                proxy_location_id = str(proxy_location_id)
            location = Location(location_id=str(loc_id), latitude=latitude,
                                longitude=longitude,
                                accuracy=accuracy,
                                curated_name=curated_name,
                                curation_method=curation_method,
                                country=country,
                                notes=notes,
                                proxy_location_id=proxy_location_id)

        stmt = '''SELECT DISTINCT attr_type, attr_value, attr_source, studies.study_name
                FROM location_attrs
                JOIN attrs a ON a.id = location_attrs.attr_id
                LEFT JOIN studies ON a.study_id = studies.id
                WHERE location_id = %s'''

        cursor.execute(stmt, (location_id, ))

        if not location:
            raise MissingKeyException("No location {}".format(location_id))

        location.attrs = []
        for (name, value, source, study) in cursor:
            ident = Attr(attr_type=name,
                         attr_value=value,
                         attr_source=source,
                         study_name=study)
            location.attrs.append(ident)

        if not location.attrs:
            location.attrs = None

        return location

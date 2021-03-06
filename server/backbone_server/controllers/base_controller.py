import logging
import os
import json
from psycopg2.extras import Json

from openapi_server.encoder import JSONEncoder

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from backbone_server.model.history_meta import versioned_session
from backbone_server.model.archive import BaseArchive
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.model.logging import *

engine = None

class BaseController():

    _connection = None
    _logger = None
    _engine = None

    CREATE_PERMISSION = 'create'
    UPDATE_PERMISSION = 'update'
    GET_PERMISSION = 'get'
    DELETE_PERMISSION = 'delete'

    def __init__(self):
        if os.getenv('BB_DEBUG'):
            logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(__name__)
        self._connection = self._init_connection()

    def __del__(self):
        if self._connection:
            self._connection.close()

    def get_connection(self):
        return self._connection

    def get_engine(self):
        return self._engine

    def get_session(self):
        return self._session

    @staticmethod
    def get_connection_config():

        config = {
            'user': os.getenv('POSTGRES_USER', os.getenv('USER')),
            'database': os.getenv('POSTGRES_DB', 'backbone_service'),
            'password': os.getenv('POSTGRES_PASSWORD', None),
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', 5432),
        }

        return config

    @staticmethod
    def get_connection_url():

        config = BaseController.get_connection_config()
        url = 'postgresql+psycopg2://' + config['user']
        if config['password']:
            url += ':' + config['password']
        url += '@' + config['host']
        url += ':' + config['port']
        url += '/' + config['database']

        return url

    def _init_connection(self):
        _postgres = True

        if _postgres:
            config = BaseController.get_connection_config()
            import psycopg2
            from psycopg2.extras import register_uuid
            from psycopg2.extras import LoggingConnection

            psycopg2.extensions.register_type(register_uuid())
            psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
            psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
            conn = psycopg2.connect(
                connection_factory=LoggingConnection, **config)
            conn.initialize(self._logger)

            log = False
            if os.getenv('SA_DEBUG'):
                log = True

            url = BaseController.get_connection_url()

            global engine

            if not engine:
                engine = create_engine(url,
                                       convert_unicode=True,
                                       pool_pre_ping=True,
                                       echo=log)
            self._engine = engine
            self._session = scoped_session(sessionmaker(autocommit=False,
                                                        autoflush=False,
                                                        bind=self._engine))

            versioned_session(self._session)

            # create the archive table
            ba = BaseArchive(self._engine, self._session)
            # https://docs.sqlalchemy.org/en/13/orm/extensions/automap.html
    #        cur = conn.cursor()
    #        cur.execute("SET search_path TO " + 'backbone,public,contrib')
    #        cur.close()
        return conn

    """
    Convert the connexion token_info (OAuth) response into something that can be made consistent
    with AWS Custom Auth details
    """

    def token_info(self, tok_info):
        resp = []
        if tok_info and 'scope' in tok_info:
            #resp = tok_info['scope']
            if 'memberOf' in tok_info and tok_info['memberOf']:
                for auth_grp in tok_info['memberOf']:
                    resp.append(auth_grp)

        return resp

    """
    Convert AWS authorizer into consistent format
    """

    def authorizer(self, authorizer):
        resp = []
        resp = list(authorizer.keys())
        return resp

#     @staticmethod
#     def study_filter(studies):
#
#         study_filter = None
#
#         if studies is not None:
#             study_codes = [i['study'] for i in studies if i['bucket'] == 'pi' or i['bucket'] == 'data' or i['bucket'] == 'all']
#             if 'all' not in study_codes:
#                 codes = ",".join(f"'{w}'" for w in study_codes)
#                 study_filter = f' study_code in ({codes})'
#
#         return study_filter
#
#     @staticmethod
#     def has_study_permission(studies, study_code, perm_type):
#
#         found = False
#
#         if isinstance(study_code, list):
#             for sc in study_code:
#                 BaseController.has_study_permission(studies, sc, perm_type)
#             return True
#         if studies is not None:
#             for study in studies:
#                 if 'all' in study['study']:
#                     found = True
#                     break
#                 if study['study'].startswith(study_code[:4]):
#                     found = True
#                     break
#
#         if not found:
#             raise PermissionException(f'No permission for study {study_code}')
#
#         return found

    def dumps(self, item):

        return json.dumps(item, cls=JSONEncoder)

    def log_action(self, user, action, entity_id, content, result, retcode,
                   duration):

        stmt = '''INSERT INTO archive (submitter, action_id, entity_id, input_value, output_value, result_code, duration)
                                       VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        try:
            # content_json = None
            # if content:
            #    content_json = json.dumps(content.to_dict())
            result_json = None
            if result:
                from openapi_server.models.base_model_ import Model
                from openapi_server.models.document import Document
                if isinstance(result, Document):
                    for key, value in result.openapi_types.items():
                    #    print(key, value)
                    #    print(type(value))
                        if str(value) == 'file':
                            #delattr(result, key)
                    #        print('yyyyyyyyy')
                            result.openapi_types.pop('content')
                else:
                    result_json = Json(result, dumps=self.dumps)
            args = (user, action, entity_id, str(content),
                    result_json, retcode, duration)

            self._logger.debug("log_action {}".format(args))

            if os.getenv('LOG_ALL_ACTIONS') or action.startswith('merge') or \
               action.startswith('create') or action.startswith('update') or \
                    action.startswith('delete') or retcode != 200:
                with self._connection:
                    with self._connection.cursor() as cursor:
                        cursor.execute(stmt, args)
        except Exception as err:
            # Don't want to fail if it's just a logging problem
            args = (user, action, entity_id, content, result, retcode, duration)
            print("failed log_action {} {}".format(err, stmt % args))
            self._logger.exception('Failed to log action %s', err)

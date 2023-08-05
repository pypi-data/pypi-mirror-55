"""
FyleLoadConnector(): Connection between Fyle and Database
"""

import logging
from os import path
from typing import BinaryIO

import pandas as pd

logger = logging.getLogger('FyleConnector')


class FyleLoadConnector:
    """
    - Extract Data from Database and load to Fyle
    """
    def __init__(self, fyle_sdk_connection, dbconn):
        self.__dbconn = dbconn
        self.__connection = fyle_sdk_connection

        logger.info('Fyle connection established.')

    def create_tables(self):
        """
        Creates DB tables
        :return: None
        """
        basepath = path.dirname(__file__)
        ddl_path = path.join(basepath, 'load_ddl.sql')
        ddl_sql = open(ddl_path, 'r').read()
        self.__dbconn.executescript(ddl_sql)

    def __load_excel(self, file_path: str) -> str:
        """
        Upload Excel File to Fyle
        :param file_path: Absolute path for the excel file
        :return: returns file id
        """
        logger.info('Uploading excel to Fyle.')

        file_data = open(file_path, 'rb')

        file_path_tokenize = file_path.split('/')
        file_name = file_path_tokenize[len(file_path_tokenize) - 1]

        file_id = self.load_file(
            file_name,
            file_data,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        logger.info('Excel file uploaded successfully.')
        return file_id

    def load_tpa_exports(self, file_path: str = None, file_id: str = None) -> None:
        """
        Load TPA Export Batches in Fyle
        :param file_path: Path of the export file
        :param file_id: Id of file already uploaded to Fyle
        :return: None
        """
        logger.info('Pushing export batch to Fyle.')

        batches = pd.read_sql_query(sql='select * from fyle_load_tpa_export_batches', con=self.__dbconn)

        if not file_id:
            if file_path:
                file_id = self.__load_excel(file_path)
            batches['file_id'] = file_id

        batches['success'] = True

        batches = batches.to_dict(orient='records')

        logger.info('Uploading %s batches to Fyle', len(batches))

        for batch in batches:
            lineitems = pd.read_sql_query(
                sql="select * from fyle_load_tpa_export_batch_lineitems where batch_id = '{0}'".format(batch['id']),
                con=self.__dbconn
            )

            lineitems_payload = lineitems.to_dict(orient='records')

            if lineitems_payload:
                batch_id = self.__connection.Exports.post_batch(batch)['id']

                logger.info('Batch successfully upload. Uploading Line items.')

                self.__connection.Exports.post_batch_lineitems(batch_id, lineitems_payload)

                logger.info('%s Lineitems successfully uploaded.', len(lineitems_payload))
            else:
                logger.info('0 Lineitems. Skipping exports')

    def load_file(self, file_name: str, file_data: BinaryIO, content_type: str) -> str:
        """
        Upload File to Fyle
        :param file_name: Name of the file
        :param file_data: Data of the fyle in bytes
        :param content_type: content type
        :return:
        """
        file_obj = self.__connection.Files.post(file_name)
        upload_url = self.__connection.Files.create_upload_url(file_obj['id'])['url']
        self.__connection.Files.upload_file_to_aws(content_type, file_data, upload_url)
        return file_obj['id']

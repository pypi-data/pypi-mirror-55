"""
GoogleSheetsConnector(): Connection between Google Sheets and SQLite
"""

import json
import logging
from typing import List

import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials


logger = logging.getLogger('GoogleSheetsConnector')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


class GoogleSheetsConnector:
    """
    - Extract Data from Google Sheets and load to SQLite
    - Write Data to Google Sheets
    """
    def __init__(self, config, db_conn):
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(config.get('gsheets_credentials')), scope)
        self.__client = gspread.authorize(credentials)
        self.__sheet = self.__client.open(config.get('sheet_name'))
        self.__dbconn = db_conn
        logger.info('Google Sheets connection established.')

    def create_tables(self, file_path: str) -> None:
        """
        Creates DB tables
        :param file_path: absolute path to the .sql file
        :return: None
        """
        ddl_sql = open(file_path, 'r').read()
        self.__dbconn.executescript(ddl_sql)

    def update_cell(self, worksheet: str, cell: str, new_value: any) -> None:
        """
        Update a particular cell of google sheet
        :param worksheet: name of the worksheet
        :param cell: cell to be updated
        :param new_value: new value of the cell
        :return: None
        """
        self.__sheet.worksheet(worksheet).update_acell(cell, new_value)

    def clear_worksheet(self, worksheet: str) -> None:
        """
        Clear a worksheet completely
        :param worksheet: name of the worksheet
        :return: None
        """
        self.__sheet.worksheet(worksheet).clear()

    def extract_data(self) -> None:
        """
        Extracts data from Google sheets
        :return: None
        """
        worksheet_list = self.__sheet.worksheets()

        logger.info('Extracting mappings from Google sheet.')

        for worksheet in worksheet_list:
            logger.info('Extracting %s', worksheet.title)

            data = self.__sheet.worksheet(worksheet.title)
            df = pd.DataFrame(data.get_all_records())
            logger.info('%s %s extracted', len(df.index), worksheet.title)
            if len(df.index):
                df.to_sql(worksheet.title, self.__dbconn, if_exists='append', index=False)

        logger.info('Mappings were successfully extracted from google sheets.')

    def update_in_range(self, worksheet: str, start_cell: str, end_cell: str, cell_values: List[str]) -> None:
        """
        Update Range in batch
        :param worksheet: name of the worksheet
        :param start_cell: start cell
        :param end_cell: end cell
        :param cell_values: list of values to be updated
        :return: None
        """
        cell_list = self.__sheet.worksheet(worksheet).range(('%s:%s', start_cell, end_cell))

        for i, val in enumerate(cell_values):
            cell_list[i].value = val

        self.__sheet.worksheet(worksheet).update_cells(cell_list)

import unittest
from scripts.postprocessing_checks import database_check
import pandas as pd
from unittest.mock import patch


data_type_check_bad = pd.DataFrame([['SL010_FIPS'], ['SL040_FIPS'], ['SL050_FIPS']], columns=['cn'])
data_type_check_good = pd.DataFrame([], columns=['cn'])


class TestClass(unittest.TestCase):

    @unittest.mock('connect_to_db.pyodbc.connect')
    def test_connect_to_db(self, mockconnect):
        connection = database_check.connect_to_db.connection()
        self.assertIsNotNone(connection)
        mockconnect.assert_called()
    #
    # def db_dtypes_uniqueness(self):
    #
    #     self.assertLogs(database_check.db_dtypes_uniqueness(data_type_check_bad),
    #                     "['SL010_FIPS', 'SL040_FIPS', 'SL050_FIPS'] have no unique data type in sql database.")
    #     self.assertLogs(database_check.db_dtypes_uniqueness(data_type_check_good))



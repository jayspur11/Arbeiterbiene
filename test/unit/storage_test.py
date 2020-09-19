from shared.storage import DatabaseHandler

import os
import sqlite3
import unittest


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect('test.db')

    def tearDown(self):
        self.connection.close()
        os.remove('test.db')

    def test_handler_initialization(self):
        _ = DatabaseHandler('TestTable', ('Col1', 'Col2'), db_name='test.db')

        table_query = self.connection.execute('SELECT COUNT(1) AS count'
                                              ' FROM sqlite_master'
                                              ' WHERE type="table"'
                                              '   AND name="TestTable";')
        table_exists = bool(table_query.fetchone()[0])
        self.assertTrue(table_exists)


if __name__ == '__main__':
    unittest.main()

import asyncio
import sqlite3


class DatabaseHandler:
    def __init__(self, table_name, column_names, db_name='arbeiterbiene.db'):
        self._db_thread = asyncio.new_event_loop()
        self._db_thread.run_until_complete(self._connect_to_db(db_name))
        self._cursor = self._connection.cursor()

        self._table_name = table_name
        self._db_thread.run_until_complete(
            self._execute_statement(
                'CREATE TABLE IF NOT EXISTS {table} ({cols});'.format(
                    table=table_name, cols=', '.join(column_names))))

    async def _connect_to_db(self, db_name):
        self._connection = sqlite3.connect(db_name)

    async def _execute_statement(self, *args):
        return self._cursor.execute(*args)

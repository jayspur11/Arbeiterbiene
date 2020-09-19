import asyncio
import sqlite3


async def _connect_to_db():
    global _connection
    _connection = sqlite3.connect('arbeiterbiene.db')


# Create a dedicated thread for database use.
_db_thread = asyncio.new_event_loop()
_db_thread.run_until_complete(_connect_to_db())
_cursor = _connection.cursor()


class DatabaseHandler:
    def __init__(self, table_name, column_names):
        self._table_name = table_name
        _db_thread.run_until_complete(
            self._execute_statement('CREATE TABLE IF NOT EXISTS ' +
                                    table_name + ' (' +
                                    ', '.join(column_names) + ');'))

    async def _execute_statement(self, *args):
        _cursor.execute(*args)

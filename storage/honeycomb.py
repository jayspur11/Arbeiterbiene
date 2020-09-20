import asyncio
import sqlite3


async def _connect():
    """Async wrapper to connect to SQL DB on a dedicated thread."""
    return sqlite3.connect("hive.db")


class Honeycomb:
    """Base class to store data locally."""
    _db_thread = asyncio.new_event_loop()
    _db_connection = _db_thread.run_until_complete(_connect())

    async def __execute(self, query, *args):
        """Run the given query.

        This coroutine is defined so we can kick execution on to the dedicated
        thread; subclasses should use the synchronous `_run_query` instead.

        Args:
            query (string): SQL query to execute.

        Returns:
            list[sqlite3.Row]: Results of the query.
        """
        return self._db_connection.execute(query, *args).fetchall()

    def _run_query(self, query, *args):
        """Run the given query.

        This is a convenience wrapper; the actual execution happens on the
        dedicated thread.

        Args:
            query (string): SQL query to execute.

        Returns:
            list[sqlite3.Row]: Results of the query.
        """
        return self._db_thread.run_until_complete(self.__execute(query, *args))

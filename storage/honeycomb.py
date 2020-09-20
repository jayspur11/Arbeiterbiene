import asyncio
import sqlite3


async def _run_async(f, *args, **kwargs):
    """Async wrapper to let us run sync functions on a dedicated thread."""
    return f(*args, **kwargs)


class Honeycomb:
    """Base class to store data locally."""
    _db_thread = asyncio.new_event_loop()
    _db_connection = _db_thread.run_until_complete(
        _run_async(sqlite3.connect, "hive.db"))

    def _run_query(self, query, *args):
        """Run the given query.

        This is a convenience wrapper; the actual execution happens on the
        dedicated thread.

        Args:
            query (string): SQL query to execute.

        Returns:
            list[sqlite3.Row]: Results of the query.
        """
        return self._db_thread.run_until_complete(
            _run_async(self._db_connection.execute, query, *args)).fetchall()

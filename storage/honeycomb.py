import asyncio
import sqlite3


async def _run_async(f, *args, **kwargs):
    """Async wrapper to let us run sync functions on a dedicated thread."""
    return f(*args, **kwargs)


class Honeycomb:
    """Base class to store data locally.
    
    Subclasses should override the `_table_name` and `_column_names` properties,
    and use `_run_query` to execute SQL commands.
    """
    _db_thread = asyncio.new_event_loop()
    _db_connection = _db_thread.run_until_complete(
        _run_async(sqlite3.connect, "hive.db"))

    def __init__(self):
        self._run_query("CREATE TABLE IF NOT EXISTS {} ({})".format(
            self._table_name, ", ".join(self._column_names)))

    @property
    def _table_name(self):
        """string: Name of the table this class represents."""
        raise NotImplementedError

    @property
    def _column_names(self):
        """tuple(string...): Names of the columns in this class' table."""
        raise NotImplementedError

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

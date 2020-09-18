from unittest import mock


class AsyncMock(mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        pass

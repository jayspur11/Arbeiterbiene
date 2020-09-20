import asyncio
import datetime
import discord
import random


class RepostWorker:
    def __init__(self, channel, url):
        self._message = None
        self._channel = channel
        self._url = url
        self._schedule()

    def cancel(self):
        self._future.cancel()

    def _schedule(self):
        self._future = asyncio.ensure_future(self._repost_and_reschedule())

    async def _repost_and_reschedule(self):
        await asyncio.sleep(random.randint(3600, 3 * 3600))
        now = datetime.datetime.now()
        if 8 <= now.time().hour < 17:
            if self._message:
                await self._message.delete()
            self._message = await self._channel.send(
                embed=discord.Embed().set_image(url=self._url))
        self._schedule()

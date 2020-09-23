import asyncio
import datetime
import discord
import random


class RepostWorker:
    def __init__(self, channel, url, last_message=None):
        self.last_message = last_message
        self.channel = channel
        self.url = url
        self._schedule()

    def cancel(self):
        self._future.cancel()

    def _schedule(self):
        self._future = asyncio.ensure_future(self._repost_and_reschedule())

    async def _repost_and_reschedule(self):
        await asyncio.sleep(random.randint(3600, 3 * 3600))
        now = datetime.datetime.now()
        if 8 <= now.time().hour < 17:
            if self.last_message:
                await self.last_message.delete()
            self.last_message = await self.channel.send(
                embed=discord.Embed().set_image(url=self.url))
        self._schedule()

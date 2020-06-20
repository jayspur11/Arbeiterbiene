import asyncio
import os
import random
from commands.base_command import BaseCommand
from discord import File


class RepostCommand(BaseCommand):
    """Class to add a 'repost' command to the bot."""

    def __init__(self):
        self._requests = {}  # {discord.Channel: _RepostRequest}

    @classmethod
    def trigger_word(cls):
        return "repost"

    def help_text(self):
        return """```repost (+attachment)```
        Schedules occasional reposting of the attachment.
        
        When the bot receives this command, it will save the attachment and re-upload it to the original channel 
        every few hours (exact timing determined randomly). Each subsequent upload will delete the previous one, 
        to avoid cluttering the channel.
         
        If the bot receives a second command in the same channel, it will override the previous attachment.
        
        If the bot receives an empty command, it will stop reposting.
        """

    async def run(self, command_io):
        channel = command_io.message.channel
        if not len(command_io.message.attachments):
            # No attachment means clear the repost or throw.
            self._requests[channel].cancel()
            del self._requests[channel]
            return
        if channel in self._requests:
            self._requests[channel].cancel()
            del self._requests[channel]
        attachment = command_io.message.attachments[0]
        filename = attachment.filename
        with open(filename, "bw+") as file:
            await attachment.save(file)
        self._requests[channel] = _RepostRequest(channel, filename)


class _RepostRequest:
    def __init__(self, channel, filename):
        self._channel = channel
        self._filename = filename
        self._schedule()
        self._message = None

    def cancel(self):
        self._future.cancel()
        os.remove(self._filename)

    def _schedule(self):
        self._future = asyncio.ensure_future(self._repost_and_reschedule())

    async def _repost_and_reschedule(self):
        await asyncio.sleep(random.randint(3600, 3 * 3600))
        if self._message:
            self._message.delete()
        with open(self._filename, "br") as file:
            self._message = await self._channel.send(file=File(file))
        self._schedule()

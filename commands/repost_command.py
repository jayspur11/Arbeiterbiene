import os
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
        
        When the bot receives this command, it will save the attachment and
         re-upload it to the original channel every few hours (exact timing is
         determined randomly).
         
        If the bot receives a second command in the same channel, it will
         override the previous attachment.
        
        If the bot receives an empty command, it will stop reposting.
        """

    async def run(self, command_io):
        channel = command_io.message.channel
        if not len(command_io.message.attachments):
            # No attachment means clear the repost or throw.
            del self._requests[channel]
            return
        attachment = command_io.message.attachments[0]
        filename = attachment.filename
        with open(filename, "bw+") as file:
            await attachment.save(file)
        self._requests[channel] = _RepostRequest(channel, filename)
        # TODO: schedule repost


class _RepostRequest:
    def __init__(self, channel, filename):
        self._channel = channel
        self._filename = filename
        self._timer_handle = None

    def __del__(self):
        if self._timer_handle:
            self._timer_handle.cancel()
        os.remove(self._filename)

    def schedule_repost(self, event_loop, delay):
        self._timer_handle = event_loop.call_later(delay, self._repost_and_reschedule, self, event_loop, delay)

    async def _repost_and_reschedule(self, event_loop, delay):
        with open(self._filename, "r") as file:
            await self._channel.send(file=File(file))
        # TODO: schedule again

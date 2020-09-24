from commands.core import base_command
from storage import repost_hc
from workers import repost_worker


class RepostCommand(base_command.BaseCommand):
    """Class to add a 'repost' command to the bot."""
    def __init__(self):
        self._requests = {}  # {discord.Channel: repost_worker.RepostWorker}
        self._honeycomb = repost_hc.RepostHC()

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
        self._requests[channel] = repost_worker.RepostWorker(
            channel, attachment.url)

    def load_with_client(self, client):
        reposts = self._honeycomb.reload_reposts(client)
        self._requests.update({repost.channel: repost for repost in reposts})

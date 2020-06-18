import os
from commands.base_command import BaseCommand
from discord import File


class RepostCommand(BaseCommand):
    """Class to add a 'repost' command to the bot."""

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
        attachment = command_io.message.attachments[0]
        with open(attachment.filename, "bw+") as file:
            await attachment.save(file)
            await command_io.message.channel.send(file=File(file))
        os.remove(attachment.filename)

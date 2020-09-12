from commands.core import base_command


class DieCommand(base_command.BaseCommand):
    """Class to add 'die' command to bot."""

    @classmethod
    def trigger_word(cls):
        return "die"

    def help_text(self):
        return """```die```
        Logs the bot out & kills the running process.
        """

    async def run(self, command_io):
        await command_io.message.channel.send(':(')
        raise KeyboardInterrupt

from commands import base_command


class DieCommand(base_command.BaseCommand):
    """Class to add 'die' command to bot."""

    def trigger_word(self):
        return "die"

    def help_text(self):
        return """```die```
        Logs the bot out & kills the running process.
        """

    async def run(self, message, bot):
        await bot.send_message(message.channel, ':(')
        raise KeyboardInterrupt

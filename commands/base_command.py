from commands.command_io import CommandIO


class BaseCommand:
    """Base class that outlines the methods needed by the command registrar."""

    @classmethod
    def trigger_word(cls):
        """Defines the word used to trigger this command,
            which is used by the registrar for fast indexing.
        Subclasses should return a string."""
        raise NotImplementedError

    def help_text(self):
        """Defines the text to be sent to users
            that need help with this command.
        Subclasses should return a string.
        - Note that this can use Discord markdown."""
        raise NotImplementedError

    async def run(self, command_io: CommandIO):
        """Executes the command."""
        raise NotImplementedError

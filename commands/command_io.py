from discord.ext.commands.bot import Bot
from discord.message import Message


class CommandIO:
    def __init__(self, bot: Bot):
        self.bot = bot
        self._message = None

    @property
    def message(self):
        if not self._message:
            raise AttributeError
        return self._message

    @message.setter
    def message(self, message: Message):
        self._message = message

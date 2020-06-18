from discord.ext.commands.bot import Bot
from discord.message import Message


class CommandIO:
    def __init__(self, bot: Bot, message: Message):
        self.bot = bot
        self.message = message

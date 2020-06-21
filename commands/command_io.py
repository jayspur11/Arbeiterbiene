from asyncio.events import AbstractEventLoop
from discord.ext.commands.bot import Bot
from discord.message import Message


class CommandIO:
    def __init__(self, bot: Bot, event_loop: AbstractEventLoop, message: Message):
        self.bot = bot
        self.event_loop = event_loop
        self.message = message

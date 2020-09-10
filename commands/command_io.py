from discord.message import Message


class CommandIO:
    def __init__(self, message: Message):
        self.message = message

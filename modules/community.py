""" Module for interactions with everyone.

A command belongs here if it involves more than one person.

A command does *not* belong here if it...
 - operates without any call or response, or
 - is an introvert.
"""

import emoji
import re
from modules import module
from modules import shared


_server_emoji_re = re.compile(r'<:.*:(.*)>')


def register_commands():
    @module.module_command
    async def poll(message):
        """```poll <question>
        <answer 1> <emojus>
        ...
        <answer N> <emojus>```
        Shortcut to add emoji as reactions to a poll question.

        Note: The bot is, sadly, unable to handle emoji from other servers.
        """
        custom_emoji_ids = _server_emoji_re.findall(message.content)
        server = message.server
        custom_emoji = []
        for emojus_id in custom_emoji_ids:
            emojus = shared.get_emoji_by_id(emojus_id, server)
            if not emojus:
                raise ValueError
            custom_emoji.append(emojus)
        for emojus in custom_emoji:
            await shared.bot.add_reaction(message, emojus)
        for emojus_match in emoji.get_emoji_regexp().finditer(message.content):
            await shared.bot.add_reaction(message, emojus_match.group())

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
        Echoes the poll back to the server and adds the emoji as reactions.

        Note: The bot is, sadly, unable to handle emoji from other servers.
        """
        custom_emoji_matches = _server_emoji_re.findall(message.content)
        server = message.server
        custom_emoji = []
        for emojus_match in custom_emoji_matches:
            emojus = shared.get_emoji_by_id(emojus_match.group(1), server)
            if not emojus:
                raise ValueError
            custom_emoji.append(emojus)
        poll_content = "Hey everyone! {op} would like to know:\n{q}".format(
            op=message.author.mention, q=message.content)
        poll_message = await shared.bot.send_message(message.channel,
                                                     poll_content)

        for emojus in custom_emoji:
            await shared.bot.add_reaction(poll_message, emojus)
        for emojus_match in emoji.get_emoji_regexp().finditer(message.content):
            await shared.bot.add_reaction(poll_message, emojus_match.group())

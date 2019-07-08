""" Module for interactions with everyone.

A command belongs here if it involves more than one person.

A command does *not* belong here if it...
 - operates without any call or response, or
 - is an introvert.
"""

import emoji
import re
from datetime import datetime
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
        """
        poll_content = "Hey everyone! {op} would like to know:\n{q}".format(
            op=message.author.mention, q=message.content)
        poll_message = await shared.bot.send_message(message.channel,
                                                     poll_content)

        server = message.server
        for emojus_match in _server_emoji_re.finditer(message.content):
            emojus = shared.get_emoji_by_id(emojus_match.group(1), server)
            await shared.bot.add_reaction(poll_message, emojus)
        for emojus_match in emoji.get_emoji_regexp().finditer(message.content):
            await shared.bot.add_reaction(poll_message, emojus_match.group())

        # def tally_votes():
        #     # TODO: count and notify
        #     pass
        # poll_end_time = int(datetime.now().timestamp()) + poll_duration
        # shared.schedule_activity(poll_end_time, tally_votes)

""" Module for interactions with everyone.

A command belongs here if it involves more than one person.

A command does *not* belong here if it...
 - operates without any call or response, or
 - is an introvert.
"""

from modules import module
from modules import shared


def register_commands():
    @module.module_command
    async def poll(message):
        """```poll "<question>" "<answer 1> <emoji>" ... "<answer N> <emoji>" [time limit]```
        Structures the poll and echoes it back to the server. After [time
        limit] has elapsed, counts the votes and notifies OP of the results.
        Default time limit is 24h.
        Answers should end with an emoji, so users can vote with a reaction.
        **The quotes are important!**
        """
        # parse answers
        # construct poll
        # echo to server
        # add reactions
        # TODO: eventually count the results


def _extract_poll_emoji(sanswer, server):
    """ Parses a poll answer (<string> <emoji>) for its emoji.

    :param sanswer: (string) String containing a poll answer and corresponding
        emoji.
    :param server: (discord.Server) Server to check for custom Emoji.
    :return: (?) Either a discord.Emoji object (for custom emoji), a string (for
        unicode emoji), or None (for an invalid string).
    """
    # TODO: check string validity
    emoji = sanswer.rsplit(' ', 1)[-1]
    if ':' in emoji:
        # emoji are formatted like '<:name:id>' and we want 'id'
        emoji_id = emoji.split(':')[-1][:-1]
        emoji = shared.get_emoji_by_id(emoji_id, server)
    return emoji

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
        answer_list = []
        segments = message.content.split('" ')
        for answer in segments[1:]:
            if '"' not in answer:
                # TODO: handle time limit
                break
            answer_list.append(_parse_poll_answer(answer.strip('"')))
        # construct poll
        # echo to server
        # add reactions
        # TODO: eventually count the results


def _parse_poll_answer(sanswer, server):
    """ Parses a poll answer (<string> <emoji>) for its emoji.

    :param sanswer: (string) String containing a poll answer and corresponding
        emoji.
    :param server: (discord.Server) Server to check for custom Emoji.
    :return: (tuple) A tuple containing a string respresenting the option, and
        either a discord.Emoji object (for custom emoji) or a string (for
        unicode emoji) representing the emoji reaction.

    :raises ValueError if the answer string is invalid.
    """
    # TODO: check string validity
    answer, emoji = sanswer.rsplit(' ', 1)[-1]
    if ':' in emoji:
        # emoji are formatted like '<:name:id>' and we want 'id'
        emoji_id = emoji.split(':')[-1][:-1]
        emoji = shared.get_emoji_by_id(emoji_id, server)
    return answer, emoji

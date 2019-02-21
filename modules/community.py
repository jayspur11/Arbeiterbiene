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
        """```poll <question> <answer 1 emote> <answer 2 emote> ... [time limit]```
        Structures the poll and echoes it back to the server. After [time
        limit] has elapsed, counts the votes and notifies OP of the results.
        Default time limit is 24h.
        Answers should end with an emote, so users can vote with a reaction.
        """
        # parse answers
        # construct poll
        # echo to server
        # add reactions
        # TODO: eventually count the results

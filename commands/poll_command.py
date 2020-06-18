import emoji
import re
from commands import base_command

_server_emoji_re = re.compile(r'<:.*:(.*)>')


class PollCommand(base_command.BaseCommand):
    """Class to add a 'poll' command to the bot."""

    @classmethod
    def trigger_word(cls):
        return "poll"

    def help_text(self):
        return """```poll <question>
        <answer 1> <emojus>
        ...
        <answer N> <emojus>```
        Shortcut to add emoji as reactions to a poll question.

        Note: The bot is, sadly, unable to handle emoji from other servers.
        """

    async def run(self, command_io):
        custom_emoji_ids = _server_emoji_re.findall(command_io.message.content)
        server = command_io.message.guild
        custom_emoji = []
        for emojus_id in custom_emoji_ids:
            emojus = get_emoji_by_id(emojus_id, server)
            if not emojus:
                raise ValueError
            custom_emoji.append(emojus)
        for emojus in custom_emoji:
            await command_io.message.add_reaction(emojus)
        for emojus_match in emoji.get_emoji_regexp().finditer(command_io.message.content):
            await command_io.message.add_reaction(emojus_match.group())


def get_emoji_by_id(sid, server):
    """ Retrieves an Emoji object from a server by ID.

    :param sid: (string) ID of the emoji.
    :param server: (discord.Server) Server containing the emoji.
    :return: Emoji object, or None if not found.
    """
    # linear search on hashable data. ugh.
    for emojus in server.emojis:
        if sid == str(emojus.id):
            return emojus
    return None

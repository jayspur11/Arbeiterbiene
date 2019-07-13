bot = None


def get_emoji_by_id(sid, server):
    """ Retrieves an Emoji object from a server by ID.

    :param sid: (string) ID of the emoji.
    :param server: (discord.Server) Server containing the emoji.
    :return: Emoji object, or None if not found.
    """
    # linear search on hashable data. ugh.
    for emoji in server.emojis:
        if sid == emoji.id:
            return emoji
    return None

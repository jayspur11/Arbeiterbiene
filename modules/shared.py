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


def parse_duration(sduration):
    """ Parses a duration specifier ([#d][#h][#m]) into seconds.

    :param sduration: (string) String to extract time length from.
    :return: (int) Number of seconds, or None if sduration was not valid.
    """
    duration_seconds = 0
    duration_values = [
        ('d', 86400),
        ('h', 3600),
        ('m', 60)
    ]

    for possible_duration, num_seconds in duration_values:
        if possible_duration in sduration:
            segment_duration, sduration = sduration.split(possible_duration, 1)
            try:
                duration_seconds += int(segment_duration) * num_seconds
            except ValueError:
                return None
    if sduration:
        # trailing info. don't know what was actually meant.
        return None
    if not duration_seconds:
        # 0 seconds? that's impossible. I won't allow it.
        return None

    return duration_seconds

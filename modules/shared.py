bot = None


def parse_duration(duration):
    """ Parses a duration specifier ([#d][#h][#m]) into seconds.

    :param duration: (string) String to extract time length from.
    :return: (int) Number of seconds, or None if duration was not valid.
    """
    duration_seconds = 0
    possible_durations = [
        ('d', 86400),
        ('h', 3600),
        ('m', 60)
    ]

    for possible_duration, num_seconds in possible_durations:
        if possible_duration in duration:
            dur_split = duration.split(possible_duration, 1)
            dur = dur_split[0]
            duration = dur_split[1]
            try:
                duration_seconds += int(dur) * num_seconds
            except ValueError:
                return None

    return duration_seconds if duration_seconds and not duration else None

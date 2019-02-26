import heapq
import threading
from datetime import datetime

bot = None
_future_activities = []  # TODO: make sure this survives outages


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


# TODO: we should do a much better job of handling 'time'
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


def schedule_activity(atime, activity):
    """ Schedule something to happen in the future.

    :param atime: Time the activity should happen (Unix epoch).
    :param activity: Function to call at the given time.
    """
    heapq.heappush(_future_activities, [atime, activity])
    # We will probably need a way to find scheduled activities, to cancel them.


def perform_scheduled_activities():
    """ Run any activities that have been scheduled to run by now. """
    # TODO: handle duplicate calls (though this shouldn't happen)
    tsnow = datetime.now().timestamp()
    while _future_activities and _future_activities[0][0] < tsnow:
        heapq.heappop(_future_activities)[1]()

    threading.Timer(60, perform_scheduled_activities()).start()

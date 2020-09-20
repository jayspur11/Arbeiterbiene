from storage import honeycomb

class RepostHC(honeycomb.Honeycomb):
    """Class for storing Repost command requests."""
    @property
    def _table_name(self):
        return "RepostCommands"

    @property
    def _column_names(self):
        return (
            "GuildID",
            "ChannelID",
            "LastMessageID",
            "URL"
        )

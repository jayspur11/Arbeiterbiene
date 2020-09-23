from storage import honeycomb


class RepostHC(honeycomb.Honeycomb):
    """Class for storing Repost command requests."""
    @property
    def _table_name(self):
        return "RepostCommands"

    @property
    def _column_names(self):
        return ("GuildID", "ChannelID", "LastMessageID", "URL")

    def store_repost(self, repost_worker):
        channel = repost_worker.channel
        message_id = (repost_worker.last_message.id
                      if repost_worker.last_message else "NULL")
        self._run_query(
            "INSERT INTO RepostCommands"
            "   VALUES(:guild, :channel, :msg, :url)",
            guild=channel.guild.id,
            channel=channel.id,
            msg=message_id,
            url=repost_worker.url)

    def update_repost(self, repost_worker):
        channel = repost_worker.channel
        message_id = (repost_worker.last_message.id
                      if repost_worker.last_message else "NULL")
        self._run_query(
            "UPDATE RepostCommands"
            "   SET LastMessageID=:msg, URL=:url"
            "   WHERE GuildID=:guild AND ChannelID=:channel",
            msg=message_id,
            url=repost_worker.url,
            guild=channel.guild.id,
            channel=channel.id)

    def remove_repost(self, repost_worker):
        channel = repost_worker.channnel
        self._run_query(
            "DELETE FROM RepostCommands"
            "   WHERE GuildID=:guild AND ChannelID=:channel",
            guild=channel.guild.id,
            channel=channel.id)

from workers import repost_worker
from storage import honeycomb


class RepostHC(honeycomb.Honeycomb):
    """Class for storing Repost command requests."""
    @property
    def _table_name(self):
        return "RepostCommands"

    @property
    def _column_names(self):
        return ("GuildID", "ChannelID", "LastMessageID", "URL")

    def create_repost(self, repost):
        channel = repost.channel
        message_id = (repost.last_message.id
                      if repost.last_message else "NULL")
        self._run_query(
            "INSERT INTO RepostCommands"
            "   VALUES(:guild, :channel, :msg, :url)",
            guild=channel.guild.id,
            channel=channel.id,
            msg=message_id,
            url=repost.url)

    def reload_reposts(self, client):
        reposts = []
        for result in self._run_query("SELECT * FROM RepostCommands"):
            channel = client.get_guild(result["GuildID"]).get_channel(
                result["ChannelID"])
            message = client.loop.run_until_complete(
                channel.fetch_message(result["MessageID"]))
            url = result["URL"]
            reposts.append(
                repost_worker.RepostWorker(channel, url, last_message=message))
        return reposts

    def update_repost(self, repost):
        channel = repost.channel
        message_id = (repost.last_message.id
                      if repost.last_message else "NULL")
        self._run_query(
            "UPDATE RepostCommands"
            "   SET LastMessageID=:msg, URL=:url"
            "   WHERE GuildID=:guild AND ChannelID=:channel",
            msg=message_id,
            url=repost.url,
            guild=channel.guild.id,
            channel=channel.id)

    def delete_repost(self, repost):
        channel = repost.channnel
        self._run_query(
            "DELETE FROM RepostCommands"
            "   WHERE GuildID=:guild AND ChannelID=:channel",
            guild=channel.guild.id,
            channel=channel.id)

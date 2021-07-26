from commands.aqi_command import AqiCommand
from commands.die_command import DieCommand
from commands.iseven_command import IsevenCommand
from commands.meow_command import MeowCommand
from commands.poll_command import PollCommand
from commands.repost_command import RepostCommand
from commands.roll_command import RollCommand
from commands.scion_command import ScionCommand
from commands.weather_command import WeatherCommand
from commands.woof_command import WoofCommand


def command_registry(airnowapi_key, owm_key):
    """Prepare a map of commands.

    Args:
        airnowapi_key (string): API key for `AirNowApi.org`.
        owm_key (string): API key for `OpenWeatherMap.org`.

    Returns:
        {string: BaseCommand}: Map of commands to use for incoming messages.
    """
    return {
        AqiCommand.trigger_word(): AqiCommand(airnowapi_key),
        DieCommand.trigger_word(): DieCommand(),
        IsevenCommand.trigger_word(): IsevenCommand(),
        MeowCommand.trigger_word(): MeowCommand(),
        PollCommand.trigger_word(): PollCommand(),
        RepostCommand.trigger_word(): RepostCommand(),
        RollCommand.trigger_word(): RollCommand(),
        ScionCommand.trigger_word(): ScionCommand(),
        WeatherCommand.trigger_word(): WeatherCommand(owm_key),
        WoofCommand.trigger_word(): WoofCommand()
    }

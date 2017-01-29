# TODO (jaysen): Expand this file!
import random
from .module import *

@module_command()
async def roll(message):
    split = message.content.split('d', 1)
    die_size = int(split[1])
    results = []
    for i in range(int(split[0])):
        results.append(random.randint(1,die_size))
    results.sort()
    for i, item in enumerate(results):
        results[i] = str(item)
    await bot.send_message(message.channel, ' + '.join(results))

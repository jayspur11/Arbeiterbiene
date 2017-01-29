# TODO (jaysen): Expand this file!
import random
from .module import *

@module_command
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

def scion_result_message(successes, results):
    firstResult = results[0]
    for i, item in enumerate(results):
        results[i] = str(item)
    message = ' + '.join(results)
    if successes == 0 and firstResult == 1:
        message = 'A botch! ' + message
    else:
        message = str(successes) + ' successes! ' + message
    return message

@module_command
async def scion(message):
    split = message.content.split(' ', 1)
    numDice = int(split[0])
    successes = int(split[1])
    if numDice > 0:
        results = []
        for i in range(numDice):
            results.append(random.randint(1, 10))
            if results[-1] > 6:
                successes += 1
            if results[-1] == 10:
                successes += 1
        results.sort()
        await bot.send_message(message.channel, scion_result_message(successes, results))

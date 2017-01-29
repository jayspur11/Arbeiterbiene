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

@module_command
async def scion(message):
    num_dice = 0
    successes = 0
    for arg in message.content.split(' '):
        if arg[0] == 's':
            successes += int(arg[1:])
        elif arg[-1] == 's':
            successes += int(arg[:-1])
        elif arg[0] == 'e':
            successes += scion_epic_successes(int(arg[1:]))
        elif arg[-1] == 'e':
            successes += scion_epic_successes(int(arg[:-1]))
        else:
            num_dice += int(arg)
    results = []
    for i in range(num_dice):
        result = random.randint(1, 10)
        if result > 6:
            successes += 1
        if result == 10:
            successes += 1
        results.append(result)
    results.sort()
    await bot.send_message(message.channel,
                           scion_result_message(successes, results))

## Helper Functions
def scion_epic_successes(epic_attr_value):
    if epic_attr_value == 0:
        return 0
    epic_successes = 1
    for i in range(1, epic_attr_value):
        epic_successes += i
    return epic_successes

def scion_result_message(successes, results):
    firstResult = results[0] if len(results) else 0
    for i, item in enumerate(results):
        results[i] = str(item)
    message = ' + '.join(results)
    if firstResult == 0:
        message = 'Got ' + str(successes) + ' successes without even trying.'
    elif successes == 0 and firstResult == 1:
        message = 'A botch! ' + message
    else:
        message = str(successes) + ' successes! ' + message
    return message

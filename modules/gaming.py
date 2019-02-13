""" Module for gaming-related commands.

A command belongs here if it...
 - is a tool to aid in gaming, or
 - is a game.

A command does *not* belong here if it...
 - is a tool that isn't related to gaming, or
 - is a picture of Hitler.
"""

from modules.module import *
import random

module_name = 'Gaming'


@module_command
async def roll(message):
    """```$roll XdY```
    Rolls dice and sends the ordered results to where the command came from.
    
    `X` is the number of dice to roll, and `Y` is the number of sides.
    """
    if not len(message.content):
        raise ValueError
    split = message.content.split('d', 1)
    die_size = int(split[1])
    results = []
    for i in range(int(split[0])):
        results.append(random.randint(1, die_size))
    results.sort()
    for i, item in enumerate(results):
        results[i] = str(item)
    await shared.bot.send_message(message.channel, ' + '.join(results))


@module_command
async def scion(message):
    """```$scion X e# s#```
    Rolls dice according to White Wolf's *Scion* rules and sends the result to
    where the command came from.
    
    `X` is the number of dice to roll, `e#` is the number of dots of
    an Epic Attribute involved, and `s#` is the number of automatic
    successes to add (do not include Epics in this number).
    **Notes:**
     - `#e` and `#s` are also accepted.
     - If using multiple Epic Attributes, include `e#` multiple times.
       (e.g. `$scion 7 e3 e4`)
     - If you don't like adding, you can include multiple raw numbers and
       they'll get added together to make your dice pool.
       (e.g. `$scion 3 4`)
    """
    if not len(message.content):
        raise ValueError
    num_dice = 0
    successes = 0
    args = message.content.split(' ')
    for arg in args:
        if arg[0] == 's':
            successes += int(arg[1:])
        elif arg[-1] == 's':
            successes += int(arg[:-1])
        elif arg[0] == 'e':
            successes += _scion_epic_successes(int(arg[1:]))
        elif arg[-1] == 'e':
            successes += _scion_epic_successes(int(arg[:-1]))
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
    await shared.bot.send_message(message.channel,
                                  _scion_result_message(successes, results))


def _scion_epic_successes(epic_attr_value):
    """
    Calculates the number of automatic successes a Scion gets for a given number
    of Epic Attribute dots.
    
    epic_attr_value (int):
        The number of dots the Scion has in an Epic Attribute.
    """
    if epic_attr_value == 0:
        return 0
    epic_successes = 1
    for i in range(1, epic_attr_value):
        epic_successes += i
    return epic_successes


def _scion_result_message(successes, results):
    """
    Formats a message for Scion roll results.
    
    successes (int):
        The number of successes garnered by the roll.
    
    results (list(int)):
        The values rolled.
    """
    results.sort()
    first_result = results[0] if len(results) else 0
    for i, item in enumerate(results):
        results[i] = str(item)
    message = ' + '.join(results)
    if first_result == 0:
        message = 'Got ' + str(successes) + ' successes without even trying.'
    elif successes == 0 and first_result == 1:
        message = 'A botch! ' + message
    else:
        message = str(successes) + ' successes! ' + message
    return message

""" Module for gaming-related commands.

A command belongs here if it...
 - is a tool to aid in gaming, or
 - is a game.

A command does *not* belong here if it...
 - is a tool that isn't related to gaming, or
 - is a picture of Hitler.
"""

from modules import module
from modules import shared
import random
import re


def register_commands():
    @module.module_command
    async def roll(message):
        """```roll XdY```
        Rolls dice and sends the result to where the command came from.

        `X` is the number of dice to roll, and `Y` is the number of sides.
        """
        if not len(message.content):
            raise ValueError
        roll_cmd = _parse_roll(message.content)
        # todo: sanitize input
        await shared.bot.send_message(
            message.channel, str(eval(roll_cmd)))

    @module.module_command
    async def scion(message):
        """```scion X e# s#```
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


def _roll_dice(num, sides):
    result = 0
    for i in range(num):
        result += random.randint(1, sides)
    return result


def _roll_table(num, table):
    results = []
    highest = len(table) - 1
    for i in range(num):
        results.append(table[random.randint(0, highest)])
    # TODO: sanitize output
    return ' + '.join(results)


def _parse_roll(command):
    """
    Parses a roll command into an interpretable equation.

    command (string):
        The roll command to translate (e.g. "1d20+1d6").

    Returns: string - the resulting Pythonic equation (e.g. "_roll(1,20)+_roll(1,6)").

    Raises: ValueError if the string couldn't be parsed, including a message about the offending format.
    TODO(jaysen): is ValErr the right thing to raise here?
    """
    arg_stack = []
    result = []
    while command:
        cmd0 = command[0]
        if cmd0 == 'd':
            arg, command = _parse_arg(command[1:])
            if arg[0] == '[':
                func = "_roll_table"
            else:
                func = "_roll_dice"
            result.append("{}({}, {})".format(func, arg_stack.pop(), arg))
        elif cmd0 in "+-":
            result.append(cmd0)
            command = command[1:]
        else:
            arg, command = _parse_arg(command)
            arg_stack.append(arg)
        command = command.strip()
    if arg_stack:
        result.append(arg_stack.pop())
    return ''.join(result)


_num_re = re.compile(r'\d+')


def _parse_arg(command):
    """
    Parses a roll command for the next argument block.

    command (string):
        The command to parse. (e.g. "2d6")

    Returns: string, string - the next arg, and the remainder of the command. (e.g. "2", "d6")
    """
    cmd0 = command[0]
    if cmd0 == "(":
        subroll, command = _extract_contents(command, '(', ')')
        arg = "({})".format(_parse_roll(subroll))
    elif cmd0 == "[":
        arg, command = _break_out_table(command)
    else:
        match = _num_re.match(command)
        arg = match.group()
        command = command[match.end():]
    return arg, command


def _extract_contents(command, opener, closer):
    """
    Parses a command string for the next fully-enclosed block, based on the given delimiters.

    command (string):
        The command to pull a block from. E.g. "(1d2)d20"

    opener (string):
        The opening delimiter. E.g. "("

    closer (string):
        The closing delimiter. E.g. ")"

    Returns: string, string - the enclosed block, and the remainder of the command. E.g. "1d2","d20"
    """
    unresolved = 1
    next_closed = command.find(closer)
    next_open = command.find(opener, 1)
    while True:
        if next_open == -1 or next_open > next_closed:
            unresolved -= 1
            if not unresolved:
                break
            next_closed = command.find(closer, next_closed+1)
        else:
            unresolved += 1
            next_open = command.find(opener, next_open+1)
    return command[1:next_closed], command[next_closed+1:]


_comma_re = re.compile(r',\s*')


def _break_out_table(command):
    """
    Parses a roll command for the next fully-bracketed table.

    command (string):
        The command to break out of. (e.g. "[hi, hello]")

    Returns: string, string - the interpretable table, and the remainder of the command. (e.g. "['hi','hello']", "")
    """
    table_string, command = _extract_contents(command, '[', ']')
    table = _comma_re.sub('","', table_string.replace('"', ''))  # anti-inject
    return '["{}"]'.format(table), command


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

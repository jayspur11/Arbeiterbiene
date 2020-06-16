import re
from commands import base_command

_comma_re = re.compile(r',\s*')
_num_re = re.compile(r'\d+')
_numeric_equation_re = re.compile(r'[()+\-\s\d]*')


class RollCommand(base_command.BaseCommand):
    """Class to add a 'roll' command to the bot."""

    def trigger_word(self):
        return "roll"

    def help_text(self):
        return """```roll XdY```
        Rolls dice and sends the result to where the command came from.

        `X` is the number of dice to roll, and `Y` is the number of sides.
        """

    async def run(self, message, bot):
        if not len(message.content):
            raise ValueError
        roll_cmd = _parse_roll(message.content)
        if _numeric_equation_re.fullmatch(roll_cmd):
            result_string = "**{}**\n{}".format(str(eval(roll_cmd)), roll_cmd)
        else:
            result_string = roll_cmd
        await bot.send_message(message.channel, result_string)


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
            arg1 = arg_stack.pop()
            if not _numeric_equation_re.fullmatch(arg1):
                raise ValueError
            if arg[0] == '[':
                func = "_roll_table"
            else:
                func = "_roll_dice"
                if not _numeric_equation_re.fullmatch(arg):
                    raise ValueError
            result.append(str(eval("{}({}, {})".format(func, arg1, arg))))
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

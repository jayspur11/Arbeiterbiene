# TODO (jaysen): Document this file!

module_commands = {}

def module_command(*args, **kwargs):
    def decorator(func):
        module_commands[func.__name__] = func
    return decorator

def process_command(cmd):
    if cmd in module_commands:
        module_commands[cmd]()
    else:
        raise KeyError

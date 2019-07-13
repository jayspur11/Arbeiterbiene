# Arbeiterbiene
Python-based Discord chat bot.

## How to bot?
First, you'll want to install
[Python 3.6.8](https://www.python.org/downloads/release/python-368/) - this is
the latest version supported by `discord.py`, so it just makes life easier. Once
that's done, `pip3 install emoji` to grab our own dependency.

Clone the source with
`git clone https://github.com/Mythos-Softworks/Arbeiterbiene.git`, then go into
the `discord.py` directory and run `git submodule init` followed by
`git submodule update`. (More info on submodules is available
[here](https://git-scm.com/book/en/v2/Git-Tools-Submodules).) Finally, run
`python setup.py install` to install all required dependencies for the
submodule.

Create an `auth.json` file with the same formatting as `example-auth.json`,
replacing the example token with your Discord Bot User's token. (Can be found on
Discord's developer portal: navigate to your app's `Bot` settings.)

Add the `discord.py` path to your `PYTHONPATH` environment, then run
`arbeiterbiene.py` to start up the bot!

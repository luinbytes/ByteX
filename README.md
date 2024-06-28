# ByteX

ByteX is a Discord bot client that allows you to manage your Discord client with ease. It is developed using Python and the discord.py-self library.

## Features

- TBD

## Installation

1. Clone the repository: `git clone https://github.com/yourusername/ByteX.git`

2. Install the dependencies: `pip install -r requirements.txt`

3. Run the bot at least once to allow for filesystem creation. Path: `%AppData%/Roaming/ByteX`

4. Add your token to the config.json in the path given previously.

5. Run the bot: `python main.py`

## Cogs

ByteX uses cogs for modular command handling. Each cog is a Python file that resides in the `cogs` directory. Here's an example of a cog:

```python
import discord
from discord.ext import commands

class MyCog(commands.Cog):
    """
    MyCog is a class that represents a Discord bot cog. It is an example of how to structure
    a cog for a discord.py bot. Each cog is essentially a Python module that contains a collection
    of commands, listeners, or a combination of both.

    Attributes:
        bot (commands.Bot): The discord.py Bot or AutoShardedBot instance.

    Methods:
        my_command(ctx): A command that sends a 'Hello, world!' message to the context channel.
    """

    def __init__(self, bot):
        """
        Constructs all the necessary attributes for the MyCog object.

        Parameters:
            bot (commands.Bot): The discord.py Bot or AutoShardedBot instance.
        """
        self.bot = bot

    @commands.command()
    async def my_command(self, ctx):
        """
        Sends a 'Hello, world!' message to the context channel. This is an example of a simple
        command. When a user in a server that your bot is in sends a message with the content
        "!my_command", this function will be triggered.

        Parameters:
            ctx (commands.Context): The context in which the command was called. This contains
            information like the channel the message was sent in, the author of the message, and
            the content of the message.
        """
        await ctx.send('Hello, world!')

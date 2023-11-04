import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="pk.",  # might be irrelevant tbh
            status=discord.Status.idle,
            activity=discord.Game(name="Scarlet and Violet"),
            intents=discord.Intents.all(),
            case_insensitive=True
        )

        self.remove_command("help")

        self.initial_extensions = [
            'sprites.guessing'
        ]

        for ext in self.initial_extensions:
            self.load_extension(ext)


bot = Bot()
bot.run(TOKEN)


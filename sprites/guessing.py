import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
from sprites.pokemonnames import ALL_POKEMON
from discord.utils import basic_autocomplete

load_dotenv()
TEST_SERVER = os.getenv("TEST_SERVER")

class GuessingGame(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.game_enabled = False
        self.curr_pokemon = None
        self.pokemon_lst = ALL_POKEMON
        self.scoreboard = {}
    
    @discord.commands.application_command(name="ping")
    async def ping(self, ctx, content: discord.Option(str)):
        await ctx.respond(f"You sent {content}")

    @discord.commands.application_command(
        name="start",
        description="Starts a Pokemon guessing game!"
    )
    async def start(self, ctx):
        if self.game_enabled:
            await ctx.respond("A game is already underway!")
            return
        
        await ctx.respond("Starting a game!", ephemeral=True)
        self.game_enabled = True
        
        # Let's figure out some back-end stuff
        # We need to generate a Pokedex number
        pokedex_number = random.randint(1, 1010)
        
        # this number should be linked to a Pokemon's name
        # (how players will actually guess the Pokemon)

        self.curr_pokemon = self.pokemon_lst[pokedex_number-1]

        # finally, we create the message!
        filename = f"sprites/{str(pokedex_number).zfill(3)}-dark.png"
        file = discord.File(filename)
        await ctx.channel.send("Who's that Pokemon?", file=file)

    @discord.commands.application_command(
        name="guess",
        description="Guess a Pokemon!"
    )
    async def guess(self, ctx: discord.ApplicationContext, pokemon_guess: discord.Option(str, "pokemon", autocomplete=basic_autocomplete(tuple(ALL_POKEMON)))):
        if not self.game_enabled:
            await ctx.respond("A game isn't currently active!", ephemeral=True)
            return
        if pokemon_guess == self.curr_pokemon:
            pokedex_number = str(ALL_POKEMON.index(self.curr_pokemon) + 1).zfill(3)
            filename = f"sprites/{pokedex_number}.png"
            file = discord.File(filename)
            await ctx.respond(f"Correct guess, <@{ctx.author.id}>! The Pokemon was {pokemon_guess}!", file=file)

            if ctx.author in self.scoreboard:
                self.scoreboard[ctx.author] += 1
            else:
                self.scoreboard[ctx.author] = 1

            # generating a new one
            pokedex_number = random.randint(1, 1010)
            self.curr_pokemon = self.pokemon_lst[pokedex_number-1]

            filename = f"sprites/{str(pokedex_number).zfill(3)}-dark.png"
            file = discord.File(filename)
            await ctx.channel.send("Who's that Pokemon?", file=file)

        else:
            await ctx.respond("Incorrect guess.", ephemeral=True)

    @discord.commands.application_command(
        name="skip",
        description="Skip the current round."
    )
    async def skip(self, ctx: discord.ApplicationContext):
        if not self.game_enabled:
            await ctx.respond("A game isn't currently active!", ephemeral=True)
            return
        pokedex_number = str(ALL_POKEMON.index(self.curr_pokemon) + 1).zfill(3)
        filename = f"sprites/{pokedex_number}.png"
        file = discord.File(filename)
        await ctx.respond(f"Skipping this round. The correct answer was {self.curr_pokemon}!", file=file)

        # generating a new one
        pokedex_number = random.randint(1, 1010)
        self.curr_pokemon = self.pokemon_lst[pokedex_number-1]

        filename = f"sprites/{str(pokedex_number).zfill(3)}-dark.png"
        file = discord.File(filename)
        await ctx.channel.send("Who's that Pokemon?", file=file)

    @discord.commands.application_command(
        name="stop",
        description="Ends the current game."
    )
    async def stop(self, ctx:discord.ApplicationContext):
        if not self.game_enabled:
            await ctx.respond("A game isn't currently active!", ephemeral=True)
            return
        
        pokedex_number = str(ALL_POKEMON.index(self.curr_pokemon) + 1).zfill(3)
        filename = f"sprites/{pokedex_number}.png"
        file = discord.File(filename)

        await ctx.respond(f"Stopping the game for now. The correct answer was {self.curr_pokemon}!", file=file)

        # turning off the game
        self.game_enabled = False
        self.curr_pokemon = None

        # printing out the scoreboard (only doing top 10, if necessary)
        # first I need to sort the keys into a list based on the value
        rankings = list(self.scoreboard.keys())
        rankings.sort(key=lambda x: self.scoreboard[x], reverse=True)
        s = "**Here is the leaderboard for this round:**\n"
        for i, item in enumerate(rankings):
            if i == 10:
                break
            
            s += f"{item.name}: {self.scoreboard[item]} points\n"
        
        await ctx.channel.send(s[:-1])

        self.scoreboard.clear()

    @discord.commands.application_command(
        name="help",
        description="Get some help!"
    )
    async def help(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(color=discord.Colour.brand_red())
        embed.set_author(name="Commands for Who's That Pokemon?")
        embed.add_field(
            name="`/help`",
            value="Prints this message.",
            inline=False
        )
        embed.add_field(
            name="`/start`",
            value="Starts a game.",
            inline=False
        )
        embed.add_field(
            name="`/guess <pokemon>`",
            value="Guess a Pokemon. This command autocompletes, so you don't have to remember the full spelling of the Pokemon.",
            inline=False
        )
        embed.add_field(
            name="`/skip`",
            value="Skips a round.",
            inline=False
        )
        embed.add_field(
            name="`/stop`",
            value="Stops the current game and prints the leaderboard.",
            inline=False
        )
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(GuessingGame(bot))

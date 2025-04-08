import os
import random

import discord
from dotenv import load_dotenv

from sprites.pokemonnames import ALL_POKEMON
from config import Config

load_dotenv()
TOKEN = os.getenv("TOKEN")


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your custom initialization code here    def __init__(self):
        self.game_enabled = False
        self.curr_pokemon = None
        self.pokemon_lst = ALL_POKEMON
        self.scoreboard = {}

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('$start'):
            if self.game_enabled:
                await message.channel.send("A game is already underway!")
                return

            await message.channel.send("Starting a game!")
            self.game_enabled = True

            # Let's figure out some back-end stuff
            # We need to generate a Pokédex number
            pokedex_number = random.randint(1, Config.LARGEST_POKEDEX_NUMBER)

            # this number should be linked to a Pokémon's name
            # (how players will actually guess the Pokémon)
            self.curr_pokemon = self.pokemon_lst[pokedex_number - 1]

            # finally, we create the message!
            filename = f"sprite_cache/{str(pokedex_number).zfill(3)}-dark.png"
            file = discord.File(filename)
            await message.channel.send("Who's that Pokemon?", file=file)

        if message.content.startswith('$guess'):
            if not self.game_enabled:
                await message.channel.send("A game isn't currently active!")
                return

            pokemon_guess = message.content[6:].strip()
            if self.curr_pokemon.lower() == pokemon_guess.lower():
                pokedex_number = str(ALL_POKEMON.index(self.curr_pokemon) + 1).zfill(3)
                filename = f"sprite_cache/{pokedex_number}.png"
                file = discord.File(filename)
                await message.channel.send(f"Correct guess! The Pokemon was {pokemon_guess}!",
                                           mention_author=True, file=file)

                author = message.author
                if author in self.scoreboard:
                    self.scoreboard[author] += 1
                else:
                    self.scoreboard[author] = 1

                # generating a new one
                pokedex_number = random.randint(1, Config.LARGEST_POKEDEX_NUMBER)
                self.curr_pokemon = self.pokemon_lst[pokedex_number - 1]

                filename = f"sprite_cache/{str(pokedex_number).zfill(3)}-dark.png"
                file = discord.File(filename)
                await message.channel.send("Who's that Pokemon?", file=file)

        if message.content.startswith('$skip'):
            if not self.game_enabled:
                await message.channel.send("A game isn't currently active!")
                return

            pokedex_number = str(ALL_POKEMON.index(self.curr_pokemon) + 1).zfill(3)
            filename = f"sprite_cache/{pokedex_number}.png"
            file = discord.File(filename)
            await message.channel.send(f"Skipping this round. The correct answer was {self.curr_pokemon}!", file=file)

            # generating a new one
            pokedex_number = random.randint(1, Config.LARGEST_POKEDEX_NUMBER)
            self.curr_pokemon = self.pokemon_lst[pokedex_number - 1]

            filename = f"sprite_cache/{str(pokedex_number).zfill(3)}-dark.png"
            file = discord.File(filename)
            await message.channel.send("Who's that Pokemon?", file=file)

        if message.content.startswith('$stop'):
            if not self.game_enabled:
                await message.respond("A game isn't currently active!")
                return

            pokedex_number = str(ALL_POKEMON.index(self.curr_pokemon) + 1).zfill(3)
            filename = f"sprite_cache/{pokedex_number}.png"
            file = discord.File(filename)

            await message.channel.send(f"Stopping the game for now. The correct answer was {self.curr_pokemon}!",
                                       file=file)

            # turning off the game
            self.game_enabled = False
            self.curr_pokemon = None

            # printing out the scoreboard (only doing top 10, if necessary)
            # first I need to sort the keys into a list based on the value
            rankings = list(self.scoreboard.keys())
            rankings.sort(key=lambda x: self.scoreboard[x], reverse=True)
            score_msg = "**Here is the leaderboard for this round:**\n"
            for user in rankings[:10]:
                score_msg += f"{user.name}: {self.scoreboard[user]} points\n"

            await message.channel.send(score_msg[:-1])

            self.scoreboard.clear()


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

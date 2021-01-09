#!/usr/bin/env python3

import discord
import asyncio
import time
import os
import sys
import json
import youtube_dl

from datetime import datetime
from discord.ext import commands
from discord.ext import tasks

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]

intents = discord.Intents.default()
bot = commands.Bot(prefix, intents = intents)
# bot = commands.when_mentioned_or(prefix)

# Create music dictionary
bot.music = {}
bot.ytdl = youtube_dl.YoutubeDL()

# HELP
bot.remove_command("help") # To create a personal help command 

# Load cogs
path = os.path.realpath(__file__)
path = path.replace('\\', '/')
path = path.replace('main.py', 'Cogs')
initial_extensions = os.listdir(path)
try:
    initial_extensions.remove("__pycache__")
except Exception as error:
    print(error)
print(initial_extensions)
initial_extensions3 = []
for initial_extensions2 in initial_extensions:
    initial_extensions2 = "Cogs." + initial_extensions2
    initial_extensions2 = initial_extensions2.replace(".py", "")
    initial_extensions3.append(initial_extensions2)

if __name__ == '__main__':
    for extension in initial_extensions3:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)

@bot.event
async def on_ready():
    for i in bot.guilds:
        bot.music[i.id] = {
            "volume": 0.5,
            "musics": [],
            "skip": {
                "count": 0,
                "users": []
            },
            "nowPlaying": None,
            "loop": False
        }
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(discord.__version__)

# ------------------------ RUN ------------------------ # 
bot.run(token)
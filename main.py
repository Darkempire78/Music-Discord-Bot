#!/usr/bin/env python3

import discord
import os
import json
import youtube_dl
import tekore # Spotify

from discord.ext import commands

from Tools.Utils import Utils

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]
    spotifyClientId = data["spotifyClientId"]
    spotifyClientSecret = data["spotifyClientSecret"]

intents = discord.Intents.default()
bot = commands.Bot(prefix, intents = intents)
# bot = commands.when_mentioned_or(prefix)

# Connect to Spotify
spotifyAppToken = tekore.request_client_token(spotifyClientId, spotifyClientSecret)
bot.spotify = tekore.Spotify(spotifyAppToken, asynchronous=True)

# Create music dictionary
bot.music = {}
bot.ytdl = youtube_dl.YoutubeDL({
    "quiet": True # Do not print messages to stdout.
})

# HELP
bot.remove_command("help") # To create a personal help command 

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    await Utils().generateGuildDictionnary(bot, bot.guilds)
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(f'We have logged in as {bot.user}')
    print(discord.__version__)

# ------------------------ RUN ------------------------ # 
bot.run(token)
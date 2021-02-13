#!/usr/bin/env python3

import discord
import wavelink
import os
import json
import youtube_dl
import tekore # Spotify

from discord.ext import commands

from Tools.Utils import Utils

from DataBase.Server import DBServer


class createEmojiList:
    def __init__(self, emojiList):
        self.youtubeLogo = emojiList["YoutubeLogo"]
        self.spotifyLogo = emojiList["SpotifyLogo"]
        self.soundcloudLogo = emojiList["SoundcloudLogo"]
        self.deezerLogo = emojiList["DeezerLogo"]
        self.true = emojiList["True"]
        self.false = emojiList["False"]
        self.alert = emojiList["Alert"]

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

    dblToken = data["dblToken"]


with open("emojis.json", "r") as emojiList:
    emojiList = json.load(emojiList)
    emojiList = {
        "YoutubeLogo": emojiList["YouTubeLogo"],
        "SpotifyLogo": emojiList["SpotifyLogo"],
        "SoundcloudLogo": emojiList["SoundCloudLogo"],
        "DeezerLogo": emojiList["DeezerLogo"],
        "True": emojiList["True"],
        "False": emojiList["False"],
        "Alert": emojiList["Alert"] 
    }


intents = discord.Intents.default()
bot = commands.Bot(prefix, intents = intents)

# Connect to Spotify
spotifyAppToken = tekore.request_client_token(spotifyClientId, spotifyClientSecret)
bot.spotify = tekore.Spotify(spotifyAppToken, asynchronous=True)

# Top.gg
bot.dblToken = dblToken

# Create music dictionary
bot.music = {}
bot.ytdl = youtube_dl.YoutubeDL({
    "quiet": True # Do not print messages to stdout.
})

# Emojis
bot.emojiList = createEmojiList(emojiList)

# HELP
bot.remove_command("help") # To create a personal help command 

# Load cogs
if __name__ == '__main__':
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    
    # Check if each server is in the DB
    print("Database check")
    servers = DBServer().display()
    serversId = [int(i[0]) for i in servers]
    for guild in bot.guilds:
        if guild.id not in serversId:
            DBServer().add(guild.id, "?", False, False, "")
            print(f"* {guild.name} ({guild.id}) added")
    
    print("----------------------------")
    print(f'We have logged in as {bot.user}')
    print(discord.__version__)

# ------------------------ RUN ------------------------ # 
bot.run(token)
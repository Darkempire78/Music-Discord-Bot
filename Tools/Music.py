import discord
import youtube_dl
import asyncio

class Music:
    def __init__(self, bot, link):
        video = bot.bot.ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.title = video["title"]
        self.duration = video["duration"]
        self.streamUrl = video_format["url"]
        self.thumbnails = video["thumbnails"][len(video["thumbnails"] )-1]["url"]
        self.isLive = video["is_live"]
import discord
import youtube_dl
import asyncio

import datetime

from youtubesearchpython import Video, StreamURLFetcher

class Music:
    def __init__(self, ctx, bot, link):
        
        # try:
        #     fetcher = StreamURLFetcher()
        #     video = Video.get(link)
        #     self.streamUrl = fetcher.get(video, 251)
        #     self.url = video["link"]
        #     self.title = video["title"]
        #     self.duration = int(video["streamingData"]["formats"][0]["approxDurationMs"])/1000
        #     self.thumbnails = video["thumbnails"][len(video["thumbnails"] )-1]["url"]
        # # If it's a Youtube live
        # except:
        try:
            video = bot.bot.ytdl.extract_info(link, download=False)
            self.url = video["webpage_url"]
            self.title = video["title"]
            self.duration = video["duration"]
            self.streamUrl = video["formats"][0]["url"]
            self.thumbnails = video["thumbnails"][len(video["thumbnails"] )-1]["url"]
        except Exception as e:
            asyncio.run_coroutine_threadsafe(ctx.channel.send(f"{bot.bot.emojiList.false} {ctx.author.mention} The song is unreadable!"), self.bot.loop)
            print("Extract video error : " + e)
import discord

from Tools.Music import Music
from Tools.playTrack import playTrack

async def addTrack(self, ctx, links):

    client = ctx.guild.voice_client

    if not isinstance(links, list):
        links = [links]

    playlistMessage = None
    isPlaylist = False
    if len(links) > 1:
        isPlaylist = True

    for link in links:
        if client and client.channel:
            if (self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]):
                return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm already connected in a voice channel!")
            if self.bot.music[ctx.guild.id]["nowPlaying"] is None:
                await ctx.send("Loading...", delete_after=10)
            music = Music(ctx, self, link)
            music.title = music.title.replace("*", "\\*")
            if music.duration is None:
                duration = "Live"
            else:
                musicDurationSeconds = round(music.duration % 60)
                if musicDurationSeconds < 10:
                    musicDurationSeconds = "0" + str(round(musicDurationSeconds))
                duration = f"{round(music.duration//60)}:{musicDurationSeconds}"
            
            if self.bot.music[ctx.guild.id]["nowPlaying"] is None:
                self.bot.music[ctx.guild.id]["musics"] = []
                self.bot.music[ctx.guild.id]["volume"] = 0.5
                return playTrack(self, ctx, client, {"music": music, "requestedBy": ctx.author})

            self.bot.music[ctx.guild.id]["musics"].append(
                {
                "music": music,
                "requestedBy": ctx.author
                }
            )

            # Queue duration
            queueDuration = sum(
                i["music"].duration
                for i in self.bot.music[ctx.guild.id]["musics"]
                if i["music"].duration is not None
            )
            queueDurationSeconds = round(queueDuration % 60)
            if queueDurationSeconds < 10:
                queueDurationSeconds = f"0{round(queueDurationSeconds)}"
            queueDuration = f"{round(queueDuration//60)}:{queueDurationSeconds}"

            if not isPlaylist:
                embed=discord.Embed(title="Song added in the queue", description=f"New song added : **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                embed.add_field(name="Place in the queue : ", value="`" + str(len(self.bot.music[ctx.guild.id]["musics"])) + f"`", inline=True)
                embed.add_field(name="Estimated time before playing :", value=f"`{queueDuration}`", inline=True)
                embed.set_thumbnail(url=music.thumbnails)
                await ctx.channel.send(embed=embed)
            else:
                # If it's a playlist => Update the same message to do not spam the channel
                if playlistMessage is None:
                    embed=discord.Embed(title="Song added in the queue", description=f"- **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                    embed.set_thumbnail(url=music.thumbnails)
                    playlistMessage = await ctx.channel.send(embed=embed)
                else:
                    # Update the message
                    embedEdited = discord.Embed(title="Songs added in the queue", description= playlistMessage.embeds[0].description + f"\n- **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                    playlistMessage.embeds[0].description = embedEdited.description
                    if len(playlistMessage.embeds[0].description) > 1800:
                        embed=discord.Embed(title="Song added in the queue", description=f"- **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                        embed.set_thumbnail(url=music.thumbnails)
                        playlistMessage = await ctx.channel.send(embed=embed)
                    else:
                        await playlistMessage.edit(embed=embedEdited)
                        
        else:
            voice = ctx.author.voice
            if ctx.author.voice is None:
                return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
            await ctx.send("Loading...", delete_after=10)
            # perm = voice.channel.overwrites_for(self.bot.user)
            client = await voice.channel.connect() # Connect the bot to the voice channel
            music = Music(ctx, self, link) # Get music data
            self.bot.music[ctx.guild.id]["musics"] = []
            self.bot.music[ctx.guild.id]["volume"] = 0.5
            playTrack(self, ctx, client, {"music": music, "requestedBy": ctx.author})
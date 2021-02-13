import discord
from discord.ext import commands

import wavelink

from Tools.Check import Check

from DataBase.Queue import DBQueue
from DataBase.Server import DBServer


class CogJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "join",
                    usage="",
                    description = "Add the bot in your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def join(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botNotInVoiceChannel(ctx, self.bot): return 

        channel = ctx.author.voice.channel
        
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.connect(channel.id)

        # Clear all the queue
        DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
        # Clear all server music parameters
        DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)
        
        await ctx.send(f"{ctx.author.mention} Connected in **`{channel.name}`**!")
        

    @commands.command(name = "leave",
                    usage="",
                    description = "Leave the bot of your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def leave(self, ctx):

        if not await Check().botInVoiceChannel(ctx, self.bot): return

        if not ctx.author.guild_permissions.administrator:
            if not await Check().userInVoiceChannel(ctx, self.bot): return 
            if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        player = self.bot.wavelink.get_player(ctx.guild.id)
        channelId = player.channel_id
        channel = self.bot.get_channel(channelId)

        if player.is_playing:
            await player.destroy()
        await player.disconnect()

        # Clear all the queue
        DBQueue(self.bot.dbConnection).clear(ctx.guild.id)
        # Clear all server music parameters
        DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)

        await ctx.channel.send(f"{ctx.author.mention} Disconnected from **`{channel.name}`**!")
        


def setup(bot):
    bot.add_cog(CogJoinLeave(bot))
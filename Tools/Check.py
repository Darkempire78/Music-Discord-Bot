import discord

class Check:

    async def userInVoiceChannel(self, ctx):
        """Check if the user is in a voice channel"""
        if ctx.author.voice is None:
            await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
            return False
        return True
    
    async def botInVoiceChannel(self, ctx):
        """Check if the bot is in a voice channel"""
        if ctx.guild.voice_client is None:
            await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm not connected in a voice channel!")
            return False
        return True

    async def userAndBotInSameVoiceChannel(self, ctx, bot):
        """Check if the user and the bot are in the same voice channel"""
        if ctx.guild.voice_client and bot.user.id not in [
            i.id for i in ctx.author.voice.channel.members
        ]:
            await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")
            return False
        return True

    async def queueEmpty(self, ctx, bot):
        """Check if the queue is empty"""
        if len(bot.music[ctx.guild.id]["musics"]) <= 0:
            await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The queue is empty!")
            return False
        return True
    
    async def botIsPlaying(self, ctx, bot):
        """Check if the bot is playing"""
        if not bot.music[ctx.guild.id]["nowPlaying"]:
            await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} There is currently no song to replay!")
            return False
        return True
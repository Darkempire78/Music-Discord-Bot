import discord
from discord.ext import commands

from Tools.Check import Check

class CogLoopLoopQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "loop",
                    usage="",
                    description = "Enable or disable the loop mode.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def loop(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        if self.bot.music[ctx.guild.id]["loop"]:
            self.bot.music[ctx.guild.id]["loop"] = False
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was disabled!")
        else:
            self.bot.music[ctx.guild.id]["loop"] = True
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was enabled!")

    @commands.command(name = "loopqueue",
                    aliases=["lq"],
                    usage="",
                    description = "Enable or disable the loop queue mode.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def loopqueue(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        
        if self.bot.music[ctx.guild.id]["loopQueue"]:
            self.bot.music[ctx.guild.id]["loopQueue"] = False
            await ctx.channel.send(f"{ctx.author.mention} The loop queue mode was disabled!")
        else:
            self.bot.music[ctx.guild.id]["loopQueue"] = True
            await ctx.channel.send(f"{ctx.author.mention} The loop queue mode was enabled!")


def setup(bot):
    bot.add_cog(CogLoopLoopQueue(bot))
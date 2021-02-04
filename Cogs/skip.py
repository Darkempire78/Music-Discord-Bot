import discord
from discord.ext import commands
from math import ceil

from Tools.Check import Check


class CogSkip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "skip",
                    aliases=["s"],
                    usage="",
                    description = "Skip the current music.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def skip(self, ctx):
 
        if not await Check().userInVoiceChannel(ctx): return 
        if not await Check().botInVoiceChannel(ctx): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        if not ctx.author.guild_permissions.administrator:
            # If user had already skip
            if ctx.author.id in self.bot.music[ctx.guild.id]["skip"]["users"]:
                return await ctx.send(f"{ctx.author.mention} Waiting for other voice users! (" + str(self.bot.music[ctx.guild.id]["skip"]["count"]) + f"/{ceil(len(ctx.author.voice.channel.voice_states)/2)})")
            
            self.bot.music[ctx.guild.id]["skip"]["count"] += 1
            self.bot.music[ctx.guild.id]["skip"]["users"].append(ctx.author.id)
            # Calcul the ratio
            ratio = self.bot.music[ctx.guild.id]["skip"]["count"]/(len(ctx.author.voice.channel.voice_states) -1) *100 # It's a percentage
            if not ratio > 50:
                return await ctx.send(f"{ctx.author.mention} Waiting for other voice users! (" + str(self.bot.music[ctx.guild.id]["skip"]["count"]) + f"/{ceil(len(ctx.author.voice.channel.voice_states)/2)})")

        # Clean the dict
        self.bot.music[ctx.guild.id]["skip"] = {"count": 0, "users": []}
        await ctx.send(f"{ctx.author.mention} Current music skipped!")

        client = ctx.guild.voice_client
        client.stop()


def setup(bot):
    bot.add_cog(CogSkip(bot))
import discord
from discord.ext import commands
from math import ceil


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
        if not ctx.author.guild_permissions.administrator:
            if ctx.author.voice is None:
                return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")

            # If user is not in the same voice channel that the bot
            if ctx.guild.voice_client and self.bot.user.id not in [
                i.id for i in ctx.author.voice.channel.members
            ]:
                return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")

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
import discord
from discord.ext import commands


class CogSupportInviteGithub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "support",
                    usage="",
                    description = "Give a link to join the support server.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def support(self, ctx):
        embed=discord.Embed(title="Support server :", description=f"Join the support server : https://discord.gg/f2UMbk95bv", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(name = "invite",
                    usage="",
                    description = "Give a link to invite the bot.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def invite(self, ctx):
        embed=discord.Embed(title="Invite the bot :", description=f"Invite {self.bot.user.mention} on your server : https://top.gg/bot/796749718217555978", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name = "github",
                    usage="",
                    description = "Give the github link of the bot.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def github(self, ctx):
        embed=discord.Embed(title="Github link :", description=f"See the code of {self.bot.user.mention} on GitHub : https://github.com/Darkempire78/Music-Discord-Bot", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name = "vote",
                    usage="",
                    description = "Give the Top.gg link to vote for the bot.")
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def vote(self, ctx):
        embed=discord.Embed(title="Vote link :", description=f"Vote for {self.bot.user.mention} on Top.gg : https://top.gg/bot/796749718217555978/vote", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogSupportInviteGithub(bot))
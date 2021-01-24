import discord
from discord.ext import commands


class CogSupportInviteGithub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "support",
                    usage="",
                    description = "Give a link to join the support server.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def support(self, ctx):
        embed=discord.Embed(title="Support server :", description=f"Join the support server : https://discord.gg/FxXQwKvmUY", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(name = "invite",
                    usage="",
                    description = "Give a link to invite the bot.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def invite(self, ctx):
        embed=discord.Embed(title="Invite the bot :", description=f"Invite {self.bot.user.mention} on your server : https://discord.com/oauth2/authorize?client_id=796749718217555978&scope=bot&permissions=2147483647", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name = "github",
                    usage="",
                    description = "Give the github link of the bot.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def github(self, ctx):
        embed=discord.Embed(title="Github link :", description=f"See the code of {self.bot.user.mention} on GitHub : https://github.com/Darkempire78/Music-Discord-Bot", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogSupportInviteGithub(bot))
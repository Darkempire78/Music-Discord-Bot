# import discord
# from discord.ext import commands


# class CogVolume(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot


#     @commands.command(name = "volume",
#                     usage="<0 to 100>",
#                     description = "Change the bot's volume.")
#     @commands.guild_only()
#     @commands.cooldown(1, 2, commands.BucketType.member)
#     async def volume(self, ctx, volume):
#         volume = int(volume)/100
#         discord.PCMVolumeTransformer(self.bot.music[ctx.guild.id]["source"], volume=volume)


# def setup(bot):
#     bot.add_cog(CogVolume(bot))
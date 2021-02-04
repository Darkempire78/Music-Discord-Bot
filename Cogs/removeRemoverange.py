import discord
from discord.ext import commands

from Tools.Check import Check

class CogRemoveRemoverange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "remove",
                    usage="<Index>",
                    description = "Remove the song with its index.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def remove(self, ctx, index):
        
        if not await Check().userInVoiceChannel(ctx): return 
        if not await Check().botInVoiceChannel(ctx): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        if not await Check().queueEmpty(ctx, self.bot): return 

        if not index.isdigit():
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The index have to be a number!")
        if (int(index) -1) > len(self.bot.music[ctx.guild.id]["musics"]):
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The index is invalid!")

        index = int(index) - 1
        music = self.bot.music[ctx.guild.id]["musics"][index]["music"]
        music.title = music.title.replace("*", "\\*")
        if music.duration is None:
            duration = "Live"
        else:
            musicDurationSeconds = round(music.duration % 60)
            if musicDurationSeconds < 10:
                musicDurationSeconds = "0" + str(round(musicDurationSeconds))
            duration = f"{round(music.duration//60)}:{musicDurationSeconds}"
        embed=discord.Embed(title="Song Removed in the queue", description=f"Song removed : **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
        embed.set_thumbnail(url=music.thumbnails)
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
        # Remove
        del self.bot.music[ctx.guild.id]["musics"][index]


    # @commands.command(name = "removerange",
    #                 usage="<FistIndex> <SecondIndex>",
    #                 description = "Remove the song with its index.")
    # @commands.guild_only()
    # @commands.cooldown(1, 2, commands.BucketType.member)
    # async def remove(self, ctx, index1,index2):
        
    #     if not await Check().userInVoiceChannel(ctx): return 
        # if not await Check().botInVoiceChannel(ctx): return 
        # if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        # if not await Check().queueEmpty(ctx, self.bot): return 
        
    #     if (not index1.isdigit()) or (not index2.isdigit()):
    #         return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} Indexs have to be numbers!")
    #     if (int(index2) -1) > len(self.bot.music[ctx.guild.id]["musics"]):
    #         return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} Indexs are invalid!")
    #     if index1 >= index2:
    #         return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The second index have to be bigger than the fisrt index invalid!")
        
    #     index1 = int(index1) - 1
    #     index2 = int(index2)
    #     message = ""

    #     for i, j in zip(range(len(self.bot.music[ctx.guild.id]["musics"])-1), self.bot.music[ctx.guild.id]["musics"]):
    #         print(self.bot.music[ctx.guild.id]["musics"][i]["music"].title, j["music"].title)

    #     for i in range(index1, index2):
    #         music = self.bot.music[ctx.guild.id]["musics"][i]["music"]
    #         music.title = music.title.replace("*", "\\*")
    #         if music.duration is None:
    #             duration = "Live"
    #         else:
    #             musicDurationSeconds = round(music.duration % 60)
    #             if musicDurationSeconds < 10:
    #                 musicDurationSeconds = "0" + str(round(musicDurationSeconds))
    #             duration = f"{round(music.duration//60)}:{musicDurationSeconds}"

    #             message += f"- **[{music.title}]({music.url})** ({duration})\n"
            
    #         # Remove
    #         del self.bot.music[ctx.guild.id]["musics"][i]

    #     embed=discord.Embed(title="Songs Removed in the queue", description=f"{message}", color=discord.Colour.random())
    #     embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
    #     await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(CogRemoveRemoverange(bot))
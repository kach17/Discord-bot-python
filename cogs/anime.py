import discord
from discord.ext import commands
import requests

class AnimeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="anime")
  async def anime(self, ctx, *, arg):
    argument = str(arg)
    results = requests.get(f"https://api.jikan.moe/v3/search/anime?q={argument}&limit=1")
    for i in results.json()["results"]:
      embed=discord.Embed(title=f'{i["title"]}', url=f'{i["url"]}', description=f'{i["synopsis"]}\n\n**Rating: ** {i["score"]}\n**Episodes:** {i["episodes"]}', color=0x5800db)
      embed.set_image(url=f'{i["image_url"]}')
      await ctx.send(embed=embed)

  @commands.command(name="manga")
  async def manga(self, ctx, *, arg):
    argument = str(arg)
    results = requests.get(f"https://api.jikan.moe/v3/search/manga?q={argument}&limit=1")
    for i in results.json()["results"]:
      embed=discord.Embed(title=f'{i["title"]}', url=f'{i["url"]}', description=f'{i["synopsis"]}\n\n**Rating: ** {i["score"]}\n**Chapters: ** {i["chapters"]}', color=0x5800db)
      embed.set_image(url=f'{i["image_url"]}')
      await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimeCog(bot))

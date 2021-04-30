from discord.ext import commands
import requests
from discord import Embed

class ApiCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['j'], help = "Tells a dark joke ranging from programming, spooky, christmas, dark and misc", brief = "Tells a dark joke by default.You can see the other categories from the commands help box")
  async def joke(self, ctx, type = "Dark"):
    the_link = "https://v2.jokeapi.dev/joke/"+type

    url = requests.get(the_link)
    api_data = url.json()

    part_1 = ((api_data['setup']))
    part_2 = ((api_data['delivery']))

    await ctx.send(part_1)
    await ctx.send(f"||{part_2}||")

  @commands.command(aliases=['imbored'], help ="Gives an activity according to the number of participants mentioned",  brief = "Gives a purpose to bored souls like me")
  async def bored(self, ctx, people = "1"):
    link = "http://www.boredapi.com/api/activity?participants="+people
    url = requests.get(link)
    api_data = url.json()    
    part_a = ((api_data['activity']))
    part_b = ((api_data['type']))


    embed = Embed(title="Imma help you?")
    fields = [("If you are so bored you can ~ ",str(part_a), False),("Type: ",str(part_b), False)]
    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)     
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ApiCog(bot))
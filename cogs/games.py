from random import choice
import json
import discord
from discord.ext import commands
import aiohttp
from datetime import datetime
import html
from discord.ext.commands.cooldowns import BucketType
with open('data/config.json') as f:
	CONFIG = json.load(f)


CLIENT_SESSION = aiohttp.ClientSession()
COLOR_RED = 0xEF2928
COLOR_BLUE = 0x0094E6

def parse_list_file(file_path: str) -> list:
	"""Parse a text file into a list containing each line."""
	
	with open(file_path) as f:
		return [l.strip() for l in f.readlines() if l.strip()]

database = {
	"truths": parse_list_file('data/truths.txt'),
	"dares": parse_list_file('data/dares.txt'),
	"nhie": parse_list_file('data/nhie.txt'),
	"tot": parse_list_file('data/tot.txt')
}


class GamesCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ['t'], help = "Gives a prompt for the game of truth!", brief = "Game of Truths!")
  @commands.cooldown(1, 2.5, BucketType.user)
  async def truth(self,ctx):
    """Get a truth question."""
    
    response = f"**Truth:** {choice(database['truths'])}" 
    await ctx.send(response)


  @commands.command(aliases = ['d'], help = "Gives a prompt for the game of dares!", brief = "Game of Daress!")
  @commands.cooldown(1, 3, BucketType.user)
  async def dare(self,ctx):
    """Get a dare."""
    
    response = f"**Dare:** {choice(database['dares'])}" 
    await ctx.send(response)


  @commands.command(aliases = ['neverhaveiever', 'nhie', 'ever', 'n'], help = "Gives questions for the age old game of never have I ever! ", brief = "Never Have I ever -")
  @commands.cooldown(1, 2.5, BucketType.user)
  async def never(self,ctx):
    """Get a never have I ever question."""
    
    response = f"**Never have I ever** {choice(database['nhie'])}" 
    await ctx.send(response)


  @commands.command(aliases = ['tot', 'tt'], help = "Gives you two options to choose from", brief = "This Or That game.")
  @commands.cooldown(1, 2.5, BucketType.user)
  async def thisorthat(self,ctx):
    """Get a this or that question."""
    
    response = choice(database['tot'])
    
    message = []
    # check if the question has a title.
    if ':' in response: 
      split = response.split(':')
      message.append(f"**{split[0]}**")  
      tort = split[1].strip()
    else:
      tort = response
    message.append(f"🔴 {tort.replace(' or ', ' **OR** ')} 🔵")
    
    embed = discord.Embed(
      color = choice((COLOR_RED, COLOR_BLUE)),
      timestamp = datetime.utcnow(),
      description = '\n'.join(message)
    )

    sent_embed = await ctx.send(embed = embed)
    await sent_embed.add_reaction("🔴")
    await sent_embed.add_reaction("🔵")



  @commands.command(aliases = ['wyr', 'rather'], help = "Gets you a would you rather question!", brief = "Would you rather?")
  @commands.cooldown(1, 3, BucketType.user)
  async def wouldyourather(self,ctx):
    """Get a would you rather question."""
    
    async with CLIENT_SESSION.get('http://either.io/questions/next/1/') as resp:
      result = await resp.json(content_type = None)
      result = result['questions'][0]

    option1, option2 = result['option_1'].capitalize(), result['option_2'].capitalize()
    option1_total, option2_total = int(result['option1_total']), int(result['option2_total'])
    option_total, comments = option1_total + option2_total, result['comment_total']
    title, desc, url = result['title'], result['moreinfo'], result['short_url']
    
    embed = discord.Embed(
      title = title,
      url = url,
      color = COLOR_RED if (option1_total > option2_total) else COLOR_BLUE,
      timestamp = datetime.utcnow()
    )
    embed.add_field(
      name = 'Would You Rather',
      value = f"🔴 `({(option1_total / option_total * 100):.1f}%)` {option1}\n🔵 `({(option2_total / option_total * 100):.1f}%)` {option2}",
      inline = False
    )
    if desc: embed.add_field(name = "More Info", value = desc, inline = False)
    embed.set_footer(text = f"either.io • 💬 {comments}")
    sent_embed = await ctx.send(embed = embed)
    await sent_embed.add_reaction("🔴")
    await sent_embed.add_reaction("🔵")



  @commands.command(aliases = ['wyp', 'willyoupressthebutton'], help = "If you are given two absurd choices, which one would you choose?", brief = "Will you press the button?")
  @commands.cooldown(1, 5, BucketType.user)
  async def button(self,ctx):
    """Get a will you press the button question."""
    
    async with CLIENT_SESSION.post('https://api2.willyoupressthebutton.com/api/v2/dilemma') as resp:
      result = await resp.json(content_type = None)
      result = result['dilemma']

    txt1, txt2 = html.unescape(result['txt1']), html.unescape(result['txt2'])
    will_press, wont_press = int(result['yes']), int(result['no'])
    press_total, q_id = (will_press + wont_press), result['id']
    url = f"https://willyoupressthebutton.com/{q_id}"
    
    embed = discord.Embed(
      title = "Press the button?",
      url = url,
      color = COLOR_RED if (will_press > wont_press) else COLOR_BLUE,
      timestamp = datetime.utcnow()
    )
    embed.add_field(
      name = 'Will you press the button if...',
      value = f"{txt1}\n**but...**\n{txt2}",
      inline = False
    )
    embed.add_field(
      name = 'Options',
      value = f"🔴 `({(will_press / press_total * 100):.1f}%)` I will press the button.\n🔵 `({(wont_press / press_total * 100):.1f}%)` I won't press the button.",
      inline = False
    )
    embed.set_footer(text = "willyoupressthebutton.com")
    sent_embed = await ctx.send(embed = embed)
    await sent_embed.add_reaction("🔴")
    await sent_embed.add_reaction("🔵")



 
def setup(bot):
    bot.add_cog(GamesCog(bot))
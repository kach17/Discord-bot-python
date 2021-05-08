from discord.ext import commands
import random
import re
import requests
import json
from data import all_lists


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

class EventsCog(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  @commands.Cog.listener()
  async def on_message(self, message):
    message.content.lower()
    if message.author.bot:
      return
    
    
    msg = message.content

    #silly dad joke lol
    reg_search = re.search(r'(i\'m|im|i am|not him) (.{1,})$', message.content, re.IGNORECASE)

    if reg_search:
        await message.channel.send('Hi {0}, I\'m Dad! {1.author.mention}'.format(reg_search.group(2), message))

    #first feature
    if "sad" in message.content.lower():
      return await message.channel.send(random.choice(all_lists
    .encouragements))
    


    if msg.startswith('Inspire me'):
      quote = get_quote()
      return await message.channel.send(quote)
    


    if "who is a loser" in message.content.lower():
        await message.channel.send('Advait is a loser')
    

    if "69" in message.content:
        await message.channel.send('nicee ( ͡° ͜ʖ ͡°)')
    
    
    if "advait" in message.content.lower():
        cuss = (random.choice(all_lists
      .bad_words))
        await message.channel.send("Oh!That Advait? He's {}".format(cuss))

    if "bad bot" in message.content.lower():
      return await message.channel.send(random.choice(all_lists
    .bad_bot))    

    if "good bot" in message.content.lower():
      return await message.channel.send(random.choice(all_lists
    .good_bot))    

    string = msg
    substring = "oya"
    count = string.count(substring)
    if count > 3:
      count = 1
    if substring in message.content.lower():
        await message.channel.send("Oya "*(count+2))


def setup(bot):
    bot.add_cog(EventsCog(bot))


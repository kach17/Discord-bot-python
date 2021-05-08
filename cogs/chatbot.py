from discord.ext import commands
from rivescript import RiveScript
import os.path
import asyncio



file = os.path.dirname(__file__)
brain = os.path.join(file, 'brain')

rs = RiveScript()
rs.load_directory(brain)
rs.sort_replies()


class ChatBotCog(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  @commands.Cog.listener()
  async def on_message(self, message):
    content = message.content.lower()
    if message.author.bot:
      return
    if message.channel.id != 831892826966065152:
      return
    else:
        reply = rs.reply("localuser", content)
        async with message.channel.typing():  
          await asyncio.sleep(2)
          await message.channel.send(reply)


def setup(bot):
    bot.add_cog(ChatBotCog(bot))


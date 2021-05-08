from discord.ext import commands
import requests
import os
from discord import Embed
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix = "#")
user_api = os.getenv('WEATHER_API')


class WeatherCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['w'], help = "Tells weather of any city!!", brief = "Shows weather")
  async def weather(self,ctx, location = "nagpur"):

    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+user_api
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    #create variables to store and display data
    temp_city = ((api_data['main']['temp']) - 273.15)
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']
    date_time = datetime.now().strftime("GMT %d %b %Y | %I:%M:%S %p")

    embed = Embed(title="Weather~",
					  description=("Weather Stats for - {}   \n({})".format(location.upper(), date_time)))
    embed.set_thumbnail(url=ctx.author
.avatar_url)
    fields = [("Temprature: ", str(temp_city), True),
  ("How's it looking :", str(weather_desc), True),("Humidity: ", str(hmdt), True),("Wind Speed: ", str(wind_spd), True)]

    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(WeatherCog(bot))


    



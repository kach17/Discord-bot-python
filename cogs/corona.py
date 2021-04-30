#CORONA UPDATES ====>
from discord.ext import commands
import requests
import asyncio



class CoronaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['corona', 'stats'], help = 'This command gives you CoViD-19 details of India \n\n(Default is set to Nagpur Maharashtra)\n\nType "all <--state-->"  for total stats of a particular state.', brief = 'CoVid-19 stats')
    async def covid(self, ctx, district="Nagpur", *, state="Maharashtra"):
        district = district.capitalize()
        state = state.title()


        if str(district) == "All":

            try:
          
                res = requests.get(
                    url="https://api.covid19india.org/state_district_wise.json"
                )
                res = res.json()
                flag = state.title()
                confirm, deceased, recovered, delcon, deldec, delrec = 0, 0, 0, 0, 0, 0
                for i in res[flag]["districtData"]:
                    confirm = confirm + \
                        res[flag]["districtData"][i]["confirmed"]
                    deceased = deceased + \
                        res[flag]["districtData"][i]["deceased"]
                    recovered = recovered + \
                        res[flag]["districtData"][i]["recovered"]
                    delrec = delrec + \
                        res[flag]["districtData"][i]["delta"]["recovered"]
                    delcon = delcon + \
                        res[flag]["districtData"][i]["delta"]["confirmed"]
                    deldec = deldec + \
                        res[flag]["districtData"][i]["delta"]["deceased"]
                
                await ctx.send(f"Hello {ctx.author.mention}, this command gives you CoViD-19 details of India")                    
                await ctx.send(
                    "**`" + flag + "`**\n\n:red_circle: `confirmed: " +
                    str(confirm) + "` :red_circle:\n:muscle: `recovered: " +
                    str(recovered) + "` :muscle:\n:blossom: `deceased: " +
                    str(deceased) +
                    "` :blossom:\n\n`Daily change:` \n\n:red_circle: `confirmed: "
                    + (str(delcon) if delcon != 0 else "Not updated yet") +
                    "`" + ":red_circle:\n:muscle: `recovered: " +
                    (str(delrec) if delrec != 0 else "Not updated yet") + "`" +
                    ":muscle:\n:blossom: `deceased: " +
                    (str(deldec) if deldec != 0 else "Not updated yet") +
                    "`:blossom:")
            except:
                await ctx.send("Please enter the state name correctly")

        else:

            try:
                res = requests.get(
                    url="https://api.covid19india.org/state_district_wise.json"
                )
                res = res.json()
                confirm = res[state]["districtData"][district]["delta"][
                    "confirmed"]
                deceased = res[state]["districtData"][district]["delta"][
                    "deceased"]
                recovered = res[state]["districtData"][district]["delta"][
                    "recovered"]

                await ctx.send(
                    f"**`Corona stats in {district}`**\n\n:red_circle: `confirmed: "
                    + (str(confirm) if confirm != 0 else "Not updated yet")+ "`"  + " :red_circle:\n:muscle: `recovered: " +
                    (str(recovered) if recovered != 0 else "Not updated yet")+ "`"  + " :muscle:\n:blossom: `deceased: " +
                    (str(deceased) if deceased != 0 else "Not updated yet")+ "`"  + " :blossom:\n\n")

                if str(confirm) == str(recovered) == str(deceased) == "0":

                  await asyncio.sleep(1)
                  await ctx.send("Maaaan")
                  await ctx.send("They sure are slow huh")

            except:
                await ctx.send("Please enter the city name correctly")


def setup(bot):
    bot.add_cog(CoronaCog(bot))

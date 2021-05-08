import discord
from discord.ext import commands
import aiohttp
import asyncio
import random

class Meme(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command(pass_context=True)
    async def dank(self,ctx):
        '''
        Posts a Dankmeme from r/Dankmemes
        '''
        embed = discord.Embed(title="From r/Dankmemes")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                async with ctx.channel.typing():
                  await asyncio.sleep(2)
      
                await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def meme(self,ctx):
        '''
        Posts a Meme from r/memes
        '''
        embed = discord.Embed(title="From r/memes")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                async with ctx.channel.typing():
                  await asyncio.sleep(2)
                await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def reddit(self,ctx, *, subreddit):
 
        embed = discord.Embed(title=f"From r/{subreddit}")

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                async with ctx.channel.typing():
                  await asyncio.sleep(2)
                await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Meme(bot))
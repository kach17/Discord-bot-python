import discord
import os
from data.keep_alive import keep_alive
from discord.ext import commands

client = commands.Bot(command_prefix = "#", case_insensitive=True)
client.remove_command("help")


@client.event
async def on_member_join(ctx,member):
    await ctx.send( f'Hi {member.name}, welcome to cul-Ahem server')
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to cul-Ahem server'
    )

@client.event
async def on_ready():
  print("Bot is online!")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='#help'))

#COGS ====>

modules = ['games', 'corona', 'admin', 'events', 'fun', 'help', 'info', 'weather', 'api', 'anime', 'meme']
try:
    for module in modules:
        client.load_extension('cogs.' + module)
        print(f'Loaded: {module}.')
except Exception as e:
    print(f'Error loading {module}: {e}')

print('Bot.....Activated')

#====START ====>

#EVENTS====>    

### --SHIFTED TO COGS ---###

#GAMES ====>

### --SHIFTED TO COGS ---###

#CORONA ====>

### --SHIFTED TO COGS ---###

#ADMINISTRATOR COMMANDS====>

### --SHIFTED TO COGS ---###

#HELP====>

### --SHIFTED TO COGS ---###

#ERROR HANDLING====>

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please type in a valid command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Please type in *all* arguments.")    
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the necessary permissions.")
    elif isinstance(error, commands.CommandOnCooldown):
      msg = "You are on cooldown, please try again in {:.2f}s".format(error.retry_after)
      await ctx.send(msg)

#API====>

### --SHIFTED TO COGS ---###

#<====END====

keep_alive()
client.run(os.getenv('TOKEN'))
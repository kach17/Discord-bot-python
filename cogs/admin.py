import discord
from discord.ext import commands


class AdminCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['c'])
  @commands.has_permissions(manage_messages = True)
  async def clear(self,ctx,amount=2):
    await ctx.channel.purge(limit=amount)

  @commands.command(aliases=['k'], help = "Kicks a member off the server", brief = "Kick a member")
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx,member : discord.Member, *, reason = "No reason provided"):
    try:
      await member.send("You have been kicked for the reasons of " + reason)
    except:
      await ctx.send("The member has their DM's off")
    await member.kick(reason = reason)

  @commands.command(aliases=['b'], help = "Bans a member from the server", brief = "Ban a member")
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx,member: discord.Member, *, reason = "No reason provided"):
    await member.send("You have been banned for the reasons of " + reason)
    await member.ban(reason = reason)

  @commands.command(aliases=['ub'], help = "Unbans a member from the server", brief = "Unban a member")
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
      user = banned_entry.user

      if(user.name + user.discriminator == member_name + member_disc ):
        await ctx.guild.unban(user)
        await ctx.send(member_name + "has been unbanned!")
        return
    await ctx.send(member = "was not found.")

  @commands.command(aliases=['m'], help = "Mutes the member lol", brief = "Mute a member")
  @commands.has_permissions(kick_members = True)
  async def mute(self,ctx, member: discord.Member = None, *, command=None):
    muted_role = ctx.guild.get_role(827640819980566548)

    await member.add_roles(muted_role)
    await ctx.send(member.mention + "has been muted")

  @commands.command(aliases=['um'], help = "Unmute the member.", brief = "Unmute a member")
  @commands.has_permissions(kick_members = True)
  async def unmute(self,ctx, member: discord.Member = None, *, command=None):
    unmuted_role = ctx.guild.get_role(827640819980566548)

    await member.remove_roles(unmuted_role)
    await ctx.send(member.mention + "has been unmuted") 


def setup(bot):
    bot.add_cog(AdminCog(bot))
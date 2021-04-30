from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

class InfoCog(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="info", aliases=["memberinfo", "ui", "mi",'userinfo'])
	async def user_info(self, ctx, target: Optional[Member]):
		target = target or ctx.author

		embed = Embed(title="User information",
					  colour=target.colour,
					  timestamp=datetime.utcnow())

		embed.set_thumbnail(url=target.avatar_url)

		fields = [("Name", str(target), True),
				  ("ID", target.id, True),
				  ("Bot?", target.bot, True),
				  ("Top role", target.top_role.mention, True),
				  ("Status", str(target.status).title(), True),
				  ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
				  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Boosted", bool(target.premium_since), True)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(InfoCog(bot))
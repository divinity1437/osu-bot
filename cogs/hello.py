# cogs / test.py
from discord.ext import commands

class Test(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command()
	async def hello(self, ctx):
		author = ctx.message.author
		await ctx.send(f"Hello, {author.mention}!")

def setup(client):
	client.add_cog(Test(client))
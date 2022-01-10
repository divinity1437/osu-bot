# cogs / test.py
from discord.ext import commands
import requests
import json
import discord

class Wink(commands.Cog):
	def __init__(self, client):
		self.client = client # sets the client variable so we can use it in cogs
	
	@commands.command()
	async def wink(self, ctx):
		response = requests.get('https://some-random-api.ml/animu/wink')
		json_data = response.json()

		embed = discord.Embed(color=discord.Colour.random(), title = 'Some wink')
		embed.set_image(url=json_data['link'])
		await ctx.send(embed=embed)
		await ctx.message.delete()

def setup(client):
	client.add_cog(Wink(client))
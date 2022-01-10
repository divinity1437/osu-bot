# cogs / test.py
from discord.ext import commands
import discord
import requests
import glob
import hashlib
from datetime import timedelta

from objects import apiRequest

"""
		    avatar_request = requests.get(f"https://a.ppy.sh/{osu_user_id}")
		    avatar_response = avatar_request.text

		    hash_object = hashlib.md5(avatar_response.encode())
		    avatar_md5_hash = hash_object.hexdigest()

		    if avatar_md5_hash == "9226b343e6fe53b64aa8b06b3f4c2f19":
		        osu_avatar = avatar_guest
		    else:
		        osu_avatar = f"https://a.ppy.sh/{osu_user_id}" 

		    title = f'osu! Standard Profile for {osu_username}'    
		    embed = discord.Embed(color = discord.Colour.random(),description=f"**▸PP:** {round(float(pp_raw),2)}\n**▸Level:** {level}\n**▸Accuracy:** {round(float(accuracy),2)}\n**▸Playcount:** {playcount}")
		    embed.set_author(name=title, icon_url = osu_user_country)
		    embed.set_thumbnail(url=osu_avatar)
		    await ctx.send(embed = embed)
"""

avatar_guest = "https://osu.ppy.sh/images/layout/avatar-guest.png"

class Osu(commands.Cog):
	def __init__(self, client):
		self.client = client 
	
	@commands.command()
	async def osu(self,ctx,arg):

		osu = apiRequest.New()
		osu.get_user(arg)

		embed = discord.Embed(color = discord.Colour.random(),description=f"**▸Rank:** #{osu.pp_rank} ({osu.country}#{osu.pp_country_rank})\n**▸Level:** {(round(float(osu.level),1))}\n**▸PP:** {round(float(osu.pp_raw),2)}\n**▸Playcount:** {osu.playcount}")
		embed.set_author(name=f"osu! Standart profile for {osu.username}!",url=f"https://osu.ppy.sh/u/{osu.user_id}", icon_url = f"https://osu.ppy.sh/images/flags/{osu.country_acronym}.png")
		embed.set_thumbnail(url=f"https://a.ppy.sh/{osu.user_id}")
		await ctx.send(embed=embed)

	@commands.command()
	async def recent(self,ctx,arg):

		osu = apiRequest.New()
		osu.get_user_recent(arg)
		osu.get_beatmaps(osu.beatmap_id)

		embed = discord.Embed(color = discord.Colour.random(),description=f"**▸**{osu.rank}\n**▸Score**: {osu.score}\n**▸**x{osu.maxcombo}/{osu.max_combo} **▸** [{osu.count300}/{osu.count100}/{osu.count50}/{osu.countmiss}]")
		embed.set_author(name=osu.title, url=f"https://osu.ppy.sh/b/{osu.beatmap_id}", icon_url=f"https://a.ppy.sh/{osu.user_id}")
		embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{osu.beatmapset_id}.jpg")
		embed.set_footer(text=osu.date)
		await ctx.send(embed=embed)

	@commands.command()
	async def map(self,ctx,arg):
	    
		osu = apiRequest.New()
		osu.get_beatmaps(arg)

		embed = discord.Embed(color = discord.Colour.random(),description=f"**▸Difficulty:** {(round(float(osu.difficultyrating),2))} **▸Max combo:** {osu.max_combo}\n**▸AR:** {osu.diff_approach} **▸OD:** {osu.diff_overall} **▸HP:** {osu.diff_drain} **▸CS:** {osu.diff_size}\n **▸BPM:** {osu.bpm} **▸Length:** {osu.total_length}")
		embed.set_author(name=osu.title,url=f"https://osu.ppy.sh/s/{osu.beatmapset_id}", icon_url = f"https://a.ppy.sh/{osu.creator_id}")
		embed.set_thumbnail(url=f"https://b.ppy.sh/thumb/{osu.beatmapset_id}.jpg")
		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Osu(client))
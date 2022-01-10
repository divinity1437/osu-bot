# cogs / test.py
from discord.ext import commands
from objects import apiRequest
import requests
import glob
import discord

avatar_guest = "https://osu.ppy.sh/images/layout/avatar-guest.png"

class Kurikku(commands.Cog):
	def __init__(self, client):
		self.client = client 
	
	@commands.command()
	async def kurikku(self,ctx,arg):

		osu = apiRequest.New()
		osu.get_user_kurikku(arg)

		embed = discord.Embed(color = discord.Colour.random(),description=f"**▸Rank:** #{osu.pp_rank} ({osu.country}#{osu.pp_country_rank})\n**▸Level:** {(round(float(osu.level),1))}\n**▸PP:** {round(float(osu.pp_raw),2)}\n**▸Playcount:** {osu.playcount}")
		embed.set_author(name=f"osu! Standart profile for {osu.username}!",url=f"https://kurikku.pw/u/{osu.user_id}", icon_url = f"https://osu.ppy.sh/images/flags/{osu.country_acronym}.png")
		embed.set_thumbnail(url=f"https://a.kurikku.pw/{osu.user_id}")
		await ctx.send(embed=embed)


	@commands.command()
	async def kmapleader(self,ctx, beatmap_arg): # number 1 from beatmap, only work with beatmap id / WIP!!!!!!!!!!!!
	    json_data = requests.get(f"https://kurikku.pw/api/v1/scores?b={beatmap_arg}&l=1").json()
	    try:
	      json_data
	    except IndexError:
	      return await ctx.send("Uh oh #1 not found or error appeared!")

	    try: 
	        code = json_data["code"]
	        print(f"used kmapleader command")
	        scores = json_data["scores"][0]
	        score = json_data["scores"][0]["score"]
	        max_combo = json_data["scores"][0]["max_combo"]
	        count_300 = json_data["scores"][0]["count_300"]
	        count_100 = json_data["scores"][0]["count_100"]
	        count_50 = json_data["scores"][0]["count_50"]
	        count_miss = json_data["scores"][0]["count_miss"]
	        accuracy = json_data["scores"][0]["accuracy"]
	        modss = int(json_data["scores"][0]["mods"])
	        pp = json_data["scores"][0]["pp"]
	        rank = json_data["scores"][0]["rank"]
	        username = json_data["scores"][0]["user"]["username"]
	        time = json_data["scores"][0]["time"]
	    except:
	        return await ctx.send("Sorry, error appeared!")

	    userid = requests.get(f"https://kurikku.pw/api/v1/users/whatid?name={username}").json()

	    score_mods = ""

	    if modss == 0:
	        score_mods += "NM"
	    if modss & mods.NOFAIL > 0:
	        score_mods += "NF"
	    if modss & mods.EASY > 0:
	        score_mods += "EZ"
	    if modss & mods.HIDDEN > 0:
	        score_mods += "HD"
	    if modss & mods.HARDROCK > 0:
	        score_mods += "HR"
	    if modss & mods.DOUBLETIME > 0:
	        score_mods += "DT"
	    if modss & mods.HALFTIME > 0:
	        score_mods += "HT"
	    if modss & mods.FLASHLIGHT > 0:
	        score_mods += "FL"
	    if modss & mods.SPUNOUT > 0:
	        score_mods += "SO"
	    if modss & mods.TOUCHSCREEN > 0:
	        score_mods += "TD"
	    if modss & mods.RELAX > 0:
	        score_mods += "RX"
	    if modss & mods.RELAX2 > 0:
	        score_mods += "AP"


	    embed = discord.Embed(color=discord.Colour.random(), description=f"**▸Username:** {username}\n**▸Score:** {score}\n**▸PP:** {pp}\n**▸Accuracy:** {accuracy}\n**▸Max combo:** {max_combo}\n**▸Rank:** {rank}\n**▸300:** {count_300} **▸100:** {count_100} **▸50:** {count_50} **▸Miss:** {count_miss}")
	    embed.set_author(name=username, url=f"https://kurikku.pw/u/{userid['id']}")
	    embed.set_footer(text=time)
	    embed.set_thumbnail(url=f"https://a.kurikku.pw/{userid['id']}")
	    await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Kurikku(client))
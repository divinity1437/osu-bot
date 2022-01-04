import discord
from discord.ext import commands
from config import settings
import json
import requests
import random
import hashlib
import time
import decimal
import math
import asyncio
from discord.ext.commands import Bot
from time import strftime
from time import gmtime

osu_api_key = "ur api here"
avatar_guest = "https://osu.ppy.sh/images/layout/avatar-guest.png"
silver_ss = "https://cdn.discordapp.com/emojis/462313722556186626.webp?size=44&quality=lossless"
gold_ss = "https://cdn.discordapp.com/emojis/462313722736672780.webp?size=44&quality=lossless"
silver_s = "https://cdn.discordapp.com/emojis/462313722732347401.webp?size=44&quality=lossless"
gold_s = "https://cdn.discordapp.com/emojis/462313719762911233.webp?size=44&quality=lossless"
a_rank = "https://cdn.discordapp.com/emojis/462313719083565066.webp?size=44&quality=lossless"

bot = commands.Bot(command_prefix = settings['prefix']) 

@bot.event
async def on_ready():
    print('------')
    print('Logged in as',bot.user.name)
    print('------')

@bot.command() 
async def hello(ctx): 
    author = ctx.message.author 

    await ctx.send(f'Hello, {author.mention}!') 
    await ctx.message.delete()

@bot.command()
async def help_me(ctx):
    author = ctx.message.author

    await ctx.send(f'Hi, {author.mention}!')
    title = f'Here your help embed'
    helpa = """
    Wink - send you some Wink gif/png 
Help_Me - send you embed with commands (You look at it rn) 
Osu - send you osu! stats from bancho 
Map - send you osu! map stats from bancho
    """
    embed = discord.Embed(color = discord.Colour.random())
    embed.set_author(name=helpa, icon_url = "https://a.ppy.sh/10081838")

    embed.set_thumbnail(url="https://a.ppy.sh/10081838")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def wink(ctx):
	response = requests.get('https://some-random-api.ml/animu/wink')
	json_data = json.loads(response.text)

	embed = discord.Embed(color = discord.Colour.random(), title = 'Some wink')
	embed.set_image(url = json_data['link'])
	await ctx.send(embed = embed)
	await ctx.message.delete()

@bot.command()
async def osu(ctx,user_arg):    
    
    response = requests.get(f"https://osu.ppy.sh/api/get_user?k={osu_api_key}&u={user_arg}")
    resp = json.loads(response.text)

    try:
      give_me_json = resp[0]
    except IndexError:
      return await ctx.send("Uh oh user not found!")
  
    osu_username = give_me_json["username"]
    osu_user_id = give_me_json["user_id"]
    osu_country_acronym = give_me_json["country"]
    osu_user_country = f"https://osu.ppy.sh/images/flags/{osu_country_acronym}.png"
    playcount = give_me_json["playcount"]
    pp_raw = give_me_json["pp_raw"]
    level = give_me_json["level"]
    accuracy = give_me_json["accuracy"]
    count_rank_ss = give_me_json["count_rank_ss"]
    count_rank_s = give_me_json["count_rank_s"]
    count_rank_sh = give_me_json["count_rank_sh"]
    count_rank_a = give_me_json["count_rank_a"]

    avatar_request = requests.get(f"https://a.ppy.sh/{osu_user_id}")
    avatar_response = avatar_request.text

    hash_object = hashlib.md5(avatar_response.encode())
    avatar_md5_hash = hash_object.hexdigest()

    if avatar_md5_hash == "9226b343e6fe53b64aa8b06b3f4c2f19":
        osu_avatar = avatar_guest
    else:
        osu_avatar = f"https://a.ppy.sh/{osu_user_id}" 

    osu = """"""

    title = f'osu! Standard Profile for {osu_username}'    
    embed = discord.Embed(color = discord.Colour.random(),description=pp_raw)
    embed.set_author(name=title, icon_url = osu_user_country)
    embed.set_thumbnail(url=osu_avatar)
    embed.add_field(name="▸PP", value=(round(int(float(pp_raw)))), inline=True)
    embed.add_field(name="▸Level", value=(round(int(float(level)))), inline=True)
    embed.add_field(name="▸Accuracy", value=(int(float((accuracy)))), inline=True)
    embed.add_field(name="▸Playcount", value=(round(int(float(playcount)))), inline=True)
    embed.description = osu
    await ctx.send(embed = embed)

@bot.command()
async def map(ctx,beatmap_arg):
    response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={osu_api_key}&s={beatmap_arg}")
    resp = json.loads(response.text)

    try:
        give_me_json = resp[0]
    except IndexError:
        return await ctx.send("Beatmap not found!")

    beatmapset_id = give_me_json["beatmapset_id"]
    beatmap_artist = give_me_json["artist"]
    beatmap_title = give_me_json["title"]
    beatmap_bpm = give_me_json["bpm"]
    creator_id = give_me_json["creator_id"]
    osu_creator_id_avatar = f"https://a.ppy.sh/{creator_id}"
    beatmap_bg = f"https://b.ppy.sh/thumb/{beatmapset_id}.jpg"
    difficultyrating = give_me_json["difficultyrating"]
    total_length = int(give_me_json["total_length"])
    diff_size = give_me_json["diff_size"] # cs
    diff_overall = give_me_json["diff_overall"] # od
    diff_approach = give_me_json["diff_approach"] # ar 
    diff_drain = give_me_json["diff_drain"] # hp
    max_combo = give_me_json["max_combo"]

    example = """
    """

    if total_length >= 3600:
        time = strftime("Lenght: **%H:%M:%S**", gmtime(total_length))
    else:
        time = strftime("Lenght: **%M:%S**", gmtime(total_length))


    embed = discord.Embed(color = discord.Colour.random(),description=time)
    embed.set_author(name=beatmap_title,url=f"https://osu.ppy.sh/s/{beatmapset_id}", icon_url = osu_creator_id_avatar)
    embed.add_field(name="▸Difficulty", value=difficultyrating, inline=True)
    embed.add_field(name="▸Max combo", value=max_combo, inline=True)
    embed.add_field(name="▸AR", value=diff_approach, inline=True)
    embed.add_field(name="▸OD", value=diff_overall, inline=True)
    embed.add_field(name="▸HP", value=diff_drain, inline=True)
    embed.add_field(name="▸CS", value=diff_size, inline=True)
    embed.add_field(name="▸BPM", value=beatmap_bpm, inline=True)
    embed.set_thumbnail(url=beatmap_bg)
    embed.description = time
    await ctx.send(embed=embed)

@bot.command()
async def recent(ctx,user_arg,beatmap_arg):
    response = requests.get(f"https://osu.ppy.sh/api/get_user_recent?k={osu_api_key}&u={user_arg}")
    response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={osu_api_key}&s={beatmap_arg}")
    resp = json.loads(response.text)

    try:
        give_me_json = resp[0]
    except IndexError:
        return await ctx.send("Can't find recent play!")

    osu_username = give_me_json["username"]
    osu_user_id = give_me_json["user_id"]
    beatmapset_id = give_me_json["beatmapset_id"]
    beatmap_artist = give_me_json["artist"]
    beatmap_title = give_me_json["title"]
    avatar_request = requests.get(f"https://a.ppy.sh/{osu_user_id}")
    avatar_response = avatar_request.text
    beatmap_bg = f"https://b.ppy.sh/thumb/{beatmapset_id}.jpg"
    difficultyrating = give_me_json["difficultyrating"]
    score = give_me_json["score"]
    maxcombo = give_me_json["maxcombo"]
    countmiss = give_me_json["countmiss"]
    count300 = give_me_json["count300"]
    count100 = give_me_json["count300"]
    count50 = give_me_json["count300"]
    rank = give_me_json["rank"]

    hash_object = hashlib.md5(avatar_response.encode())
    avatar_md5_hash = hash_object.hexdigest()

    if avatar_md5_hash == "9226b343e6fe53b64aa8b06b3f4c2f19":
        osu_avatar = avatar_guest
    else:
        osu_avatar = f"https://a.ppy.sh/{osu_user_id}"

    embed = discord.Embed(color = discord.Colour.random(),description=score)
    embed.set_author(name=beatmap_title,url=f"https://osu.ppy.sh/s/{beatmapset_id}", icon_url = osu_creator_id_avatar)


    embed.set_thumbnail(url=beatmap_bg)
    embed.description = example
    await ctx.send(embed=embed)

bot.run(settings['token']) 

from discord.ext import commands
from config import settings
from time import strftime
from time import gmtime
from mods import *
import requests
import discord
import hashlib
import mods

avatar_guest = "https://osu.ppy.sh/images/layout/avatar-guest.png"

bot = commands.Bot(command_prefix = settings['prefix'])
osu_api_key = settings['osu_api_key']

@bot.event
async def on_ready():
    print('------')
    print(f'Logged in as {bot.user.name}')
    print('------')

@bot.command() # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def hello(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.

    await ctx.send(f'Hello, {author.mention}!') # Выводим сообщение с упоминанием автора, обращаясь к переменной author.
    await ctx.message.delete()

@bot.command()
async def help_me(ctx):
    author = ctx.message.author

    await ctx.send(f'Hi, {author.mention}!')
    helpa = """
    Wink - Returns a wink PNG / GIF  
    Help_Me - Sends this message 
    Osu - shows your osu!bancho stats 
    Map - shows osu!bancho map stats
    """
    embed = discord.Embed(color=discord.Colour.random())
    embed.set_author(name=helpa, icon_url="https://a.ppy.sh/10081838")

    embed.set_thumbnail(url="https://a.ppy.sh/10081838")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@bot.command()
async def wink(ctx):
	response = requests.get('https://some-random-api.ml/animu/wink')
	json_data = response.json()

	embed = discord.Embed(color=discord.Colour.random(), title = 'Some wink')
	embed.set_image(url=json_data['link'])
	await ctx.send(embed=embed)
	await ctx.message.delete()

@bot.command()
async def osu(ctx, user_arg):    
    
    response = requests.get(f"https://osu.ppy.sh/api/get_user?k={osu_api_key}&u={user_arg}")
    resp = response.json()

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
    embed.add_field(name="▸PP", value=(round(float(pp_raw))), inline=True)
    embed.add_field(name="▸Level", value=(round(float(level))), inline=True)
    embed.add_field(name="▸Accuracy", value=(round(float((accuracy)))), inline=True)
    embed.add_field(name="▸Playcount", value=(int(float(playcount))), inline=True)
    embed.description = osu
    await ctx.send(embed = embed)

@bot.command()
async def kurikku(ctx, user_arg): # only work with id 
    json_data = requests.get(f"https://kurikku.pw/api/v1/users/full?id={user_arg}").json()

    try:
      json_data
    except IndexError:
      return await ctx.send("Uh oh user not found!")
  
    osu_username = json_data["username"]
    osu_user_id = json_data["id"]
    osu_country_acronym = json_data["country"]
    osu_user_country = f"https://osu.ppy.sh/images/flags/{osu_country_acronym}.png"
    playcount = json_data["std"]["playcount"]
    pp = json_data["std"]["pp"]
    level = json_data["std"]["level"]
    accuracy = json_data["std"]["accuracy"]

    avatar_request = requests.get(f"https://a.kurikku.pw/{osu_user_id}")
    avatar_response = avatar_request.text

    hash_object = hashlib.md5(avatar_response.encode())
    avatar_md5_hash = hash_object.hexdigest()

    if avatar_md5_hash == "9226b343e6fe53b64aa8b06b3f4c2f19":
        osu_avatar = avatar_guest
    else:
        osu_avatar = f"https://a.kurikku.pw/{osu_user_id}" 

    osu = """"""

    title = f'osu! Kurikku Profile for {osu_username}'    
    embed = discord.Embed(color=discord.Colour.random(), description=osu_username)
    embed.set_author(name=title, icon_url = osu_user_country)
    embed.set_thumbnail(url=osu_avatar)
    embed.add_field(name="▸PP", value=(round(float(pp))), inline=True)
    embed.add_field(name="▸Level", value=(round(float(level))), inline=True)
    embed.add_field(name="▸Accuracy", value=(round(float((accuracy)))), inline=True)
    embed.add_field(name="▸Playcount", value=(int(float(playcount))), inline=True)
    embed.description = osu
    await ctx.send(embed = embed)

@bot.command()
async def maplistk(ctx, beatmap_arg): # number 1 from beatmap, only work with beatmap id
    json_data = requests.get(f"https://kurikku.pw/api/v1/scores?b={beatmap_arg}&l=1").json()
    try:
      json_data
    except IndexError:
      return await ctx.send("Uh oh user not found!")

    try: 
        code = json_data["code"]
        print(code)
        scores = json_data["scores"][0]
        score = json_data["scores"][0]["score"]
        max_combo = json_data["scores"][0]["max_combo"]
        count_300 = json_data["scores"][0]["count_300"]
        count_100 = json_data["scores"][0]["count_100"]
        count_50 = json_data["scores"][0]["count_50"]
        count_miss = json_data["scores"][0]["count_miss"]
        accuracy = json_data["scores"][0]["accuracy"]
        pp = json_data["scores"][0]["pp"]
        rank = json_data["scores"][0]["rank"]
        username = json_data["scores"][0]["user"]["username"]
        time = json_data["scores"][0]["time"]
    except:
        return await ctx.send("Sorry, error uwu")

    example = """
    """
    userid = requests.get(f"https://kurikku.pw/api/v1/users/whatid?name={username}").json()

    embed = discord.Embed(color=discord.Colour.random(), description=code)
    embed.set_author(name=username, url=f"https://kurikku.pw/u/{username}")
    embed.add_field(name="▸Username", value=username, inline=True)
    embed.add_field(name="▸Score", value=score, inline=True)
    embed.add_field(name="▸PP", value=pp, inline=True)
    embed.add_field(name="▸Rank", value=rank, inline=True)
    embed.add_field(name="▸Max combo", value=max_combo, inline=True)
    embed.add_field(name="▸300", value=count_300, inline=True)
    embed.add_field(name="▸100", value=count_100, inline=True)
    embed.add_field(name="▸50", value=count_50, inline=True)
    embed.add_field(name="▸Miss", value=count_miss, inline=True)
    embed.add_field(name="▸Date", value=time, inline=True)
    embed.set_thumbnail(url=f"https://a.kurikku.pw/{userid['id']}")
    embed.description = "Idk wtf is that"
    await ctx.send(embed=embed)

@bot.command()
async def map(ctx, beatmap_arg):
    response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={osu_api_key}&s={beatmap_arg}")
    resp = response.json()

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
        time = strftime("Length: **%H:%M:%S**", gmtime(total_length))
    else:
        time = strftime("Length: **%M:%S**", gmtime(total_length))


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
async def recent(ctx, user_arg, beatmap_arg): # WIP
    response = requests.get(f"https://osu.ppy.sh/api/get_user_recent?k={osu_api_key}&u={user_arg}")
    response = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={osu_api_key}&s={beatmap_arg}")
    resp = response.json()

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

@bot.command()
async def top(ctx, user_arg):
    response = requests.get(f"https://osu.ppy.sh/api/get_user_best?k={osu_api_key}&u={user_arg}&limit=1")
    resp = response.json()

    try:
        give_me_json = resp[0]
    except IndexError:
        return await ctx.send("Can't find user top play!")

    osu_user_id = give_me_json["user_id"]
    avatar_request = requests.get(f"https://a.ppy.sh/{osu_user_id}")
    avatar_response = avatar_request.text
    beatmap_id = give_me_json["beatmap_id"]
    score = give_me_json["score"]
    maxcombo = give_me_json["maxcombo"]
    beatmap_bg = f"https://b.ppy.sh/thumb/{beatmap_id}.jpg"
    count50 = give_me_json["count50"]
    count100 = give_me_json["count100"]
    count300 = give_me_json["count300"]
    countmiss = give_me_json["countmiss"]
    enabled_mods = give_me_json["enabled_mods"]
    rank = give_me_json["rank"]
    pp_play = give_me_json["pp"]

    hash_object = hashlib.md5(avatar_response.encode())
    avatar_md5_hash = hash_object.hexdigest()

    if avatar_md5_hash == "9226b343e6fe53b64aa8b06b3f4c2f19":
        osu_avatar = avatar_guest
    else:
        osu_avatar = f"https://a.ppy.sh/{osu_user_id}"

    score_mods = ""
    if enabled_mods == 0:
        score_mods += "NM"
    if enabled_mods & mods.NOFAIL > 0:
        score_mods += "NF"
    if enabled_mods & mods.EASY > 0:
        score_mods += "EZ"
    if enabled_mods & mods.HIDDEN > 0:
        score_mods += "HD"
    if enabled_mods & mods.HARDROCK > 0:
        score_mods += "HR"
    if enabled_mods & mods.DOUBLETIME > 0:
        score_mods += "DT"
    if enabled_mods & mods.HALFTIME > 0:
        score_mods += "HT"
    if enabled_mods & mods.FLASHLIGHT > 0:
        score_mods += "FL"
    if enabled_mods & mods.SPUNOUT > 0:
        score_mods += "SO"
    if enabled_mods & mods.TOUCHSCREEN > 0:
        score_mods += "TD"
    if enabled_mods & mods.RELAX > 0:
        score_mods += "RX"
    if enabled_mods & mods.RELAX2 > 0:
        score_mods += "AP"

    print(score_mods)

    osu = """
    Weird way to dispay this :o"""

    title = f'osu! TopPlay Score for {osu_user_id}'    
    embed = discord.Embed(color = discord.Colour.random(),description=f"Why did i do that...")
    embed.set_author(name=title, url=f"https://osu.ppy.sh/u/{osu_user_id}", icon_url = osu_avatar)
    embed.set_thumbnail(url=beatmap_bg)
    embed.add_field(name="▸PP", value=(round(int(float(pp_play)))), inline=True)
    embed.add_field(name="▸300", value=(round(int(float(count300)))), inline=True)
    embed.add_field(name="▸100", value=(int(float((count100)))), inline=True)
    embed.add_field(name="▸50", value=(round(int(float(count50)))), inline=True)
    embed.add_field(name="▸MODS", value=score_mods, inline=True)
    embed.description = osu
    await ctx.send(embed = embed)

bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена

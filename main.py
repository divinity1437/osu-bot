from discord.ext import commands
from config import settings
from time import strftime
from time import gmtime
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

@bot.command()
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')

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
    json_data = requests.get(f"https://osu.ppy.sh/api/get_user?k={osu_api_key}&u={user_arg}").json()

    try:
      json_data
    except IndexError:
      return await ctx.send("Uh oh user not found!")

    osu_username =json_data[0]["username"]
    osu_user_id =json_data[0]["user_id"]
    osu_country_acronym =json_data[0]["country"]
    osu_user_country = f"https://osu.ppy.sh/images/flags/{osu_country_acronym}.png"
    playcount =json_data[0]["playcount"]
    pp_raw =json_data[0]["pp_raw"]
    level =json_data[0]["level"]
    accuracy =json_data[0]["accuracy"]
    count_rank_ss =json_data[0]["count_rank_ss"]
    count_rank_s =json_data[0]["count_rank_s"]
    count_rank_sh =json_data[0]["count_rank_sh"]
    count_rank_a =json_data[0]["count_rank_a"]

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

@bot.command()
async def kurikku(ctx, user_arg): # only work with id 
    json_data = requests.get(f"https://kurikku.pw/api/v1/users/full?id={user_arg}").json()

    try:
      json_data
    except IndexError:
      return await ctx.send("Uh oh user not found!")

    if json_data["code"] == 404:
        return await ctx.send("User disabled/restricted/not exists!")
    else:
        osu_user_id = json_data["id"]
        osu_username = json_data["username"]
        osu_country_acronym = json_data["country"]
        osu_user_country = f"https://osu.ppy.sh/images/flags/{osu_country_acronym}.png"
        playcount = json_data["std"]["playcount"]
        pp = json_data["std"]["pp"]
        level = json_data["std"]["level"]
        accuracy = json_data["std"]["accuracy"]
        osu_avatar = f"https://a.kurikku.pw/{osu_user_id}"

    title = f'osu! Kurikku Profile for {osu_username}'    
    embed = discord.Embed(color = discord.Colour.random(),description=f"**▸PP:** {round(float(pp),2)}\n**▸Level:** {round(float(level),2)}\n**▸Accuracy:** {round(float(accuracy),2)}\n**▸Playcount:** {playcount}")
    embed.set_author(name=title, url=f"https://kurikku.pw/u/{osu_user_id}", icon_url = osu_user_country)
    embed.set_thumbnail(url=osu_avatar)
    await ctx.send(embed = embed)

@bot.command()
async def kmapleader(ctx, beatmap_arg): # number 1 from beatmap, only work with beatmap id / WIP!!!!!!!!!!!!
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
        mods = json_data["scores"][0]["mods"]
        pp = json_data["scores"][0]["pp"]
        rank = json_data["scores"][0]["rank"]
        username = json_data["scores"][0]["user"]["username"]
        time = json_data["scores"][0]["time"]
    except:
        return await ctx.send("Sorry, error appeared!")

    userid = requests.get(f"https://kurikku.pw/api/v1/users/whatid?name={username}").json()

    score_mods = ""
    if mods == 0:
        score_mods += "NM"
    if mods & mods.NOFAIL > 0:
        score_mods += "NF"
    if mods & mods.EASY > 0:
        score_mods += "EZ"
    if mods & mods.HIDDEN > 0:
        score_mods += "HD"
    if mods & mods.HARDROCK > 0:
        score_mods += "HR"
    if mods & mods.DOUBLETIME > 0:
        score_mods += "DT"
    if mods & mods.HALFTIME > 0:
        score_mods += "HT"
    if mods & mods.FLASHLIGHT > 0:
        score_mods += "FL"
    if mods & mods.SPUNOUT > 0:
        score_mods += "SO"
    if mods & mods.TOUCHSCREEN > 0:
        score_mods += "TD"
    if mods & mods.RELAX > 0:
        score_mods += "RX"
    if mods & mods.RELAX2 > 0:
        score_mods += "AP"

    print(score_mods)

    embed = discord.Embed(color=discord.Colour.random(), description=f"**▸Username:** {username}\n**▸Score:** {score}\n**▸PP:** {pp}\n**▸Accuracy:** {accuracy}\n**▸Max combo:** {max_combo}\n**▸Rank:** {rank}\n**▸300:** {count_300} **▸100:** {count_100} **▸50:** {count_50} **▸Miss:** {count_miss}")
    embed.set_author(name=username, url=f"https://kurikku.pw/u/{userid['id']}")
    embed.set_footer(text=time)
    embed.set_thumbnail(url=f"https://a.kurikku.pw/{userid['id']}")
    await ctx.send(embed=embed)

@bot.command()
async def map(ctx, beatmap_arg):
    json_data = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={osu_api_key}&s={beatmap_arg}").json()

    try:
        json_data
    except IndexError:
        return await ctx.send("Beatmap not found!")

    beatmapset_id = json_data[0]["beatmapset_id"]
    beatmap_artist = json_data[0]["artist"]
    beatmap_title = json_data[0]["title"]
    beatmap_bpm = json_data[0]["bpm"]
    creator_id = json_data[0]["creator_id"]
    osu_creator_id_avatar = f"https://a.ppy.sh/{creator_id}"
    beatmap_bg = f"https://b.ppy.sh/thumb/{beatmapset_id}.jpg"
    difficultyrating = float(json_data[0]["difficultyrating"])
    total_length = int(json_data[0]["total_length"])
    diff_size = json_data[0]["diff_size"] # cs
    diff_overall = json_data[0]["diff_overall"] # od
    diff_approach = json_data[0]["diff_approach"] # ar 
    diff_drain = json_data[0]["diff_drain"] # hp
    max_combo = json_data[0]["max_combo"]

    if total_length >= 3600:
        time = strftime("%H:%M:%S", gmtime(total_length))
    else:
        time = strftime("%M:%S", gmtime(total_length))


    embed = discord.Embed(color = discord.Colour.random(),description=f"**▸Difficulty:** {(round(float(difficultyrating),2))} **▸Max combo:** {max_combo}\n**▸AR:** {diff_approach} **▸OD:** {diff_overall} **▸HP:** {diff_drain} **▸CS:** {diff_size}\n **▸BPM:** {beatmap_bpm} **▸Length:** {time}")
    embed.set_author(name=beatmap_title,url=f"https://osu.ppy.sh/s/{beatmapset_id}", icon_url = osu_creator_id_avatar)
    embed.set_thumbnail(url=beatmap_bg)
    await ctx.send(embed=embed)

@bot.command()
async def recent(ctx, user_arg): # no WIP anymore hell yea
    json_data = requests.get(f"https://osu.ppy.sh/api/get_user_recent?k={osu_api_key}&u={user_arg}").json()

    try:
        json_data
    except IndexError:
        return await ctx.send("Can't find recent play!") 
    try:
        osu_username = requests.get(f"https://osu.ppy.sh/api/get_user?k={osu_api_key}&u={user_arg}").json()
        osu_user_id = json_data[0]["user_id"]
        beatmap_id = json_data[0]["beatmap_id"]
        beatmap_info = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={osu_api_key}&b={beatmap_id}").json()
        beatmap_title = beatmap_info[0]["title"]
        avatar_request = requests.get(f"https://a.ppy.sh/{osu_user_id}")
        osu_creator_id_avatar = beatmap_info[0]["creator_id"]
        avatar_response = avatar_request.text
        beatmap_bg = f"https://b.ppy.sh/thumb/{beatmap_info[0]['beatmapset_id']}.jpg"
        difficultyrating = beatmap_info[0]["difficultyrating"]
        score = json_data[0]["score"]
        maxcombo = beatmap_info[0]["max_combo"]
        user_combo = json_data[0]["maxcombo"]
        countmiss = json_data[0]["countmiss"]
        count300 = json_data[0]["count300"]
        count100 = json_data[0]["count100"]
        count50 = json_data[0]["count50"]
        countmiss = json_data[0]["countmiss"]
        rank = json_data[0]["rank"]
        time = json_data[0]["date"]
    except IndexError:
        return await ctx.send(f"Can't find {osu_username[0]['username']} recent play!")

    hash_object = hashlib.md5(avatar_response.encode())
    avatar_md5_hash = hash_object.hexdigest()

    if avatar_md5_hash == "9226b343e6fe53b64aa8b06b3f4c2f19":
        osu_avatar = avatar_guest
    else:
        osu_avatar = f"https://a.ppy.sh/{osu_user_id}"

    embed = discord.Embed(color = discord.Colour.random(),description=f"▸**{rank}**\n **▸{score}**\n**▸**x{user_combo}/{maxcombo} **[{count300}/{count100}/{count50}/{countmiss}]**")
    embed.set_footer(text=time)
    embed.set_author(name=beatmap_title,url=f"https://osu.ppy.sh/b/{beatmap_id}", icon_url=f"https://a.ppy.sh/{osu_user_id}")
    embed.set_thumbnail(url=beatmap_bg)
    await ctx.send(embed=embed)

@bot.command()
async def top(ctx, user_arg):
    json_data = requests.get(f"https://osu.ppy.sh/api/get_user_best?k={osu_api_key}&u={user_arg}&limit=5").json()

    try:
        json_data
    except IndexError:
        return await ctx.send("Can't find user top play!")

    user_api = requests.get(f"https://osu.ppy.sh/api/get_user?k={osu_api_key}&u={user_arg}").json()
    beatmap_id = json_data[0]["beatmap_id"]
    beatmap_info = requests.get(f"https://osu.ppy.sh/api/get_beatmaps?k={osu_api_key}&b={beatmap_id}").json()
    osu_user_id = user_api[0]["user_id"]
    avatar_request = requests.get(f"https://a.ppy.sh/{osu_user_id}")
    avatar_response = avatar_request.text
    score = json_data[0]["score"]
    title = beatmap_info[0]["title"]
    user_combo = json_data[0]["maxcombo"]
    difficultyrating = float(beatmap_info[0]["difficultyrating"])
    max_combo = beatmap_info[0]["max_combo"]
    count50 = json_data[0]["count50"]
    count100 = json_data[0]["count100"]
    count300 = json_data[0]["count300"]
    countmiss = json_data[0]["countmiss"]
    enabled_mods = json_data[0]["enabled_mods"]
    rank = json_data[0]["rank"]
    pp_play = float(json_data[0]["pp"])
    date = json_data[0]["date"]
    osu_country_acronym = requests.get(f"https://osu.ppy.sh/api/get_user?k={osu_api_key}&u={user_arg}").json()
    osu_user_country = f"https://osu.ppy.sh/images/flags/{osu_country_acronym[0]['country']}.png"

    hash_object = hashlib.md5(avatar_response.encode())
    avatar_md5_hash = hash_object.hexdigest()

    if avatar_md5_hash == "9226b343e6fe53b64aa8b06b3f4c2f19":
        osu_avatar = avatar_guest
    else:
        osu_avatar = f"https://a.ppy.sh/{osu_user_id}"

    score_mods = ""
    if int(enabled_mods) == 0:
        score_mods += "NM"
    if int(enabled_mods) & mods.NOFAIL > 0:
        score_mods += "NF"
    if int(enabled_mods) & mods.EASY > 0:
        score_mods += "EZ"
    if int(enabled_mods) & mods.HIDDEN > 0:
        score_mods += "HD"
    if int(enabled_mods) & mods.HARDROCK > 0:
        score_mods += "HR"
    if int(enabled_mods) & mods.DOUBLETIME > 0:
        score_mods += "DT"
    if int(enabled_mods) & mods.HALFTIME > 0:
        score_mods += "HT"
    if int(enabled_mods) & mods.FLASHLIGHT > 0:
        score_mods += "FL"
    if int(enabled_mods) & mods.SPUNOUT > 0:
        score_mods += "SO"
    if int(enabled_mods) & mods.TOUCHSCREEN > 0:
        score_mods += "TD"
    if int(enabled_mods) & mods.RELAX > 0:
        score_mods += "RX"
    if int(enabled_mods) & mods.RELAX2 > 0:
        score_mods += "AP"

    print(f"used top command")

    title = (f"osu! Top Play Score for {user_api[0]['username']}")
    embed = discord.Embed(color = discord.Colour.random(),description=f"**#1** https://osu.ppy.sh/b/{beatmap_id} +**{score_mods}** [{round(float(difficultyrating),2)}]\n**▸**{rank} **{round(float(pp_play),1)}PP**\n**▸**{score} **▸**x{user_combo}/{max_combo} **▸** [{count300}/{count100}/{count50}/{countmiss}]\n{date}")
    embed.set_author(name=title, url=f"https://osu.ppy.sh/{osu_user_id}", icon_url = osu_user_country)
    embed.set_thumbnail(url=osu_avatar)
    await ctx.send(embed = embed)


bot.run(settings['token'])

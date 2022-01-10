from discord.ext import commands
from cmyui.mysql import AsyncSQLPool
from config import settings
from time import strftime
from time import gmtime

import requests
import discord
import hashlib
import mods
import glob
import os


bot = commands.Bot(command_prefix = settings['prefix'])
glob.db = AsyncSQLPool()
cogs_count = 0

for f in os.listdir("./cogs"):
    if f.endswith(".py"):
        cogs_count += 1
        bot.load_extension("cogs." + f[:-3])

@bot.event
async def on_ready():

    activity = discord.Game(name=".help", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    await glob.db.connect(glob.config.sql)

    print('  ____            ____                      ')
    print(' / __ \          / __ \                     ')
    print('| |  | |_      _| |  | |_   _ ___  ___ _ __ ')
    print('| |  | \ \ /\ / / |  | | | | / __|/ _ \ __| ')
    print('| |__| |\ V  V /| |__| | |_| \__ \  __/ |   ')
    print(' \____/  \_/\_/  \____/ \__,_|___/\___|_|   ')

    print('------')
    print(f'Logged in as {bot.user.name} with {cogs_count} cogs.')
    print('------')

bot.run(settings['token'])
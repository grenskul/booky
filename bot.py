import discord
from discord.ext import commands
import datetime
import asyncio
import glob
import os
import requests
import json

from urllib import parse, request
import re

Intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', description="This is a Fic Grabber Bot", intents=Intents)

@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send('pong')


@bot.command()
async def dl(ctx, *, url):
    await ctx.message.delete()
    user = ctx.author
    await user.send("Story has started downloading.")

    result = await run_command_shell('cd html/ficsbot/fics; fanficfare '+url);


    check = " already contains"

    if check in result:

        partial_filename = result.split('.epub')[0]
        partial_filename = partial_filename.replace('Updating ', '');
        latest_file = 'html/ficsbot/fics/'+partial_filename+'.epub'
        latest_story = parse.quote(latest_file.replace('/var/www/html/ficsbot', 'myurl.com'))
        temp_filename = latest_file.replace('html/ficsbot/fics', '');

    else:

        list_of_files = [
            f for f in glob.glob('html/ficsbot/fics/*')
            if os.path.isfile(f)
        ]
        if not list_of_files:
            await user.send("didn't work, try again or contact grenskul")
            return

        latest_file = max(list_of_files, key=os.path.getctime);
        latest_story = parse.quote(latest_file.replace('html/ficsbot', 'myurl.com'));
        temp_filename = latest_file.replace('html/ficsbot/fics', '');

    statinfo = os.stat(latest_file);

    if statinfo.st_size < 8388608:

      file = discord.File(latest_file, filename=temp_filename);

      await user.send('Finished Converting!');
      await user.send(file=file);

    else:
        epu = open(latest_file, "rb")
        apiurl = os.getenv('api_url')
        headers = {"accept": "application/json", "apikey": os.getenv('api_key')}
        data = {"allowedDownloads":"10", "expiryDays": "5"}
        files = {"file": (latest_file ,epu ,"application/octet-stream")}
        response = requests.post(apiurl, headers=headers,data = data, files=files)
        var2 = response.json()
        await user.send('Finished Converting:'+"   "+var2["Url"]+var2['FileInfo']["Id"]+'    \n'+var2['FileInfo']["Name"]);



# Events
@bot.event
async def on_ready():
    game = discord.Game("with Fanfics")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print('Bot has started')

async def run_command_shell(command):

    # Create subprocess
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    # Status
    print("Started:", command, "(pid = " + str(process.pid) + ")", flush=True)

    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()

    # Progress
    if process.returncode == 0:
        print("Done:", command, "(pid = " + str(process.pid) + ")", flush=True)
    else:
        print(
            "Failed:", command, "(pid = " + str(process.pid) + ")", flush=True
        )

    # Result
    result = stdout.decode().strip()

    # Return stdout
    return result

bot.run(os.getenv('discord_token'))


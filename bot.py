from importlib.resources import path
import discord
from discord.ext import commands, tasks
import requests
import os
from os import system
import subprocess
import shutil
from flask import Flask
from threading import Thread
from itertools import cycle

app = Flask('')

@app.route('/')
def main():
    return "Your Bot Is Ready"

def run():
    app.run(host="0.0.0.0", port=8000)
    
def keep_alive():
    server = Thread(target=run)
    server.start()
 
# make sure you add discord bot token in secret environment variables with a key named DISCORD_TOKEN
token = os.environ['DISCORD_TOKEN']
# channel id of the channel you want the bot obfuscate in. 
# with developer settings enabled right click channel and copy id. (bot works in direct messages as well)
channel_id = 985608627723337768

bot = commands.Bot(command_prefix="!")
bot.remove_command("help")


def obfuscation(path, author):
    copy = f".//obfuscated//{author}.lua"

    #removing duplicates
    if os.path.exists(copy):
        os.remove(copy)

    #copying uploaded one to make operations on it
    shutil.copyfile(path, copy)

    #copying obfuscate file to copied one
    text_file = open(f".//obfuscate.lua", "r")
    data = text_file.read()
    text_file.close()
    f = open(copy, "a")
    f.truncate(0)
    f.write(data)
    f.close()

    #writing upload file into obfuscation script
    originalupload = open(path, "r")
    originalupload_data = originalupload.read()
    originalupload.close()

    with open(copy, "r") as in_file:
        buf = in_file.readlines()

    with open(copy, "w") as out_file:
        for line in buf:
            if line == "--SCRIPT\n":
                line = line + originalupload_data + '\n'
            out_file.write(line)

    #executing script and making new file with obfuscated output
    output = subprocess.getoutput(f'bin/luvit {copy}')

    if os.path.exists(f".//obfuscated//{author}-obfuscated.lua"):
        os.remove(f".//obfuscated//{author}-obfuscated.lua")

    f = open(f".//obfuscated//{author}-obfuscated.lua", "a")
    f.write(output)
    f.close()

    os.remove(copy)


status = cycle([
    'for .lua files to obfuscate.', 'for .lua files to obfuscate..',
    'for .lua files to obfuscate...'
])


@bot.event
async def on_ready():
    change_status.start()
    print(f"{bot.user} is online ✔️")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                                  type=discord.ActivityType.watching,
                                  name=next(status)))


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(
                                  type=discord.ActivityType.watching,
                                  name=next(status)))


@bot.event
async def on_message(message):
    channel = str(message.channel)
    author = str(message.author)
    channel = bot.get_channel(channel_id)

    try:
        url = message.attachments[0].url
        if not message.author.bot:
            #if message.channel.id == channel_id:
            if message.channel.type is discord.ChannelType.private:
                if message.attachments[0].url:
                    if '.lua' not in url:
                        embed = discord.Embed(
                            title=f"***Wrong file extension!***",
                            description=f"only ``.lua`` allowed",
                            color=0xFF3357)
                        message = await channel.send(embed=embed)
                        dm = await message.author.create_dm()
                        await dm.send(embed=embed)
                    else:
                        uploads_dir = f".//uploads//"
                        obfuscated_dir = f".//obfuscated//"

                        if not os.path.exists(uploads_dir):
                            os.makedirs(uploads_dir)
                        if not os.path.exists(obfuscated_dir):
                            os.makedirs(obfuscated_dir)

                        print(f'\nNew lua script received from {author}.')
                        print(
                            f'Attachment Link: {message.attachments[0].url}\n')
                        response = requests.get(url)
                        path = f".//uploads//{author}.lua"

                        if os.path.exists(path):
                            os.remove(path)

                        open(path, "wb").write(response.content)
                        obfuscation(path, author)
                        embed = discord.Embed(title="File has been obfuscated",
                                              color=0x3357FF)
                        dm = await message.author.create_dm()
                        await dm.send(
                            embed=embed,
                            file=discord.File(
                                f".//obfuscated//{author}-obfuscated.lua"))
            if message.channel.id == channel_id:
                if message.attachments[0].url:
                    if '.lua' not in url:
                        embed = discord.Embed(
                            title=f"***Wrong file extension!***",
                            description=f"only ``.lua`` allowed",
                            color=0xFF3357)
                        message = await channel.send(embed=embed)
                        dm = await message.author.create_dm()
                        await dm.send(embed=embed)
                    else:
                        uploads_dir = f".//uploads//"
                        obfuscated_dir = f".//obfuscated//"

                        if not os.path.exists(uploads_dir):
                            os.makedirs(uploads_dir)
                        if not os.path.exists(obfuscated_dir):
                            os.makedirs(obfuscated_dir)

                        print(f'\nNew lua script received from {author}.')
                        print(
                            f'Attachment Link: {message.attachments[0].url}\n')
                        response = requests.get(url)
                        path = f".//uploads//{author}.lua"

                        if os.path.exists(path):
                            os.remove(path)

                        open(path, "wb").write(response.content)
                        obfuscation(path, author)
                        embed = discord.Embed(title="File has been obfuscated",
                                              color=0x3357FF)
                        await channel.send(
                            embed=embed,
                            file=discord.File(
                                f".//obfuscated//{author}-obfuscated.lua"))
    except:
        pass


bot.run(token)

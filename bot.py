import os
from PIL import Image 
import PIL
import discord
from dotenv import load_dotenv
import requests
import json


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
baseulr="https://cdn.betterttv.net/emote/"


with open('emotes.json') as f:
    bttvemotes = json.load(f)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if ('Bot' in message.content or 'bot' in message.content) and ('yetki' in message.content or 'Yetki' in message.content):
        await message.channel.send("Ne zannettin?")
        response=baseulr+bttvemotes["EZ"]+"/3x"
        with open('temp.gif','wb') as f:
            f.write(requests.get(response).content)
            
        await message.channel.send(file=discord.File("temp.gif"))
        os.remove("C:\\Users\Furka\Desktop\DiscordBot/temp.gif")

    if message.content.startswith('bttvadd'):
        if message.content.split()[1] in bttvemotes:
            await message.channel.send("This emote already exists")
        else:
            updatedic= {message.content.split()[1]:message.content.split()[2]}
            bttvemotes.update(updatedic)
            updatejson=json.dumps(bttvemotes)
            with open('emotes.json', 'w') as json_file:
                json.dump(bttvemotes, json_file)
            await message.channel.send("Emote added")

    if message.content in bttvemotes:
        response=baseulr+bttvemotes[message.content]+"/3x"
        with open('temp.gif','wb') as f:
            f.write(requests.get(response).content)
            
        await message.channel.send(file=discord.File("temp.gif"))
        os.remove("C:\\Users\Furka\Desktop\DiscordBot/temp.gif")

client.run(TOKEN)
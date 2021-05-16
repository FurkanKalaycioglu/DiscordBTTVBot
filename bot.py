import os
import discord
from dotenv import load_dotenv
import requests
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
prefix='=<'
client = discord.Client()
baseulr="https://cdn.betterttv.net/emote/"
with open('emotes.json') as f:
    bttvemotes = json.load(f)

commands={'add','remove','emotelist'}
async def add_emote(message):
    if message.content.split()[2] in bttvemotes:
        await message.channel.send("This emote already exists")
    else:
        #updatedic= {message.content.split()[2]:message.content.split()[3]}
        bttvemotes.update({message.content.split()[2]:message.content.split()[3]})
        updatejson=json.dumps(bttvemotes)
        with open('emotes.json', 'w') as json_file:
            json.dump(bttvemotes, json_file)
        await message.channel.send("Emote added")

async def send_emote(message):
    response=baseulr+bttvemotes[message.content]+"/3x"
    with open('temp.gif','wb') as f:
        f.write(requests.get(response).content)
    await message.channel.send(file=discord.File("temp.gif"))
    os.remove("temp.gif")

async def remove_emote(message):
    if message.content.split()[2] in bttvemotes:
        bttvemotes.pop(message.content.split()[2])
        updatejson=json.dumps(bttvemotes)
        with open('emotes.json','w') as json_file:
            json.dump(bttvemotes,json_file)
        await message.channel.send('Emote removed')
    else:
        await message.channel.send("This emote doesn't exists")

async def emotes_list(message):
    await message.channel.send("Emotes:")
    output=''.join((keys +', ')for keys in bttvemotes)
    await message.channel.send(output)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix):
        if message.content.split()[1] == 'add':
            await add_emote(message)
        if message.content.split()[1] == 'remove':
            await remove_emote(message)
        if message.content.split()[1] == 'emotelist':
            await emotes_list(message)
        if message.content.split()[1] not in commands:
            await message.channel.send('That command doesn\'t exist.')
            await message.channel.send("Commands:")
            output=''.join((command + ' ')for command in commands)
            await message.channel.send(output)

    if message.content in bttvemotes:
        await send_emote(message)

client.run(TOKEN)
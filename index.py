import pandas as pd
import pathlib
import json
import discord
from discord.ext import commands
from discord.ui import Button , View, Select
from discord import app_commands
import threading
import Myview
import requests
import datetime
import nacl

path = pathlib.Path(__file__).parent.absolute()


with open(str(path)+'/env.json') as f:
    appData = json.load(f)

CLIENT_ID = appData['CLIENT_ID']
GUILD_ID = appData['GUILD_ID']
TOKEN=appData['TOKEN']

re_list=[]
embed = discord.Embed()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(intents=intents,command_prefix='!')



#####slash command
@tree.command(name="ping",description='Replies with Pong',guild=discord.Object(id=GUILD_ID))
async def ping(interaction):
    await interaction.response.send_message("Pong")
@tree.command(name="hello",description='Replies with hello',guild=discord.Object(id=GUILD_ID))
async def hello(interaction):
    await interaction.response.send_message("hello")/ㄥ
@tree.command(name="leave",description="call leave form",guild=discord.Object(id=GUILD_ID))
async def leave(interaction):
    await interaction.response.send_modal(Myview.leavemodal())
@tree.command(name="menu",description='call menu',guild=discord.Object(id=GUILD_ID))
async def interface(interaction):   
    view = Myview.menu()
    
    await interaction.response.send_message(view=view,ephemeral=True) ### ephmeral =只有自己看得到
    
#########

####bot 
@bot.command(pass_context=True)
async def invite(ctx):
        
        channel = ctx.author.voice.channel
        voice =await channel.connect()
       
        print(type(voice))
        re_list.append(voice)
        return
  
@bot.command(pass_context=True)
async def leave(ctx):

        await ctx.voice_client.disconnect()
        re_list.pop()



#########


####client 


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))  ### 部屬 slash command

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    pass

#########



def client_run():
    client.run(TOKEN)
def bot_run():
    bot.run(TOKEN)

t1=threading.Thread(target=client_run)
#t2=threading.Thread(target=bot_run)

t1.start()
#t2.start()


t1.join()
#t2.join()
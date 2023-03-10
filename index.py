import datetime
import threading

import discord
from discord import app_commands
from discord.ext import commands

import Myview
from api import database, sysini
from config import ConfigParser

CLIENT_ID = ConfigParser()["appData"]["CLIENT_ID"]
GUILD_ID = ConfigParser()["appData"]["GUILD_ID"]
TOKEN = ConfigParser()["appData"]["TOKEN"]

"""
# 本來用來做錄音 但是沒有成功 現在沒有用
re_list = []
embed = discord.Embed()

# 設定client intents
intents = discord.Intents.default()
intents.message_content = True  ## 機器人會收到訊息內容
intents.members = True  ## 機器人會收到成員訊息


# 初始化改寫過的client  Myclient 繼承 discord.Client   ( type(Myclient) = type(discord.Client) )
client = Myview.MyClient(intents=intents)

# 建立指令樹 用來存放 slash command
tree = app_commands.CommandTree(client)

# 初始化bot (目前尚未有實際做用)  bot 主要用來控制 bot帳號本身的行為 (邀請加入語音頻道等等,發送訊息 大部分的功能都可以被client取代)
bot = commands.Bot(intents=intents, command_prefix="!")
"""

# slash command

# 測試用 輸入/ping 回復 pong
@sysini.tree.command(name="ping", description="Replies with Pong", guild=discord.Object(id=GUILD_ID))
async def ping(interaction):
    
    await interaction.response.send_message("Pong")

@sysini.tree.command(name='instock',description="insert stock company",guild=discord.Object(id=GUILD_ID))
async def stock(interaction: discord.Interaction,company: str):
    try:
        with database.dbopen("./database.db") as c:
            c.execute(f"insert into stock(company) values( \"{company}\" ) ")
        
        await interaction.response.send_message("存入成功",ephemeral=True)
    except:
        await interaction.response.send_message("格式錯誤",ephemeral=True)
    
    


# 測試用 輸入/hello 回復 hello
@sysini.tree.command(name="hello", description="Replies with hello", guild=discord.Object(id=GUILD_ID))
async def hello(interaction):
    await interaction.response.send_message("hello")

@sysini.tree.command(name='book',description='recommand book', guild=discord.Object(id=GUILD_ID))
async def book(interaction: discord.Interaction,cls: str ):
    id=interaction.channel_id
    ch=sysini.client.get_channel(id)
    await ch.send("test")
    pass
    ##list=booksearch(cls)
   # embed.set_thumbnail(url=)

@sysini.tree.command(name='login-schedual',description='login schedual', guild=discord.Object(id=GUILD_ID))
async def loginsche(intercation):
    await intercation.response.send_modal(Myview.updatesche())



# 呼叫功能選單 /menu 回傳功能選單
@sysini.tree.command(name="menu", description="call menu", guild=discord.Object(id=GUILD_ID))
async def interface(interaction):
    view = Myview.menu()

    await interaction.response.send_message(view=view, ephemeral=True)  # ephmeral = true 只有自己看得到


# bot (目前沒有實際用途)

# 邀請機器人加入語音頻道
@sysini.bot.command(pass_context=True)
async def invite(ctx):
    channel = ctx.author.voice.channel
    voice = await channel.connect()
    print(type(voice))
    return


# 機器人離開語音頻道
@sysini.bot.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()
    


##


# event

# client 啟動完成
@sysini.client.event
async def on_ready():
    sysini.client.checkleave.start()  # 執行定時任務
    await sysini.tree.sync(guild=discord.Object(id=GUILD_ID))  # 部屬 slash command


# 頻道內有人發送訊息
@sysini.client.event
async def on_message(message):
    if message.author == sysini.client.user:
        return

    today = datetime.datetime.now()

    if "@" in message.content:  ### 只讓有@的訊息進入迴圈@
        memberlist = []
        for i in sysini.client.guilds:
            if int(i.id) == int(GUILD_ID):
                memberlist = i.members

        for i in memberlist:
            if (f"@{i.id}") in str(message.content):  ### 如果訊息內有 @人名
                channellist = sysini.client.get_all_channels()
                for j in channellist:  # 找頻道
                    if j.name == "出缺勤":
                        channel = j
                        break
                with database.dbopen("./database.db") as c:  # 確認是否有請假
                    c.execute(f"select * from leave where name = {i.name} and year={today.year} and month={today.month} and day={today.day}")
                    out=c.fetchall()
                    if len(out) !=0:
                        await channel.send(f"{i.name} 今天已經請假了")
                        return
    pass


##


def client_run():
    sysini.client.run(TOKEN)


def bot_run():
    sysini.bot.run(TOKEN)


##t1 = threading.Thread(target=client_run)  # client thread
#t2=threading.Thread(target=bot_run)    # bot thread

#t1.start()
#t2.start()
client_run()
#t1.join()
#t2.join()

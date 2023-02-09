import datetime
import json
import pathlib
import threading

import discord
from discord import app_commands
from discord.ext import commands

import Myview

# 找到json檔案的路徑
path = pathlib.Path(__file__).parent.absolute()


# 讀取環境變數
with open(str(path) + "/env.json") as f:
    appData = json.load(f)


CLIENT_ID = appData["CLIENT_ID"]
GUILD_ID = appData["GUILD_ID"]
TOKEN = appData["TOKEN"]


# 本來用來做錄音 但是沒有成功 現在沒有用
re_list = []
#

# embed 物件初始化
embed = discord.Embed()

# 設定client intents
intents = discord.Intents.default()
intents.message_content = True

# 初始化改寫過的client  Myclient 繼承 discord.Client   ( type(Myclient) = type(discord.Client) )
client = Myview.MyClient(intents=intents)

# 建立指令樹 用來存放 slash command
tree = app_commands.CommandTree(client)

# 初始化bot (目前尚未有實際做用)  bot 主要用來控制 bot帳號本身的行為 (邀請加入語音頻道等等,發送訊息 大部分的功能都可以被client取代)
bot = commands.Bot(intents=intents, command_prefix="!")


# slash command

# 測試用 輸入/ping 回復 pong
@tree.command(name="ping", description="Replies with Pong", guild=discord.Object(id=GUILD_ID))
async def ping(interaction):
    await interaction.response.send_message("Pong")


# 測試用 輸入/hello 回復 hello
@tree.command(name="hello", description="Replies with hello", guild=discord.Object(id=GUILD_ID))
async def hello(interaction):
    await interaction.response.send_message("hello")


# 執行請假流程 輸入/leave 回傳請假表單
@tree.command(name="leave", description="call leave form", guild=discord.Object(id=GUILD_ID))
async def askleave(interaction):
    await interaction.response.send_modal(Myview.leavemodal())


# 查詢當日請假人員 輸入/checkleave 回傳當日請假人員
@tree.command(name="checkleave", description="check leave form", guild=discord.Object(id=GUILD_ID))
async def checkleave(interaction):
    leavelist = Myview.get_leve_list()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    for i in leavelist:
        if i["date"] == today:
            await interaction.response.send_message(f"姓名:{i['user']} \n日期:{i['date']} \n原因:{i['reason']}\n\n")


# 呼叫功能選單 /menu 回傳功能選單
@tree.command(name="menu", description="call menu", guild=discord.Object(id=GUILD_ID))
async def interface(interaction):
    view = Myview.menu()

    await interaction.response.send_message(view=view, ephemeral=True)  # ephmeral = true 只有自己看得到


# bot (目前沒有實際用途)

# 邀請機器人加入語音頻道
@bot.command(pass_context=True)
async def invite(ctx):
    channel = ctx.author.voice.channel
    voice = await channel.connect()
    print(type(voice))
    re_list.append(voice)
    return


# 機器人離開語音頻道
@bot.command(pass_context=True)
async def leave(ctx):
    await ctx.voice_client.disconnect()
    re_list.pop()


##


# event

# client 啟動完成
@client.event
async def on_ready():
    client.checkleave.start()  # 執行定時任務
    await tree.sync(guild=discord.Object(id=GUILD_ID))  # 部屬 slash command


# 頻道內有人發送訊息
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    pass


##


def client_run():
    client.run(TOKEN)


def bot_run():
    bot.run(TOKEN)


t1 = threading.Thread(target=client_run)  # client thread
# t2=threading.Thread(target=bot_run)    # bot thread

t1.start()
# t2.start()

t1.join()
# t2.join()

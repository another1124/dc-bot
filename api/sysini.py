
import datetime

import discord
from discord import app_commands
from discord.ext import commands, tasks

leavelist=[]
# 定義個人 Client
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    ##定時工作請假提醒
    @tasks.loop(hours=5)
    async def checkleave(self):
        print(leavelist)
        channellist = self.get_all_channels()
        for i in channellist:
            if i.name == "出缺勤":
                channel = i
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        if leavelist == []:
            return
        else:
            for i in leavelist:
                if i["date"] == today:
                    await channel.send(f"請假通知\n 姓名:{i['user']} \n日期:{i['date']} \n原因:{i['reason']}\n\n")

# 設定client intents
intents = discord.Intents.default()
intents.message_content = True  ## 機器人會收到訊息內容
intents.members = True  ## 機器人會收到成員訊息


# 初始化改寫過的client  Myclient 繼承 discord.Client   ( type(Myclient) = type(discord.Client) )
client = MyClient(intents=intents)

# 建立指令樹 用來存放 slash command
tree = app_commands.CommandTree(client)

# 初始化bot (目前尚未有實際做用)  bot 主要用來控制 bot帳號本身的行為 (邀請加入語音頻道等等,發送訊息 大部分的功能都可以被client取代)
bot = commands.Bot(intents=intents, command_prefix="!")
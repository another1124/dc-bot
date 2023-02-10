
import datetime

import discord
from discord import app_commands
from discord.ext import commands, tasks

from api import database

with database.dbopen("./database.db") as c:
    c.execute("CREATE TABLE IF NOT EXISTS leave(id auto_increment, name varchar(20), year int, month int ,day int ,reason varchar(200) ) ")



# 定義個人 Client
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    ##定時工作請假提醒
    @tasks.loop(hours=5)
    async def checkleave(self):
        today = datetime.datetime.now()
        with database.dbopen("./database.db") as c:  # 確認是否有請假
                c.execute(f"select * from leave where  year={today.year} and month={today.month} and day={today.day}")
                out=c.fetchall()

        channellist = self.get_all_channels()
        for i in channellist:
            if i.name == "出缺勤":
                channel = i
        for i in out:
            await channel.send(f"請假通知\n 姓名:{i[1]} \n日期:{i[2]}-{i[3]}-{i[4]} \n原因:{i[5]}\n\n")

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
import datetime
import random

import discord
from discord.ext import commands, tasks
from discord.ui import Button, Modal, Select, TextInput, View

import book2
import constellation1
import movie1
from api import database, sysini
from config import ConfigParser

embed = discord.Embed()


# 假單
class leavemodal(Modal, title="leave form"):
    def __init__(self):
        super().__init__()

    year = TextInput(
        label="year",
        style=discord.TextStyle.short,
        placeholder="title",
        default=datetime.datetime.now().year,
        required=True,
        max_length=4,
        row=0,
    )
    month = TextInput(
        label="month",
        style=discord.TextStyle.short,
        placeholder="title",
        default=datetime.datetime.now().month,
        required=True,
        max_length=2,
        row=1,
    )
    day = TextInput(
        label="day",
        style=discord.TextStyle.short,
        placeholder="title",
        default=datetime.datetime.now().day,
        required=True,
        max_length=2,
        row=2,
    )
    reason = TextInput(
        label="reason",
        style=discord.TextStyle.long,
        placeholder="title",
        default="None",
        required=True,
        max_length=50,
        row=3,
    )

    # 送出假單
    async def on_submit(self, interaction: discord.Interaction):
        try:
            with database.dbopen("./database.db") as c:
                c.execute(f"insert into leave(name , year,month,day,reason) values (\"{interaction.user}\",{self.year},{self.month},{self.day},\"{self.reason}\")")

            await interaction.response.send_message("已經送出假單了", ephemeral=True)
        except :
            await interaction.response.send_message("輸入格式錯誤", ephemeral=True)


# 選單
class menu(View):
    def __init__(self):
        super().__init__()
        self.value = None

    # 擲骰子
    @discord.ui.button(label="roll dice", style=discord.ButtonStyle.blurple)
    async def roll(self, interaction, button):
        v = rolldice()

        await interaction.response.send_message(view=v)

    # 創立投票
    @discord.ui.button(label="create vote", style=discord.ButtonStyle.blurple)
    async def vote(self, interaction, button):
        await interaction.response.send_modal(votemodal())

    # 猜拳
    @discord.ui.button(label="mora", style=discord.ButtonStyle.blurple)
    async def mora(self, interaction, button):
        embed = discord.Embed(title="猜拳", description="參加人員:")
        v = joinmora(embed=embed)
        await interaction.response.send_message(view=v, embed=embed)

    # 假單
    @discord.ui.button(label="leave form", style=discord.ButtonStyle.blurple)
    async def leave(self, interaction, button):
        await interaction.response.send_modal(leavemodal())

    # 查詢請假人員
    @discord.ui.button(label="check leave", style=discord.ButtonStyle.blurple)
    async def checkleave(self, interaction, button):
        count = 0
        now=datetime.datetime.now()
        leavelist=[]
        with database.dbopen("./database.db") as c:
            c.execute(f"select * from leave where year={now.year} and month={now.month} and day={now.day}")
            leavelist=c.fetchall()
        id=interaction.channel_id
        ch=sysini.client.get_channel(id)
        for i in leavelist:
             await ch.send(f"姓名:{i[1]} \n日期:{i[2]}-{i[3]}-{i[4]} \n原因:{i[5]}\n\n")
        if len(leavelist)==0:
            await interaction.response.send_message("今天沒有人請假")
        else:
            await interaction.response.send_message(f"共查詢到{len(leavelist)}筆資料")
        return
        
    # 書籍推薦
    @discord.ui.button(label="book recommand",style=discord.ButtonStyle.blurple)
    async def book(self,interaction,button):
        await interaction.response.send_modal(bookmodal(self))
    
    # 電影
    @discord.ui.button(label="new movie",style=discord.ButtonStyle.blurple)
    async def movie(self,interaction,button):
        list=movie1.get_result()
        id=interaction.user.id
        user=sysini.client.get_user(id)
        for i in list:
            embed.title=str(i["name"])
            embed.set_thumbnail(url=i['url'])
            
            await user.send(embed=embed)
    # 星座
    @discord.ui.button(label="fortune-teller",style=discord.ButtonStyle.blurple)
    async def luck(self,interaction,button):
        v=luckview()
        await interaction.response.send_message(view=v,ephemeral=True)


## 星座
class luckview(View):
    def __init__(self):
        super().__init__()
        self.s=None
    list1 = ["牡羊座","金牛座","雙子座","巨蟹座",
            "獅子座","處女座","天秤座","天蠍座",
            "射手座","摩羯座","水瓶座","雙魚座"]
    @discord.ui.select(
        placeholder="chose constellation",
        options=[ discord.SelectOption(value=i,label=i) for i in list1]
    )
    async def callback(self,interection,select):
        self.s=str(select.values[0])
        select.placeholder=str(select.values[0])
        await interection.response.edit_message(view=self)

    @discord.ui.button(label="submit",style=discord.ButtonStyle.green)
    async def submit(self,interction,button):
        out=constellation1.destiny(self.s)
        await interction.response.send_message(out, ephemeral=True)
#查詢推薦書籍


class bookmodal(Modal,title="書籍推薦"):
    def __init__(self,view):
        super().__init__()
        self.v=view

    cls = TextInput(
        label="key",
        style=discord.TextStyle.short,
        placeholder="class",
        default="None",
        required=True,
        max_length=20,
        row=0,
    )
    async def on_submit(self, interaction: discord.Interaction):
        list=book2.query(str(self.cls) )
        id=interaction.user.id
        user=sysini.client.get_user(id)
        await interaction.response.edit_message(view=self.v)
        for i in list:
            embed.set_thumbnail(url=i["url"])
            embed.title=i['name']
            embed.description=i['price']
            await user.send(embed=embed)
# 猜拳
class joinmora(View):
    def __init__(self, embed):
        super().__init__()
        self.embed = embed
        self.moralist = []  # 猜拳列表
        self.joinuser = []  # 參加人員列表
        self.submitlist = []  # 已經出拳的人員列表
    
    def gameset(self):
        out = ""
        for i in range(len(self.moralist)):
            out += f"{self.moralist[i]['user']}:{self.moralist[i]['value']}\n"

        self.joinuser.clear()
        self.submitlist.clear()
        self.moralist.clear()
        return out

    @discord.ui.button(label="剪刀", style=discord.ButtonStyle.red)
    async def scissors(self, interaction, button):
        if str(interaction.user) not in self.joinuser:
            await interaction.response.send_message("你沒有參加遊戲", ephemeral=True)
            return
        if str(interaction.user) not in self.submitlist:
            self.submitlist.append(str(interaction.user))
            self.moralist.append({"user": str(interaction.user), "value": "剪刀"})
            if len(self.submitlist) == len(self.joinuser):
                await interaction.response.send_message("遊戲結束\n" + self.gameset())
            else:
                await interaction.response.send_message("等待其他人", ephemeral=True)
        else:
            await interaction.response.send_message("你已經出過拳了", ephemeral=True)

    @discord.ui.button(label="石頭", style=discord.ButtonStyle.red)
    async def rock(self, interaction, button):
        if str(interaction.user) not in self.joinuser:
            await interaction.response.send_message("你沒有參加遊戲", ephemeral=True)
            return
        if str(interaction.user) not in self.submitlist:
            self.submitlist.append(str(interaction.user))
            self.moralist.append({"user": str(interaction.user), "value": "石頭"})

            if len(self.submitlist) == len(self.joinuser):
                await interaction.response.send_message("遊戲結束\n" + self.gameset())
            else:
                await interaction.response.send_message("等待其他人", ephemeral=True)
        else:
            await interaction.response.send_message("你已經出過拳了", ephemeral=True)

    @discord.ui.button(label="布", style=discord.ButtonStyle.red)
    async def paper(self, interaction, button):
        if str(interaction.user) not in self.joinuser:
            await interaction.response.send_message("你沒有參加遊戲", ephemeral=True)
            return
        if str(interaction.user) not in self.submitlist:
            self.submitlist.append(str(interaction.user))
            self.moralist.append({"user": str(interaction.user), "value": "布"})
            if len(self.submitlist) == len(self.joinuser):
                await interaction.response.send_message("遊戲結束\n" + self.gameset())
            else:
                await interaction.response.send_message("等待其他人", ephemeral=True)
        else:
            await interaction.response.send_message("你已經出過拳了", ephemeral=True)

    @discord.ui.button(label="join", style=discord.ButtonStyle.green)
    async def join(self, interaction, button):
        if interaction.user not in self.joinuser:
            self.joinuser.append(str(interaction.user))
            self.embed.description = f"{self.embed.description}\n{interaction.user}"
            await interaction.response.edit_message(embed=self.embed, view=self)
        else:
            await interaction.response.send_message("你已經參加了", ephemeral=True)


# 投票介面
class voteui(View):
    def __init__(self, embed, l1, l2, l3):
        super().__init__()
        self.c1 = 0  # choice1的票數
        self.c2 = 0  # choice2的票數
        self.c3 = 0  # choice3的票數

        self.l1 = l1  # choice1的名稱
        self.l2 = l2  # choice2的名稱
        self.l3 = l3  # choice3的名稱
        self.votelist = []  # 記錄誰投票了
        self.embed = embed  # 投票的embed

    def update(self):  # 更新票數
        return (
            self.l1 + "  " + str(self.c1) + "\n" + self.l2 + "  " + str(self.c2) + "\n" + self.l3 + "  " + str(self.c3)
        )

    @discord.ui.button(label="option A", style=discord.ButtonStyle.green)
    async def choice1(self, interaction, button):
        if interaction.user.id not in self.votelist:
            self.votelist.append(interaction.user.id)
            self.c1 += 1
            self.embed.description = self.update()
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("你已經投過票了", ephemeral=True)

    @discord.ui.button(label="option B", style=discord.ButtonStyle.green)
    async def choice2(self, interaction, button):
        if interaction.user.id not in self.votelist:
            self.votelist.append(interaction.user.id)
            self.c2 += 1
            self.embed.description = self.update()
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("你已經投過票了", ephemeral=True)

    @discord.ui.button(label="option C", style=discord.ButtonStyle.green)
    async def choice3(self, interaction, button):
        if interaction.user.id not in self.votelist:
            self.votelist.append(interaction.user.id)
            self.c3 += 1
            self.embed.description = self.update()
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("你已經投過票了", ephemeral=True)


# 投票設定表單
class votemodal(Modal, title="vote setting"):
    t = TextInput(
        label="title",
        style=discord.TextStyle.short,
        placeholder="title",
        default="None",
        required=True,
        max_length=50,
        row=0,
    )
    s1 = TextInput(
        label="option A",
        style=discord.TextStyle.short,
        placeholder="option A",
        default="None",
        required=True,
        max_length=50,
        row=1,
    )
    s2 = TextInput(
        label="option B",
        style=discord.TextStyle.short,
        placeholder="option B",
        default="None",
        required=True,
        max_length=50,
        row=2,
    )
    s3 = TextInput(
        label="option C",
        style=discord.TextStyle.short,
        placeholder="option C",
        default="None",
        required=True,
        max_length=50,
        row=3,
    )

    async def on_submit(self, interaction: discord.Interaction):
        l1 = str(self.s1.label) + "：" + str(self.s1)
        l2 = str(self.s2.label) + "：" + str(self.s2)
        l3 = str(self.s3.label) + "：" + str(self.s3)

        embed = discord.Embed(
            title=str(self.t),
            description=l1 + "  0\n" + l2 + "  0\n" + l3 + "  0",
            timestamp=datetime.datetime.now(),
            color=discord.Color.red(),
        )
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)  # 設定誰發起的
        v = voteui(embed=embed, l1=l1, l2=l2, l3=l3)
        await interaction.response.send_message(view=v, embed=embed)


# 丟骰子的介面
class rolldice(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="roll", style=discord.ButtonStyle.red)
    async def roll(self, interaction, button):
        i = random.randint(1, 6)

        # 圖片自己找的 可修改
        embed.set_thumbnail(url=ConfigParser()["image"][f"dice_{i}_url"])

        await interaction.response.edit_message(embed=embed)



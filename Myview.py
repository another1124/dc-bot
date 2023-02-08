import json
from discord.ext import commands
from discord.ui import Button , View, Select ,TextInput,Modal
from discord import app_commands
import discord
import datetime
import random


embed = discord.Embed()
leavelist=[]

###假單
class leavemodal(Modal,title = 'leave form'):
    def __init__(self):
        super().__init__()
        self.value = None
    
    year=TextInput(label='year',style=discord.TextStyle.long,placeholder='title',default=datetime.datetime.now().year,required=True,max_length=4,row=0)
    month=TextInput(label='month',style=discord.TextStyle.long,placeholder='title',default=datetime.datetime.now().month,required=True,max_length=2,row=0)
    day=TextInput(label='day',style=discord.TextStyle.long,placeholder='title',default=datetime.datetime.now().day,required=True,max_length=2,row=0)
    cause=TextInput(label='cause',style=discord.TextStyle.long,placeholder='title',default='None',required=True,max_length=50,row=1)

    async def on_submit(self, interaction: discord.Interaction):
        leavelist.append({'user':str(interaction.user),'cause':self.cause,'time':datetime.datetime.strptime(self.year+self.month+self.day,"%Y%m%d")})
        print(leavelist)
        await interaction.response.send_message("已經送出假單了",ephemeral=True)
    

###選單
class menu(View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="roll dice",style=discord.ButtonStyle.red)
    async def roll(self,interaction, button):
        v=rolldice()
        
        await interaction.response.send_message(view=v)
    @discord.ui.button(label="record",style=discord.ButtonStyle.red)
    async def record(self,interaction, button ):
        v=record()
        
        await interaction.response.send_message(view=v)
    @discord.ui.button(label="create vote",style=discord.ButtonStyle.red)
    async def vote(self,interaction, button ):
        await interaction.response.send_modal(votemodal())

### 投票介面
class voteui(View):
    
    def __init__(self,embed,l1,l2,l3):
        super().__init__()
        self.c1=0
        self.c2=0
        self.c3=0
        self.l1=l1
        self.l2=l2
        self.l3=l3
        self.votelist=[] ## 記錄誰投票了
        self.embed=embed
    
    def update(self): ##更新票數
        return self.l1+"  "+str(self.c1)+'\n'+self.l2+"  "+str(self.c2)+'\n'+self.l3+"  "+str(self.c3)
    @discord.ui.button(label="choice1",style=discord.ButtonStyle.green)
    async def choice1(self,interaction, button ):
        if interaction.user.id not in self.votelist:
            self.votelist.append(interaction.user.id)
            self.c1+=1
            self.embed.description=self.update()
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("你已經投過票了",ephemeral=True)
    @discord.ui.button(label="choice2",style=discord.ButtonStyle.green)
    async def choice2(self,interaction, button ):
        if interaction.user.id not in self.votelist:
            self.votelist.append(interaction.user.id)
            self.c2+=1
            self.embed.description=self.update()
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("你已經投過票了",ephemeral=True)
    @discord.ui.button(label="choice3",style=discord.ButtonStyle.green)
    async def choice3(self,interaction, button ):
        if interaction.user.id not in self.votelist:
            self.votelist.append(interaction.user.id)
            self.c3+=1
            self.embed.description=self.update()
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message("你已經投過票了",ephemeral=True)
    
##投票設定
class votemodal(Modal,title = 'vote setting'):
    t=TextInput(label='title',style=discord.TextStyle.short,placeholder='title',default='None',required=True,max_length=50,row=0)
    s1=TextInput(label='choice 1',style=discord.TextStyle.short,placeholder='choice 1',default='None',required=True,max_length=50,row=1)
    s2=TextInput(label='choice 2',style=discord.TextStyle.short,placeholder='choice 2',default='None',required=True,max_length=50,row=2)
    s3=TextInput(label='choice 3',style=discord.TextStyle.short,placeholder='choice 3',default='None',required=True,max_length=50,row=3)
    
    
    async def on_submit(self, interaction: discord.Interaction):
        l1=str(self.s1.label) + ':' + str(self.s1)
        l2=str(self.s2.label) + ':' + str(self.s2)
        l3=str(self.s3.label) + ':' + str(self.s3)
        
        embed = discord.Embed(title=str(self.t),description=l1+'  0\n'+l2+'  0\n'+l3+'  0',
                              timestamp=datetime.datetime.now(),color=discord.Color.red())
       # embed.set_author(name= interaction.user, icon_url=interaction.user.avatar)  #設定誰能看到
        v=voteui(embed=embed,l1=l1,l2=l2,l3=l3)
        await interaction.response.send_message(view=v,embed=embed)


##丟骰子
class rolldice(View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="roll",style=discord.ButtonStyle.red)
    async def roll(self,interaction, button):
        i=random.randint(1,6)
        if i==1:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/774950219669307397/1069858458163228702/1.png?width=467&height=467")
        if i==2:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/774950219669307397/1069858458456838154/2.png?width=467&height=467")
        if i==3:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/774950219669307397/1069858458716876840/3.png?width=467&height=467")
        if i==4:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/774950219669307397/1069858458905628722/4.png?width=467&height=467")
        if i==5:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/774950219669307397/1069858459106934844/5.png?width=467&height=467")
        if i==6:
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/774950219669307397/1069858459333439498/6.png?width=467&height=467")
        await interaction.response.edit_message(embed=embed)

class record(View):
    def __init__(self):
        super().__init__()
        self.value = None
        
    @discord.ui.button(label="start",style=discord.ButtonStyle.red)
    async def start(self,interaction, button):
        channel = interaction.channel
        out="channel is "+str(channel)
        await interaction.response.send_message(out)

    @discord.ui.button(label="stop",style=discord.ButtonStyle.red)
    async def stop(self,interaction, button):
        await interaction.response.edit_message(embed=self.value)






    
    

import json
import discord
import requests
import time
import os
import subprocess
import time
import random
import io
import pprint
import pandas as pd
from tabulate import tabulate
from discord.ext import commands, tasks

TOKEN=str(open("bot.token","r").readline()).replace("\n","")
prev = 366405

CHANNEL = None

client = discord.Client()

def convertName(things):
    retlist = []
    for thing in things:
        thing = thing.split(" ")
        retstring = ""
        for _ in thing:
            retstring += _[0]
        retlist.append(retstring)
    return retlist

# async def backtask():
#
#         global CHANNEL
#         message=CHANNEL
#         while(1):
#
#             prev=366405
#             res = requests.get('https://www.osmania.ac.in/examination-results.php').text
#
#             if len(res)!=prev:
#                 prev=len(res)
#                 await message.send(f"Results aagaye I guess <@&874319527167545344>")
#             # else:
#             #     await message.send(f"Checking if this works or not <@&874319527167545344>")
#               
#
#           
#
#             time.sleep(600)

            



def system_call(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return (output,err)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Game(name="Suffering with exam result")
    #client.loop.create_task(backtask())

    


@client.event
async def on_message(message):
    global prev,CHANNEL

    if(message.content.startswith("setchannel?")):
        CHANNEL = message.CHANNEL


    if(message.content.startswith("cmd?")):
        print("Entering Command Shell bash")
        if("rm" in message.content or "nano" in message.content or "apt" in message.content or "bot.token" in message.content):
            await message.channel.send("NOT ALLOWED")
            return 0
        try:
            await message.channel.send(f"```{str(system_call(str(message.content)[4:])[0].decode(encoding='UTF-8',errors='strict'))}```"[:1950])
        except IndexError as e:
            try:
                framify = f"```{str(system_call(str(message.content)[4:])[1])}``` \n{e}"[:1950]
                embed = discord.Embed(title="bash", colour=discord.Colour(0x7bff61), description=framify)
                await message.channel.send(embed=embed)
            except Exception as p:
                await message.channel.send(embed=discord.Embed(title="Execution Error", colour=discord.Colour(0xff6164), description="Something went wrong while executing "))
        return

    if message.author == client.user:
        return
    if(message.content.startswith('jnturesult?')):
        lencmd = 11
        s = message.content
        rollno = s[s.find('rno')+4:s.find('rno')+14]
        examcode = s[s.find('ecode')+6:s.find('ecode')+10]
        try:
            result = requests.get("http://api.itspacchu.tk/jnturesult?rollno="+rollno+"&examcode="+examcode).json()
            df = pd.DataFrame(result['result']).drop(['SUB_CODE','CREDIT','INTERNAL','EXTERNAL'],axis=1)
            df['SUB_NAME'] = convertName(df['SUB_NAME'].to_list())
            df = df.set_index("SUB_NAME")
            usrclass = result['usr']
            gpa = result['sgpa']
            result = tabulate(df,headers="keys",tablefmt="psql")
            embed = discord.Embed(title=f"{usrclass[0]} : {usrclass[1]} GPA : {gpa}", colour=discord.Colour(0x9185ff), description="```"+result[:1990]+"```")
            embed.set_footer(text="Courtesy of http://api.itspacchu.tk", icon_url="https://cdn.discordapp.com/attachments/852930321493655563/881428478640140328/pacbot.png")
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="404", colour=discord.Colour(0xff6161), description=f"Result not found or Probably not out yet?? Check maybe later \n||{e}||")
            embed.set_footer(text="Courtesy of http://api.itspacchu.tk", icon_url="https://cdn.discordapp.com/attachments/852930321493655563/881428478640140328/pacbot.png")
            await message.channel.send(embed=embed)

    if(message.content.startswith('results?')):
        res = requests.get('https://www.osmania.ac.in/examination-results.php').text
        if(len(res)!=prev):

            await message.add_reaction("🔎")
            await message.channel.send(f"Results are out I guess ... <@&874319527167545344>")
            return

        elif len(res)==prev:
            await message.add_reaction("🔎")
            embed = discord.Embed(title="Nope", colour=discord.Colour(0xff6161), description=f"Take it easy. Results nahi aaye {message.author.mention}")
            embed.set_footer(text="Courtesy of Baseer's OU API", icon_url="https://cdn.discordapp.com/attachments/852930321493655563/881447276969619496/731cb6ef4b3004a109fc13e653ef8965.png")
            await message.channel.send(embed=embed)

@client.command(name='oof')
async def oog(ctx):
    quotes = ['Yesterday is history, tomorrow is a mystery, and today is a gift... that\'s why they call it present','If she cannot make you come, then you go for her mum','If your granny has dentures, it is fine to have adventures','If there is a hole, there is a goal, even if she has a pp ._.']
    b = random.randit(0, len(quote))
    await ctx.send(f'Today\'s Master Oogway Quote - {quotes[b]}')

client.run(TOKEN)

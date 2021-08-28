import discord
import requests
import time
import os
import subprocess
import time
import io

TOKEN=str(open("bot.token","r").readline()).replace("\n","")
prev = 366405

CHANNEL = None

client = discord.Client()


async def backtask():

        global CHANNEL
        message=CHANNEL
        while(1):

            prev=366405
            res = requests.get('https://www.osmania.ac.in/examination-results.php').text

            if len(res)!=prev:
                prev=len(res)
                await message.send(f"Results aagaye I guess <@&874319527167545344>")
            # else:
            #     await message.send(f"Checking if this works or not <@&874319527167545344>")
                

            

            time.sleep(600)

            



def system_call(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    return (output,err)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Game(name="Suffering with exam result")
    client.loop.create_task(backtask())

    


@client.event
async def on_message(message):
    global prev,CHANNEL

    if(message.content.startswith("cmd?")):
        CHANNEL = message.CHANNEL


    if(message.content.startswith("cmd?")):
        print("Entering Command Shell bash")
        if("rm" in message.content or "nano" in message.content or "apt" in message.content or "bot.token" in message.content):
            await message.channel.send("NOT ALLOWED")
            return 0
        try:
            await message.channel.send(f"```{str(system_call(str(message.content)[4:])[0].decode(encoding='UTF-8',errors='strict'))}```"[:1950])
        except Exception as e:
            try:
                await message.channel.send(f"```{str(system_call(str(message.content)[4:])[1])}``` \n{e}"[:1950])
            except Exception as p:
                await message.channel.send(f"Something broke?{p}")
        return

    if message.author == client.user:
        return

    if message.content.startswith('results?'):
            res = requests.get('https://www.osmania.ac.in/examination-results.php').text
            if(len(res)!=prev):

                await message.add_reaction("🔎")
                await message.channel.send(f"Results are out I guess..Check! <@&874319527167545344>")
                return

            elif len(res)==prev:
                await message.add_reaction("🔎")
                await message.channel.send(f"Take it easy. Results nahi aaye {message.author.mention}")
    
    

client.run(TOKEN)

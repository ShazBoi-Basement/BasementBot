import discord
import requests
import time

TOKEN="NzI3MDA2MzY2MzIxMDgyNDkx.XvljcA.17yPNj9W9pgzcTAfWi9yXc3AXvQ"

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

prev = 366405
@client.event
async def on_message(message):

    print(message.content)

    global prev
    res = requests.get('https://www.osmania.ac.in/examination-results.php').text

    if message.author == client.user:
        return

    if message.content.startswith('results?') and len(res)!=prev:

        await message.add_reaction("🔎")
        await message.channel.send(f"Results are out I guess..Check! <@&874319527167545344>")
        return

    elif message.content.startswith('results?') and len(res)==prev:
        await message.add_reaction("🔎")
        await message.channel.send(f"Take it easy. Results nahi aaye {message.author.mention}")


client.run(TOKEN)

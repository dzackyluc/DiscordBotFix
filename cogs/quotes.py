import discord
import logging
import requests
import datetime
import asyncio
from discord.ext import commands

def quotesani():
    url = "https://katanime.vercel.app/api/getrandom"

    payload = ""
    headers = {"User-Agent": "insomnia/8.4.5"}

    response = requests.request("GET", url, data=payload, headers=headers)

    result = response.json()
    
    return result

def imageani(charname: str):
    import requests

    url = "https://www.animecharactersdatabase.com/api_series_characters.php"

    querystring = {"character_q":charname}

    payload = ""
    headers = {
        "cookie": "USTATS=17035408646c46008900471644a78138073f445975",
        "User-Agent": "insomnia/8.4.5"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    result = response.json()

    return result

class quotes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/quotes is online!")

    @commands.hybrid_command(name="quotes", description="Get quotes from anime character")
    async def quotes(self, interaction: discord.Interaction):
        await interaction.interaction.response.defer()
        data = quotesani()
        resultquote = data['result'][0]['indo']
        character = data['result'][0]['character']

        gambar = imageani(character)
        if gambar == -1:
            pass
        else:
            resultlink = gambar['search_results'][0]['character_image']

        embed = discord.Embed(title=character,
                      description=f"> {resultquote}",
                      colour=0x41f500,
                      timestamp=datetime.datetime.now())

        embed.set_author(name=interaction.message.author,
                 icon_url=interaction.message.author.avatar)
        
        if gambar == -1:
            pass
        else:
            embed.set_image(url=f"{resultlink}")

        embed.set_footer(text=self.client.user.name,
                 icon_url=self.client.user.avatar)

        await interaction.interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(quotes(client))
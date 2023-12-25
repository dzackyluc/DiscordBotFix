import discord
import logging
import requests
from discord.ext import commands

class bingai(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/bingai is online!")

    @commands.command()
    async def bingai(self, ctx, *, messages: str):
        querystring = {"role":"user","content":messages}
        url = "https://gpts4u.p.rapidapi.com/bingChat"

        payload = [
            {
                "role": "user",
                "content": messages
            }
        ]
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "insomnia/8.4.5",
            "X-RapidAPI-Key": "3a604343c0msh23c5684994743b2p1ed3e7jsnf816bda51cbf",
            "X-RapidAPI-Host": "gpts4u.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers, params=querystring)

        await ctx.send(response.text)

async def setup(client):
    await client.add_cog(bingai(client))
import discord
import logging
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/ping is online!")

    @commands.command()
    async def ping(self, ctx):
        botlatency = round(self.client.latency * 1000)
        await ctx.send(f"connected {botlatency} ms!")

async def setup(client):
    await client.add_cog(ping(client))
import discord
import logging
from discord.ext import commands

class twitter(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/twitsend is online!")

    @commands.command()
    async def twitsend(self, ctx, messages):
        await ctx.send("testing twit send!")

async def setup(client):
    await client.add_cog(twitter(client))
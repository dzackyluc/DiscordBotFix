import discord
import logging
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/ping is online!")

    @commands.hybrid_command(name="ping", description="Ping the bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.interaction.response.defer(ephemeral=True)
        botlatency = round(self.client.latency * 1000)
        await interaction.interaction.followup.send(f"connected {botlatency} ms!")

async def setup(client):
    await client.add_cog(ping(client))
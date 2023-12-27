import discord
import logging
from discord.ext import commands

class embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/embed is online!")

    @commands.hybrid_command(name="embed", description="Display some help")
    async def embed(self, interaction: discord.Interaction):
        embedmessage = discord.Embed(title="LIST ALL COMMANDS", color=discord.Color.green())
        embedmessage.set_author(name=f"Requested by {interaction.author.mention}", icon_url=interaction.author.avatar)
        embedmessage.add_field(name="/embed", value="Menampilkan teks ini", inline=False)
        embedmessage.add_field(name="/ping", value="Menampilkan latency", inline=False)
        embedmessage.add_field(name="/twitsend", value="Mengiim twit ke base", inline=False)
        embedmessage.add_field(name="/join", value="Join ke voice channel", inline=False)
        embedmessage.add_field(name="/leave", value="Keluar dari voice channel", inline=False)
        embedmessage.add_field(name="/play", value="Memainkan musik", inline=False)
        embedmessage.add_field(name="/skip", value="Melewati lagu yang sedang dimainkan", inline=False)

        await interaction.interaction.response.send_message(embed = embedmessage)

async def setup(client):
    await client.add_cog(embed(client))
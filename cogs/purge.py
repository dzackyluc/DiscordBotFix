import discord
import asyncio
import logging
from discord.ext import commands

class purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/purge is online!")

    @commands.hybrid_command(name="purge", description="Delete chat with given value(Admin Only)")
    @commands.has_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction, amount = 0):
        await interaction.interaction.response.defer(ephemeral=True)
        if amount == 0:
            await interaction.interaction.followup.send("Please enter an amount to delete!")

        elif amount > 0 or amount < 100:
            await interaction.channel.purge(limit=amount)
            await asyncio.sleep(2)
            await interaction.interaction.followup.send(f"{amount} messages has been deleted")
        else:
            await interaction.interaction.followup.send("Cannot delete more than 99")

async def setup(client):
    await client.add_cog(purge(client))
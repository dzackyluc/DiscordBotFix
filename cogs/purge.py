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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount = 0):
        if amount == 0:
            fail = await ctx.send ("Please enter an amount to delete!")
            await asyncio.sleep (6)
            await fail.delete()

        elif amount > 0 or amount < 100:
            await ctx.channel.purge(limit=amount)
            sucess = await ctx.send (f"{amount} messages has been deleted <a:Verified:878231325469974599>") #sending success msg
            await asyncio.sleep (6) #wait 6 seconds
            await sucess.delete() #deleting the sucess msg
        else:
            fail = await ctx.send ("Cannot purge more than 99")
            await asyncio.sleep (6)
            await fail.delete()

async def setup(client):
    await client.add_cog(purge(client))
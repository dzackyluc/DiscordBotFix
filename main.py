import os
import asyncio
import discord
import logging
from app import alwayson
from discord.ext import commands, tasks

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
discord.utils.setup_logging(level=logging.INFO)

@client.event
async def on_ready():
    logging.info(f"Logged in: {client.user} | {client.user.id}")
    await client.tree.sync()

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(str(DISCORD_TOKEN))

alwayson()
asyncio.run(main())
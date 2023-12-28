import discord
import logging
import requests
import datetime
import asyncio
from discord.ext import commands

def alquran(number: int):
    url = f"https://equran.id/api/v2/surat/{number}"

    payload = ""
    headers = {"User-Agent": "insomnia/8.4.5", "Content-Type": "application/json"}

    response = requests.request("GET", url, data=payload, headers=headers)

    result = response.json()
    
    return result

class quran(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/quotes is online!")

    @commands.hybrid_command(name="quran", description="Dapatkan ayat al-quran berdasarkan surat")
    async def quran(self, interaction: discord.Interaction, nomor: int):
        await interaction.interaction.response.defer()
        if nomor >= 1 or nomor <= 114:
            hasil = alquran(nomor)
            namalatin = hasil['data']['namaLatin']
            deskripsi = hasil['data']['deskripsi']
            replacements = str(deskripsi).replace("<i>", "_").replace("</i>", "_")
            ayats = hasil['data']['ayat']
            audio = hasil['data']['audioFull']['01']
            mbed = discord.Embed(title=f"{namalatin}",
                  description=f"{replacements}",
                  colour=0x00b0f4,
                  timestamp=datetime.datetime.now())
            mbed.set_author(name=interaction.message.author, icon_url=interaction.message.author.avatar)
            for ayat in ayats:
                teks_arab = ayat['teksArab']
                teks_latin = ayat['teksLatin']
                mbed.add_field(name=f"{teks_arab}",
                               value=f"{teks_latin}",
                               inline=False)
            mbed.add_field(name="Link Audio Baca",
                           value=f"> {audio}",
                           inline=False)
            mbed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar)
            await interaction.interaction.followup.send(embed=mbed)
        else:
            await interaction.interaction.followup.send("Pilih dari surat 1 sampai surat ke 114")


async def setup(client):
    await client.add_cog(quran(client))
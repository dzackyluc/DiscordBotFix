import discord
import wavelink
import logging
import asyncio
import typing
from typing import cast
from discord.ext import commands, tasks

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.position = 0
        self.repeat = False
        self.repeatMode = "NONE"
        self.playingTextChannel = 0
        client.loop.create_task(self.create_nodes())
    
    async def create_nodes(self):
        nodes = [wavelink.Node(uri="http://n1.ll.darrennathanael.com:2269", password="glasshost1984", secure=False)]
        await self.client.wait_until_ready()
        await wavelink.NodePool.connect(client=self.client, nodes=nodes)
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("/Music is online!")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        logging.info(f"Node <{node.id}> is now Ready! | Resumed: <{node.status}>")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload:wavelink.TrackEventPayload):
        reason = payload.reason
        try:
            self.queue.pop(0)
        except:
            pass
        logging.info(reason)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload:wavelink.TrackEventPayload):
        player: wavelink.Player | None = payload.player
        reason= payload.reason
        if str(reason) == "FINISHED":
            if not len(self.queue) == 0:
                next_track: wavelink.tracks = self.queue[0]
                channel = self.client.get_channel(self.playingTextChannel)

                try:
                    await player.play(next_track)
                except:
                    return await self.commands.Context.send(embed=discord.Embed(title=f"Something went wrong while playing **{next_track.title}**", color=discord.Color.from_rgb(255, 255, 255)))
                
                await self.commands.Context.send(embed=discord.Embed(title=f"Now playing: {next_track.title}", color=discord.Color.from_rgb(255, 255, 255)))
            else:
                pass
        else:
            logging.info(reason)

    @commands.command(name="join", aliases=["connect", "summon"])
    async def join_command(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            channel = ctx.author.voice.channel
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is not None:
            if player.is_connected():
                return await ctx.send("bot is already connected to a voice channel")
        
        await channel.connect(cls=wavelink.Player)
        mbed=discord.Embed(title=f"Connected to {channel.name}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)

    @commands.command(name="leave", alises=["disconnect"])
    async def leave_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("bot is not connected to any voice channel")
        
        await player.stop()
        await player.disconnect()
        mbed = discord.Embed(title="Disconnected", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)
    
    @commands.command(name="play")
    async def play_command(self, ctx: commands.Context, *, search: str):
        try:
            search = await wavelink.YouTubeMusicTrack.search(search)
        except:
            return await ctx.reply(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255, 255, 255)))

        track = search[0]

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if not vc.is_playing():
            try:
                await player.play(track)
            except:
                return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this tracks", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            self.queue.append(track)

        mbed = discord.Embed(title=f"Added {track} To the queue", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)
    
    @commands.command(name="stop")
    async def stop_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")

        self.queue.clear()
        
        if player.is_playing():
            await player.stop()
            mbed = discord.Embed(title="Playback Stoped", color=discord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=mbed)
        else:
            return await ctx.send("Nothing Is playing right now")
    
    @commands.command(name="pause")
    async def pause_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                mbed = discord.Embed(title="Playback Paused", color=discord.Color.from_rgb(255, 255, 255))
                return await ctx.send(embed=mbed)
            else:
                return await ctx.send("Nothing is playing right now")
        else:
            return await ctx.send("Playback is Already paused")
    
    @commands.command(name="resume")
    async def resume_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if player is None:
            return await ctx.send("bot is not connnected to any voice channel")
        
        if player.is_paused():
            await player.resume()
            mbed = discord.Embed(title="Playback resumed", color=discord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=mbed)
        else:
            if not len(self.queue) == 0:
                track: wavelink.tracks = self.queue[0]
                player.play(track)
                return await ctx.reply(embed=discord.Embed(title=f"Now playing: {track.title}"))
            else:
                return await ctx.send("playback is not paused")

    @commands.command(name="volume")
    async def volume_command(self, ctx: commands.Context, to: int):
        if to > 100:
            return await ctx.send("Volume should be between 0 and 100")
        elif to < 1:
            return await ctx.send("Volume should be between 0 and 100")

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        await player.set_volume(to)
        mbed = discord.Embed(title=f"Changed Volume to {to}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)

    @commands.command(name="skip")
    async def skip_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)

        if not len(self.queue) == 0:
            next_track: wavelink.tracks = self.queue[0]
            try:
                await player.play(next_track)
            except:
                return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255, 255, 255)))

            await ctx.reply(embed=discord.Embed(title=f"Now playing {next_track.title}", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            await ctx.reply("The queue is empty")

    #this command would queue a song if some args(search) is provided else it would just show the queue
    @commands.command(name="queue")
    async def queue_command(self, ctx: commands.Context, *, search=None):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        
        if search is None:
            if not len(self.queue) == 0:
                np = wavelink.tracks.Playable | None
                mbed = discord.Embed(
                    title=f"Now playing: {np}" if player.is_playing else "Queue: ",
                    description = "\n".join(f"**{i+1}. {track}**" for i, track in enumerate(self.queue[:10])) if not player.is_playing else "**Queue: **\n"+"\n".join(f"**{i+1}. {track}**" for i, track in enumerate(self.queue[:10])),
                    color=discord.Color.from_rgb(255, 255, 255)
                )

                return await ctx.reply(embed=mbed)
            else:
                return await ctx.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            try:
                track = await wavelink.YouTubeMusicTrack.search(search)
            except:
                return await ctx.reply(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255, 255, 255)))
            
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel(cls=wavelink.Player)
                await player.connect(ctx.author.voice.channel)
            else:
                vc: wavelink.Player = ctx.voice_client
            
            if not vc.is_playing():
                try:
                    await vc.play(track)
                except:
                    return await ctx.reply(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255, 255, 255)))
            else:
                self.queue.append(track)
            
            await ctx.reply(embed=discord.Embed(title=f"Added {track.title} to the queue", color=discord.Color.from_rgb(255, 255, 255)))

async def setup(client):
    await client.add_cog(music(client))
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import yt_dlp

class MusicCog(commands.Cog):
    """Handles music commands for ArcaneBot"""
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "default_search": "ytsearch",
            "quiet": True,
            "no_warnings": True,
            "source_address": "0.0.0.0",
        }

        self.ydl = yt_dlp.YoutubeDL(ydl_opts)

    def search_youtube(self, query):
        try:
            data = self.ydl.extract_info(query, download=False)
            if "entries" in data:
                data = data["entries"][0]
            return {
                "title": data.get("title"),
                "url": data.get("url"),
                "webpage_url": data.get("webpage_url")
            }
        except Exception as e:
            return None

    @app_commands.command(name="join", description="Summon the mage to your voice channel")
    async def join(self, interaction: discord.Interaction):
        if interaction.user.voice and interaction.user.voice.channel:
            channel = interaction.user.voice.channel
            voice_client = interaction.guild.voice_client

            if voice_client:
                await voice_client.move_to(channel)
                await interaction.response.send_message(
                    f"🔮 Moved to **{channel.name}** to weave our musical tapestry.")
            else:
                await channel.connect()
                await interaction.response.send_message(
                    f"🔮 Joined **{channel.name}** and ready to channel melodies.")
        else:
            await interaction.response.send_message(
                "❌ You must be in a voice channel to summon me.", ephemeral=True)

    @app_commands.command(name="play", description="Play a song from YouTube")
    async def play(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()

        voice_client = interaction.guild.voice_client
        if not voice_client:
            if interaction.user.voice and interaction.user.voice.channel:
                channel = interaction.user.voice.channel
                voice_client = await channel.connect()
            else:
                await interaction.followup.send("❌ You're not in a voice channel.", ephemeral=True)
                return

        song = self.search_youtube(query)
        if not song:
            await interaction.followup.send("❌ Couldn't find anything with that search.")
            return

        url = song["webpage_url"]
        title = song["title"]

        # Stream audio
        ffmpeg_options = {
            "options": "-vn"
        }

        try:
            source = await discord.FFmpegOpusAudio.from_probe(
                song["url"],
                **ffmpeg_options
            )
            voice_client.play(source, after=lambda e: print(f"Player error: {e}") if e else None)
            await interaction.followup.send(f"🎶 Now playing: **{title}**")
        except Exception as e:
            await interaction.followup.send(f"⚠️ Failed to play song: {e}")

    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message("⏭️ Skipped the song.")
        else:
            await interaction.response.send_message("❌ Nothing is playing.", ephemeral=True)

    @app_commands.command(name="stop", description="Stop playing and leave the voice channel")
    async def stop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client:
            await voice_client.disconnect()
            await interaction.response.send_message("🛑 Music stopped and I have left the channel.")
        else:
            await interaction.response.send_message("❌ I'm not in a voice channel.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MusicCog(bot))

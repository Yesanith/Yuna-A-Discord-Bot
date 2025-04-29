import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone

class PingCog(commands.Cog):
    """Measures the mage's reflexes (latency)"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Measure the mage's arcane reflexes")
    async def arcane_ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        uptime = datetime.now(timezone.utc) - self.bot.start_time
        config = self.bot.config

        embed = discord.Embed(
            title="✨ Arcane Reflex Pulse",
            description=f"Measured latency is **{latency}ms**.\n"
                        f"The mage has been channeling for `{str(uptime).split('.')[0]}`.",
            color=config["embed_color"]
        )
        embed.set_footer(text=config["footer_text"])
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1364191142589235245/1366755125665861723/download20250405152346.png")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PingCog(bot))

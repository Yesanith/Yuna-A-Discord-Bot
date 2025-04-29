import discord
from discord.ext import commands
from discord import app_commands
import platform
import psutil
from datetime import datetime, timezone

class StatusCog(commands.Cog):
    """Displays system status with Arcane Mage analogy"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="View mage's arcane status")
    async def arcane_grid(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        uptime = datetime.now(timezone.utc) - self.bot.start_time
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        config = self.bot.config
        embed = discord.Embed(
            title="🔮 Arcane Grid Analysis",
            color=config["embed_color"]
        )
        embed.add_field(name="Familiar Bond Latency", value=f"```{latency}ms```", inline=True)
        embed.add_field(name="Channeling Duration", value=f"```{str(uptime).split('.')[0]}```", inline=True)
        embed.add_field(
            name="Mana Core Usage",
            value=f"```CPU: {cpu}%\nRAM: {ram}%```",
            inline=False
        )
        embed.add_field(name="Ethereal Platform", value=f"```{platform.system()}```", inline=True)
        embed.set_footer(text=config["footer_text"])
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1364191142589235245/1366755125665861723/download20250405152346.png?ex=68121967&is=6810c7e7&hm=6f8ee87c3e24fd36ce5c38706de106c18297a6fc4acf544b92e73a84e8470223&")  # replace with your asset

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(StatusCog(bot))
import discord
from discord import app_commands
import platform
import psutil
from datetime import datetime

def setup(bot, config):
    START_TIME = datetime.utcnow()
    
    @bot.tree.command(name="sphere_grid", description="View summoner's status")
    async def sphere_grid(interaction: discord.Interaction):
        """System status with FFX analogy"""
        latency = round(bot.latency * 1000)
        uptime = datetime.utcnow() - START_TIME
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        embed = discord.Embed(
            title="📜 Sphere Grid Analysis",
            color=config["embed_color"]
        )
        embed.add_field(
            name="Aeon Bond Latency",
            value=f"```{latency}ms```",
            inline=True
        )
        embed.add_field(
            name="Summoning Duration",
            value=f"```{str(uptime).split('.')[0]}```",
            inline=True
        )
        embed.add_field(
            name="Machina Core Usage",
            value=f"```CPU: {cpu}%\nRAM: {ram}%```",
            inline=False
        )
        embed.add_field(
            name="Celestial Platform",
            value=f"```{platform.system()}```",
            inline=True
        )
        embed.set_footer(text=config["footer_text"])
        embed.set_thumbnail(url="https://external-preview.redd.it/fHjk7O1Cbbyswd6cgN5w3T-p3ClR5H5q6dU1pRpZ24o.jpg?width=1080&crop=smart&auto=webp&s=53730ccaccdfbbeef88da9e4cb86de5c8b8eb59f")  # Yuna resmi
        
        await interaction.response.send_message(embed=embed)
import discord
from discord import app_commands
from discord.ext import commands
import random

class MysticFortune(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config  # config burada bot'tan alınıyor

    @app_commands.command(name="mfoyu", description="Reveal your mystic fortune")
    async def mfoyu(self, interaction: discord.Interaction):
        fortunes = [
            "The stars align in your favor. Destiny calls.",
            "The path ahead is shrouded in mist, proceed with caution.",
            "An unexpected ally will appear soon.",
            "Beware of those who speak in riddles; not all are as they seem.",
            "A great challenge is coming. Stay strong, brave soul.",
            "A powerful energy stirs within you. Harness it wisely."
        ]
        
        # Pick a random fortune
        fortune = random.choice(fortunes)

        # Get the user's display name (nickname in server)
        display_name = interaction.user.display_name  # This gets the nickname in the server, or username if no nickname

        # Prepare embed with the mystic fortune
        embed = discord.Embed(
            title="🔮 Mystic Fortune",
            description=f"**{display_name}**, your fortune is:",
            color=self.config["embed_color"]
        )
        embed.add_field(name="🌟 Your Fortune", value=fortune, inline=False)
        embed.set_footer(text=self.config["footer_text"])
        #embed.set_thumbnail(url="https://i.pinimg.com/originals/d2/a6/95/d2a6950ee61d2a58644b601f5dbf64b8.jpg")  # Mystic themed image

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(MysticFortune(bot))

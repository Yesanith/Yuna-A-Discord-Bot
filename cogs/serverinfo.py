import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config  # config burada bot'tan alınıyor

    @app_commands.command(name="serverinfo", description="Reveal secrets of this mystic realm")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        creation_date = guild.created_at.replace(tzinfo=timezone.utc).astimezone()

        embed = discord.Embed(
            title="📜 Realm Insight",
            description=f"Revealing secrets of **{guild.name}**...",
            color=self.config["embed_color"]
        )

        embed.add_field(name="🧙‍♀️ Realm Owner", value=f"<@{guild.owner_id}>", inline=True)
        embed.add_field(name="🌍 Region", value="Auto / Global", inline=True)
        embed.add_field(name="📆 Founded On", value=f"`{creation_date.strftime('%Y-%m-%d %H:%M:%S')}`", inline=False)
        embed.add_field(name="👥 Inhabitants", value=f"`{guild.member_count}` souls", inline=True)
        embed.add_field(name="💬 Text Channels", value=f"`{len(guild.text_channels)}`", inline=True)
        embed.add_field(name="🔊 Voice Channels", value=f"`{len(guild.voice_channels)}`", inline=True)
        embed.add_field(name="📜 Roles", value=f"`{len(guild.roles)}` distinct paths", inline=True)

        embed.set_footer(text=self.config["footer_text"])

        # If guild icon exists, set it as the thumbnail, otherwise, leave it out
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))

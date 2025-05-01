import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timezone
from termcolor import colored
from random import choice
import logging
from pathlib import Path

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Mage Themed Configuration
MAGE_CONFIG = {
    "embed_color": 0x9b59b6,
    "footer_text": "Arcane Mage • Guardian of the Ethereal",
    "status_messages": [
        "Channeling Arcane Energies",
        "Studying Ancient Grimoires",
        "Guarding the Mystic Realm"
    ]
}

# Setup intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Needed for voice control

# Setup logging to file
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file_path = log_dir / "arcane.log"

logger = logging.getLogger("arcane")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S UTC")
file_handler.setFormatter(file_fmt)
logger.addHandler(file_handler)

# Custom log function
def arcane_log(message: str, color: str, icon: str = "✨"):
    timestamp = colored(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "cyan")
    print(f"{icon} {timestamp} | {colored(message, color)}")
    logger.info(message)

# Custom Bot with command logging
class ArcaneBot(commands.Bot):
    async def on_app_command_completion(self, interaction: discord.Interaction, command: discord.app_commands.Command):
        try:
            user = interaction.user
            guild = interaction.guild
            channel = interaction.channel

            guild_info = f"{guild.name} ({guild.id})" if guild else "DM"
            channel_info = f"{channel.name} ({channel.id})" if hasattr(channel, 'name') else f"Channel ID: {channel.id}"

            log_msg = f"{user} ({user.id}) used /{command.name} in guild '{guild_info}', channel '{channel_info}'"
            arcane_log(log_msg, "blue", "🪄")
        except Exception as e:
            arcane_log(f"Failed to log command usage: {e}", "red", "⚠️")

# Init bot
bot = ArcaneBot(command_prefix="/", intents=intents)
bot.config = MAGE_CONFIG

# Bot is ready
@bot.event
async def on_ready():
    bot.start_time = datetime.now(timezone.utc)

    logger.info("=" * 60)
    logger.info(f"NEW SESSION • {bot.user} started at {bot.start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    logger.info("=" * 60)

    arcane_log(f"{bot.user} has awakened the Arcane Grimoire", "magenta", "🔮")

    await asyncio.sleep(2)
    try:
        synced = await bot.tree.sync()
        arcane_log(f"{len(synced)} arcane commands synchronized:", "cyan", "📜")
        for cmd in synced:
            arcane_log(f"- {cmd.name}", "white", "  ")
        await bot.change_presence(activity=discord.Game(name=choice(MAGE_CONFIG["status_messages"])))
    except Exception as e:
        arcane_log(f"Command synchronization failed: {e}", "red", "⚠️")

# Slash command error logging
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    user = interaction.user
    arcane_log(
        f"Command {interaction.command.name} error for {user} ({user.id}): {error}",
        "red",
        "🔥"
    )

# Load cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                arcane_log(f"{filename[:-3]} familiar bonded", "green", "🧙‍♀️")
            except Exception as e:
                arcane_log(f"Failed to bond {filename}: {e}", "red", "❌")

# Start bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())


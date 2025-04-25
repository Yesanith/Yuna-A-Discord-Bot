import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime, timezone
from termcolor import colored
from random import choice

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Mage Themed Configuration
MAGE_CONFIG = {
    "embed_color": 0x9b59b6,  # purple-ish
    "footer_text": "Arcane Mage • Guardian of the Ethereal",
    "status_messages": [
        "Channeling Arcane Energies",
        "Studying Ancient Grimoires",
        "Guarding the Mystic Realm"
    ]
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)
bot.config = MAGE_CONFIG  # accessible in cogs

# Custom log function
def arcane_log(message: str, color: str, icon: str = "✨"):
    timestamp = colored(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"), "cyan")
    print(f"{icon} {timestamp} | {colored(message, color)}")

@bot.event
async def on_ready():
    # record when bot became ready
    bot.start_time = datetime.now(timezone.utc)

    arcane_log(f"{bot.user} has awakened the Arcane Grimoire", "magenta", "🔮")

    await asyncio.sleep(2)
    try:
        synced = await bot.tree.sync()
        arcane_log(f"{len(synced)} arcane commands synchronized:", "cyan", "📜")
        for cmd in synced:
            arcane_log(f"- {cmd.name}", "white", "  ")
        # set initial status
        await bot.change_presence(activity=discord.Game(name=choice(MAGE_CONFIG["status_messages"])))
    except Exception as e:
        arcane_log(f"Command synchronization failed: {e}", "red", "⚠️")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    user = interaction.user
    arcane_log(
        f"Command {interaction.command.name} error for {user} ({user.id}): {error}",
        "red",
        "🔥"
    )

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                arcane_log(f"{filename[:-3]} familiar bonded", "green", "🧙‍♀️")
            except Exception as e:
                arcane_log(f"Failed to bond {filename}: {e}", "red", "❌")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
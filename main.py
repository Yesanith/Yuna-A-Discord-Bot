import discord
from discord.ext import commands
import os
import importlib
from pathlib import Path
from dotenv import load_dotenv
import asyncio
from datetime import datetime
from termcolor import colored
from random import choice

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Yuna Themed Configuration
YUNA_CONFIG = {
    "embed_color": 0x2ecc71,
    "footer_text": "Summoner Yuna • Spira's Guardian",
    "status_messages": [
        "Praying at Besaid Temple",
        "Dancing for the Fayth",
        "Guarding Spira from Sin"
    ]
}

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, help_command=None)

def ffx_log(message: str, color: str, icon: str = "🌀"):
    timestamp = colored(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "cyan")
    print(f"{icon} {timestamp} | {colored(message, color)}")

def load_commands():
    kommands_path = Path("./kommands")
    
    if not kommands_path.exists():
        kommands_path.mkdir()
        ffx_log("Aeon Archive initialized", "blue", "📚")

    for file in kommands_path.glob("*.py"):
        if file.name == "__init__.py":
            continue
            
        module_name = f"kommands.{file.stem}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "setup"):
                module.setup(bot, YUNA_CONFIG)
                ffx_log(f"{file.stem} Aeon bonded", "green", "✨")
            else:
                ffx_log(f"{file.stem} lacks Fayth connection", "yellow", "⚠️")
        except Exception as e:
            ffx_log(f"Aeon bond failed for {file.stem}: {str(e)}", "red", "💥")

@bot.event
async def on_ready():
    ffx_log(f"{bot.user} has answered Spira's call", "magenta", "🌟")
    
    load_commands()
    
    await asyncio.sleep(3)
    
    try:
        synced = await bot.tree.sync()
        ffx_log(f"{len(synced)} Aeon commands synchronized:", "cyan", "🔗")
        for cmd in synced:
            ffx_log(f"- {cmd.name}", "white", "  ")
        
        await bot.change_presence(activity=discord.Game(name=choice(YUNA_CONFIG["status_messages"])))
    except Exception as e:
        ffx_log(f"Aeon synchronization failed: {e}", "red", "⛔")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    log_time = datetime.now().strftime("%H:%M:%S")
    user = interaction.user
    ffx_log(
        f"Command {interaction.command.name} failed for {user} ({user.id}): {error}",
        "red",
        "💢"
    )

bot.run(TOKEN)
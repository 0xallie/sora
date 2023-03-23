import asyncio
import logging
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from platformdirs import PlatformDirs
from ruamel.yaml import YAML

from .cogs import ChatGPT, Embed, Logger, Moderation, Ping, Roles, Sync


def main() -> None:
    dirs = PlatformDirs("sora", appauthor=False)
    config = YAML().load(dirs.user_config_path / "config.yaml")

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix=config["prefix"], intents=intents)

    asyncio.run(bot.add_cog(ChatGPT(bot, config)))
    asyncio.run(bot.add_cog(Embed(config)))
    asyncio.run(bot.add_cog(Logger(config)))
    asyncio.run(bot.add_cog(Moderation(config)))
    asyncio.run(bot.add_cog(Ping(config)))
    asyncio.run(bot.add_cog(Roles(config)))
    asyncio.run(bot.add_cog(Sync(config)))

    bot.run(config["token"], log_level=logging.DEBUG)

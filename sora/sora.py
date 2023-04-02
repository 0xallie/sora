import asyncio
import logging

import discord
from discord.ext import commands
from platformdirs import PlatformDirs
from ruamel.yaml import YAML

from .cogs import AppleWiki, ChatGPT, Embed, IPInfo, Logger, Moderation, Ping, Rules, Say, Sync, Twitter


def main() -> None:
    dirs = PlatformDirs("sora", appauthor=False)
    config = YAML().load(dirs.user_config_path / "config.yaml")

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=config["prefix"],
        intents=intents,
        allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
    )

    asyncio.run(bot.add_cog(AppleWiki(bot, config)))
    asyncio.run(bot.add_cog(ChatGPT(bot, config)))
    asyncio.run(bot.add_cog(Embed(bot, config)))
    asyncio.run(bot.add_cog(IPInfo(bot, config)))
    asyncio.run(bot.add_cog(Logger(bot, config)))
    asyncio.run(bot.add_cog(Moderation(bot, config)))
    asyncio.run(bot.add_cog(Ping(bot, config)))
    asyncio.run(bot.add_cog(Rules(bot, config)))
    asyncio.run(bot.add_cog(Say(bot, config)))
    asyncio.run(bot.add_cog(Sync(bot, config)))
    asyncio.run(bot.add_cog(Twitter(bot, config)))

    bot.run(config["token"], log_level=logging.DEBUG)

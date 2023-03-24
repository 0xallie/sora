from __future__ import annotations

from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot, config: dict):
        self.bot = bot
        self.config = config


def pluralize(n: int, singular: str, plural: str | None = None) -> str:
    plural = plural or f"{singular}s"
    return singular if n == 1 else plural

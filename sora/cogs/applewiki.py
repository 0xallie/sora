import re

import aiohttp
import discord
from discord.ext import commands

from ..utils import Cog, pluralize


class AppleWiki(Cog):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        applewiki_urls = []

        async with aiohttp.ClientSession() as session:
            for article in re.findall(r"https?://(?:www\.)?theiphonewiki\.com/wiki/(\S+)", message.content):
                if article.upper().startswith(("/", "%2F")):
                    article = f"Filesystem:{article}"
                aw_url = f"https://theapplewiki.com/wiki/{article}"
                async with session.head(aw_url) as r:
                    if r.ok:
                        applewiki_urls.append(aw_url)

            for article in re.findall(
                r"https?://(?:www\.)?iphonedev(?:\.wiki|wiki\.net)/index\.php/(\S+)", message.content
            ):
                aw_url = f"https://theapplewiki.com/wiki/Dev:{article}"
                async with session.head(aw_url) as r:
                    if r.ok:
                        applewiki_urls.append(aw_url)

        if applewiki_urls:
            reply = (
                f"Found {pluralize(len(applewiki_urls), 'article')} on The Apple Wiki:\n"
                + "\n".join(applewiki_urls)
            )
            await message.reply(reply, suppress_embeds=True)

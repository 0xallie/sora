import json
import os
import re

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from ..utils import Cog


class Twitter(Cog, commands.GroupCog, group_name="twitter"):
    # Twitter Web App official client token
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"  # noqa: E501

    @app_commands.command()
    async def blue(self, interaction: discord.Interaction, username: str) -> None:
        """Get information about a Twitter user's verification status

        :param username: Username of target user
        """
        async with aiohttp.ClientSession() as session:
            # Get guest token
            async with session.get("https://twitter.com/home") as r:
                guest_token = re.findall(r"gt=(\d+)", await r.text())[0]

            csrf_token = os.urandom(16).hex()

            async with session.get(
                url="https://twitter.com/i/api/graphql/k26ASEiniqy4eXMdknTSoQ/UserByScreenName",
                params={
                    "variables": json.dumps({
                        "screen_name": username,
                        "withSafetyModeUserFields": True,
                    }),
                    "features": json.dumps({
                        "blue_business_profile_image_shape_enabled": False,
                        "responsive_web_graphql_exclude_directive_enabled": True,
                        "verified_phone_label_enabled": False,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                    }),
                },
                headers={
                    "Accept-Language": "en",
                    "Authorization": f"Bearer {self.BEARER_TOKEN}",
                    "x-csrf-token": csrf_token,
                    "x-guest-token": guest_token,
                },
                cookies={
                    "ct0": csrf_token,
                },
            ) as r:
                res = await r.json()

        try:
            data = res["data"]["user"]["result"]
        except KeyError:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    title="Error",
                    description=f"User `{discord.utils.escape_markdown(username)}` not found.",
                ),
                ephemeral=True,
            )

        try:
            description = data["verification_info"]["reason"]["description"]["text"].removesuffix(" Learn more")
        except KeyError:
            description = None

        legacy_verified = data["legacy"]["verified"]
        blue_verified = data["is_blue_verified"]
        verified_type = data["legacy"].get("verified_type")

        verified = bool(legacy_verified or blue_verified or verified_type)

        embed = discord.Embed(
            color=discord.Color.blue(),
            description=description,
        )
        embed.set_author(
            name=data["legacy"]["name"],
            url=f"https://twitter.com/{data['legacy']['screen_name']}",
            icon_url=data["legacy"]["profile_image_url_https"],
        )
        embed.add_field(
            name="Username",
            value=discord.utils.escape_markdown(f"@{data['legacy']['screen_name']}"),
            inline=False,
        ),
        embed.add_field(
            name="Verified",
            value=f":white_check_mark: {verified_type or 'Personal'}" if verified else ":x: No",
            inline=False,
        )
        embed.add_field(
            name="Legacy Verified",
            value=":white_check_mark: Yes" if data["legacy"]["verified"] else ":x: No",
            inline=False,
        )
        embed.add_field(
            name="Blue Verified",
            value=":white_check_mark: Yes" if data["is_blue_verified"] else ":x: No",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

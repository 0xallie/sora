import ipaddress

import aiohttp
import discord
from discord import app_commands

from ..utils import Cog


class IPInfo(Cog):
    @app_commands.command()
    async def ipinfo(self, interaction: discord.Interaction, ip: str) -> None:
        """Get information about an IP address

        :param ip: IP address
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    title="Error",
                    description="Invalid IP address.",
                ),
                ephemeral=True,
            )

        await interaction.response.defer()

        embed = discord.Embed(
            color=discord.Color.fuchsia(),
            title="IP Address Information",
        )

        async with aiohttp.ClientSession() as session:
            token = self.config.get("ipinfo_api_token")
            async with session.get(
                url=f"https://ipinfo.io/{ip}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token}" if token else "",
                },
            ) as r:
                res = await r.json()

        for k, v in res.items():
            if k == "readme":
                continue

            if k == "error":
                await interaction.response.send_message(
                    embed=discord.Embed(
                        color=discord.Color.red(),
                        title=f"Error [{res['status']}]",
                        description=v["title"],
                    ),
                    ephemeral=True,
                )
                return

            if k == "bogon":
                k = ""
                v = "This is a private IP address (bogon)."

            if k == "loc":
                v = v.replace(",", ", ")

            k = {
                "Ip": "IP",
                "Loc": "Location",
                "Org": "Organization",
                "Postal": "Postal code",
            }.get(k.title(), k.title())

            v = {
                True: "Yes",
                False: "No",
            }.get(v, str(v))

            embed.add_field(
                name=discord.utils.escape_markdown(k),
                value=discord.utils.escape_markdown(v),
                inline=bool(k),
            )

        await interaction.followup.send(embed=embed)

import time

import aiohttp
import discord
from discord import app_commands
from ..utils import Cog


class Pomelo(Cog):
    @app_commands.command()
    async def pomelo(self, interaction: discord.Interaction, username: str) -> None:
        """Check whether a Discord Pomelo username is available.

        :param username: Username to check
        """
        username = username.lower()

        async with aiohttp.ClientSession() as session:
            token = self.config.get("pomelo_token")
            if not token:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        color=discord.Color.red(),
                        title="Error",
                        description="No token configured.",
                    ),
                    ephemeral=True,
                )
                return

            await interaction.response.defer()

            while True:
                async with session.post(
                    url="https://discord.com/api/v9/users/@me/pomelo-attempt",
                    json={
                        "username": username,
                    },
                    headers={
                        "Authorization": token,
                    },
                ) as r:
                    res = await r.json()

                if "retry_after" in res:
                    time.sleep(res["retry_after"])
                else:
                    break

            if "errors" in res:
                try:
                    error = res["errors"]["username"]["_errors"][0]["message"]
                except LookupError:
                    error = "Error: `{discord.utils.escape_markdown(json.dumps(res['errors']))}`"

                embed = discord.Embed(
                    color=discord.Color.red(),
                    title=username,
                    description=error,
                )
            else:
                embed = discord.Embed(
                    color=discord.Color.green(),
                    title=username,
                    description="This username is available!",
                )

            await interaction.followup.send(embed=embed)

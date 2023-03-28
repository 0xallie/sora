from datetime import datetime
from typing import Optional

import discord
from discord import app_commands

from ..utils import Cog


class Say(Cog):
    @app_commands.command(description="Make the bot say something")
    async def say(self, interaction: discord.Interaction, message: str, channel: Optional[discord.TextChannel]) -> None:
        if interaction.user.id != self.config["owner_id"]:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="Permission denied.",
                ),
                ephemeral=True,
            )
            return

        channel = channel or interaction.channel
        await channel.send(message)

        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Done.",
            ),
            ephemeral=True,
        )

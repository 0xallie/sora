from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import Cog


class Embed(Cog):
    @app_commands.command(description="Post an embed")
    async def postembed(
        self,
        interaction: discord.Interaction,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[str] = None,
    ) -> None:
        if interaction.user.id != self.config["owner_id"]:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="Permission denied.",
                ),
                ephemeral=True,
            )
            return

        color_obj = None
        if color:
            color_obj = getattr(discord.Color, color.lower())
            if not callable(color_obj):
                if interaction.user.id != self.config["owner_id"]:
                    await interaction.response.send_message(
                        embed=discord.Embed(
                            color=discord.Color.red(),
                            title="Error",
                            description=f"Invalid color: `{discord.utils.escape_markdown(color)}`.",
                        ),
                        ephemeral=True,
                    )
                    return

        await interaction.channel.send(
            embed=discord.Embed(
                color=color_obj(),
                title=title,
                description=description,
            ),
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Embed posted.",
            ),
            ephemeral=True,
        )

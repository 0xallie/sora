from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from ..utils import Cog, pluralize


class Moderation(Cog):
    @app_commands.command(description="Purge the specified amount of messages from the channel")
    async def purge(self, interaction: discord.Interaction, count: int) -> None:
        if not interaction.channel.permissions_for(interaction.user).manage_messages:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    title="Permission denied",
                    description="You must have the `Manage Messages` permission in the channel to use this command.",
                ),
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        purged = await interaction.channel.purge(limit=count, before=interaction.created_at)

        await interaction.followup.send(
            embed=discord.Embed(
                color=discord.Color.green(),
                description=f"Purged {len(purged)} {pluralize(len(purged), 'message')}.",
            ),
        )


from datetime import datetime
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, config: dict):
        self.config = config

    @app_commands.command(description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction) -> None:
        embed=discord.Embed(
            color=discord.Color.green(),
            title="Pong!",
        )
        embed.add_field(
            name="Message latency",
            value="Calculating...",
        )
        embed.add_field(
            name="API latency",
            value="Calculating...",
        )

        start = datetime.utcnow()
 
        await interaction.response.send_message(
            embed=embed,
            ephemeral=interaction.channel.id != self.config["channels"]["bot_commands"],
        )

        embed.clear_fields()
        embed.add_field(
            name="Message latency",
            value=f"{(datetime.utcnow() - start).total_seconds() * 1000:.0f} ms",
        )
        embed.add_field(
            name="API latency",
            value=f"{interaction.client.latency * 1000:.0f} ms",
        )
        await interaction.edit_original_response(embed=embed)

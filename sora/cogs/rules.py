import discord
from discord import app_commands

from ..utils import Cog


class Rules(Cog):
    @app_commands.command()
    async def postrules(self, interaction: discord.Interaction) -> None:
        """Post the server's rules"""
        if interaction.user.id != self.config["owner_id"]:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="Permission denied.",
                ),
                ephemeral=True,
            )
            return

        if not (rules := self.config.get("rules")):
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="No rules are configured for this server.",
                ),
                ephemeral=True,
            )
            return

        await interaction.channel.send(
            embeds=[discord.Embed(
                color=discord.Color.fuchsia(),
                title=f"Rule {i + 1}",
                description=rule,
            ) for i, rule in enumerate(rules)]
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Done.",
            ),
            ephemeral=True,
        )

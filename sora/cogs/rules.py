import discord
from discord import app_commands
from discord.ext import commands

from ..utils import Cog


class Rules(Cog):
    @app_commands.command(description="Post rules")
    async def postrules(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.config["owner_id"]:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="Permission denied.",
                ),
                ephemeral=True,
            )
            return

        await interaction.channel.send(
            embeds=[
                discord.Embed(
                    color=discord.Color.fuchsia(),
                    title="Rule 1",
                    description=(
                        "Be nice. Swearing is allowed, but try not to insult people. "
                        "A little banter is fine, but if someone is uncomfortable with it, please stop."
                    ),
                ),
                discord.Embed(
                    color=discord.Color.fuchsia(),
                    title="Rule 2",
                    description="No racism, sexism, homophobia, transphobia, ableism or other bigotry.",
                ),
                discord.Embed(
                    color=discord.Color.fuchsia(),
                    title="Rule 3",
                    description=(
                        "Keep NSFW content to a minimum. "
                        "Only mild NSFW is allowed and it must be spoilered."
                    ),
                ),
                discord.Embed(
                    color=discord.Color.fuchsia(),
                    title="Rule 4",
                    description="If you post potentially sensitive/triggering content, please spoiler it.",
                ),
            ]
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Posted rules.",
            ),
            ephemeral=True,
        )

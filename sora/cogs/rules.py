import discord
from discord import app_commands

from ..utils import Cog


class Rules(Cog):
    @app_commands.command()
    async def postrules(self, interaction: discord.Interaction) -> None:
        """Post rules"""
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
                        "Only mild NSFW is allowed, and any NSFW media must be spoilered."
                    ),
                ),
                discord.Embed(
                    color=discord.Color.fuchsia(),
                    title="Rule 4",
                    description=(
                        f"Avoid excessive spam outside <#{self.config['channels']['bot_commands']}> "
                        f"or the appropriate channels."
                    ),
                ),
                discord.Embed(
                    color=discord.Color.fuchsia(),
                    title="Rule 5",
                    description="If you post potentially sensitive/triggering content, please spoiler it.",
                ),
                discord.Embed(
                    color=discord.Color.fuchsia(),
                    title="Rule 6",
                    description="Please don't invite anyone without my permission.",
                ),

            ]
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Done.",
            ),
            ephemeral=True,
        )

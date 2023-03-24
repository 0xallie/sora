import discord
from discord import app_commands
from discord.ext import commands

from ..utils import Cog


class Roles(Cog):
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction) -> None:
        if "custom_id" not in interaction.data:
            return

        event, data = interaction.data["custom_id"].split(":")

        if event == "toggle_role":
            role = interaction.guild.get_role(self.config["assignable_roles"][data])

            if role not in interaction.user.roles:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        color=discord.Color.green(),
                        description=f"You have been given the `{discord.utils.escape_markdown(role.name)}` role.",
                    ),
                    ephemeral=True,
                )
            else:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(
                    embed=discord.Embed(
                        color=discord.Color.green(),
                        description=f"Your `{discord.utils.escape_markdown(role.name)}` role has been removed.",
                    ),
                    ephemeral=True,
                )

    @app_commands.command(description="Post role buttons")
    async def postroles(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.config["owner_id"]:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="Permission denied.",
                ),
                ephemeral=True,
            )
            return

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                row=1,
                label="he/him",
                style=discord.ButtonStyle.primary,
                custom_id="toggle_role:pronouns_he_him",
            )
        )
        view.add_item(
            discord.ui.Button(
                row=1,
                label="she/her",
                style=discord.ButtonStyle.primary,
                custom_id="toggle_role:pronouns_she_her",
            )
        )
        view.add_item(
            discord.ui.Button(
                row=1,
                label="they/them",
                style=discord.ButtonStyle.primary,
                custom_id="toggle_role:pronouns_they_them",
            )
        )
        view.add_item(
            discord.ui.Button(
                row=2,
                label="Any",
                style=discord.ButtonStyle.secondary,
                custom_id="toggle_role:pronouns_any",
            )
        )
        view.add_item(
            discord.ui.Button(
                row=2,
                label="Ask me",
                style=discord.ButtonStyle.secondary,
                custom_id="toggle_role:pronouns_ask_me",
            )
        )
        await interaction.channel.send(
            embed=discord.Embed(
                color=discord.Color.fuchsia(),
                title="Pronouns",
                description="\n\n".join([
                    f"Choose your preferred pronouns using the buttons below.",
                    #f"If you would like more pronouns to be added, please contact <@{self.config['owner_id']}>.",
                ]),
            ),
            view=view,
        )

        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                row=1,
                label="tree ping",
                style=discord.ButtonStyle.primary,
                custom_id="toggle_role:ping_tree",
            )
        )
        await interaction.channel.send(
            embed=discord.Embed(
                color=discord.Color.fuchsia(),
                title="Ping roles",
                description="\n\n".join([
                    f"Choose what you would like to be pinged for.",
                ]),
            ),
            view=view,
        )

        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Posted role buttons.",
            ),
            ephemeral=True,
        )

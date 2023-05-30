import aiohttp
import discord
from discord import app_commands

from ..utils import Cog


class PronounDB(Cog):
    PRONOUN_MAP = {
        "he": "he/him",
        "it": "it/its",
        "she": "she/her",
        "they": "they/them",
        "any": "Any pronouns",
        "ask": "Ask me my pronouns",
        "avoid": "Avoid pronouns, use my name",
        "other": "Other pronouns",
    }

    @app_commands.command()
    async def pronouns(self, interaction: discord.Interaction, user: discord.User) -> None:
        """Get a Discord user's pronouns via PronounDB

        :param user: User to get pronouns of
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url="https://pronoundb.org/api/v2/lookup",
                params={
                    "platform": "discord",
                    "ids": user.id,
                },
            ) as r:
                res = await r.json()

        pronouns = res.get(str(user.id), {}).get("sets", {}).get("en", [])

        if not pronouns:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description=f"{user.mention} does not have pronouns set on PronounDB.",
                ),
                ephemeral=True,
            )
            return

        embed = discord.Embed(color=discord.Color.fuchsia())
        embed.add_field(
            name="Pronouns",
            value=", ".join(self.PRONOUN_MAP[x] for x in pronouns),
        )
        embed.set_author(
            name=str(user),
            icon_url=user.avatar.url if user.avatar else None,
            url=f"https://discord.com/users/{user.id}",
        )
        embed.set_footer(text="Data provided by PronounDB")

        await interaction.response.send_message(embed=embed)

import aiohttp
import discord
from discord import app_commands

from ..utils import Cog


class PronounDB(Cog):
    PRONOUN_MAP = {
        "unspecified": "Unspecified",
        "hh": "he/him",
        "hi": "he/it",
        "hs": "he/she",
        "ht": "he/they",
        "ih": "it/he",
        "ii": "it/its",
        "is": "it/she",
        "it": "it/they",
        "shh": "she/he",
        "sh": "she/her",
        "si": "she/it",
        "st": "she/they",
        "th": "they/he",
        "ti": "they/it",
        "ts": "they/she",
        "tt": "they/them",
        "any": "Any pronouns",
        "other": "Other pronouns",
        "ask": "Ask me my pronouns",
        "avoid": "Avoid pronouns, use my name",
    }

    @app_commands.command()
    async def pronouns(self, interaction: discord.Interaction, user: discord.User) -> None:
        """Get a Discord user's pronouns via PronounDB

        :param user: User to get pronouns of
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url="https://pronoundb.org/api/v1/lookup",
                params={
                    "platform": "discord",
                    "id": user.id,
                },
            ) as r:
                res = await r.json()

        if res["pronouns"] == "unspecified":
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description=f"{user.mention} does not have pronouns set on PronounDB.",
                ),
                ephemeral=True,
            )
            return

        try:
            pronouns = self.PRONOUN_MAP[res["pronouns"]]
        except KeyError:
            await interaction.response.send_message(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    description="An unexpected response was returned by PronounDB.",
                ),
                ephemeral=True,
            )
            return

        embed = discord.Embed(color=discord.Color.fuchsia())
        embed.add_field(
            name="Pronouns",
            value=pronouns,
        )
        embed.set_author(
            name=f"{user.name}#{user.discriminator}",
            icon_url=user.avatar.url if user.avatar else None,
            url=f"https://discord.com/users/{user.id}",
        )
        embed.set_footer(text="Data provided by PronounDB")

        await interaction.response.send_message(embed=embed)

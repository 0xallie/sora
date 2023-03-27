import discord
from discord.ext import commands

from ..utils import Cog


class Sync(Cog):
    @commands.command(name="sync", description="Sync slash commands")
    async def sync(self, ctx: commands.Context) -> None:
        if ctx.author.id != self.config["owner_id"]:
            await ctx.reply(
                embed=discord.Embed(
                    color=discord.Color.red(),
                    title="Error",
                    description="Permission denied.",
                ),
            )
            return

        #await ctx.bot.tree.sync(guild=discord.Object(self.config["main_guild_id"]))
        await ctx.bot.tree.sync()

        await ctx.reply(
            embed=discord.Embed(
                color=discord.Color.green(),
                description="Synced slash commands.",
            )
        )

import textwrap

import discord
from discord.ext import commands

from ..utils import Cog, pluralize


class Logger(Cog):
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        log_channel = member.guild.get_channel(self.config["channels"]["private_logs"])

        embed = discord.Embed(
            color=discord.Color.green(),
            title="Member Joined",
        )
        embed.add_field(
            name="User",
            value=f"{discord.utils.escape_markdown(str(member))} ({member.mention})",
        )
        embed.add_field(
            name="Created",
            value=f"<t:{int(member.created_at.timestamp())}:R>",
        )

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        log_channel = member.guild.get_channel(self.config["channels"]["private_logs"])

        embed = discord.Embed(
            color=discord.Color.red(),
            title="Member Left",
        )
        embed.add_field(
            name="User",
            value=f"{discord.utils.escape_markdown(str(member))} ({member.mention})",
        )
        embed.add_field(
            name="Joined",
            value=f"<t:{int(member.joined_at.timestamp())}:R>",
        )

        got_audit_log_entry = False
        async for entry in member.guild.audit_logs(action=discord.AuditLogAction.ban, limit=1, after=member.joined_at):
            if entry.target.id == member.id:
                mod = entry.user
                embed.add_field(
                    name="Banned by",
                    value=f"{discord.utils.escape_markdown(str(mod))} ({mod.mention})",
                    inline=False,
                )
                got_audit_log_entry = True
            break
        if not got_audit_log_entry:
            async for entry in member.guild.audit_logs(
                action=discord.AuditLogAction.kick, limit=1, after=member.joined_at
            ):
                if entry.target.id == member.id:
                    mod = entry.user
                    embed.add_field(
                        name="Kicked by",
                        value=f"{discord.utils.escape_markdown(str(mod))} ({mod.mention})",
                        inline=False,
                    )
                    got_audit_log_entry = True
                break

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        log_channel = before.guild.get_channel(self.config["channels"]["private_logs"])

        embed = discord.Embed(
            color=discord.Color.orange(),
            title="Member Updated",
        )
        embed.add_field(
            name="User",
            value=f"{discord.utils.escape_markdown(str(before))} ({before.mention})",
            inline=False,
        )

        if before.nick != after.nick:
            embed.add_field(
                name="Old nickname",
                value=discord.utils.escape_markdown(before.nick or before.name),
                inline=True,
            )
            embed.add_field(
                name="New nickname",
                value=discord.utils.escape_markdown(after.nick or after.name),
                inline=True,
            )

        all_roles = set(before.roles) | set(after.roles)
        if added_roles := all_roles - set(before.roles):
            embed.add_field(
                name=f"{pluralize(len(added_roles), 'Role')} added",
                value=" ".join(x.mention for x in sorted(added_roles)),
                inline=True,
            )
        if removed_roles := all_roles - set(after.roles):
            embed.add_field(
                name=f"{pluralize(len(removed_roles), 'Role')} removed",
                value=" ".join(x.mention for x in sorted(removed_roles)),
                inline=True,
            )

        if len(embed.fields) <= 1:
            return

        if added_roles or removed_roles:
            async for entry in before.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):
                if entry.target.id == before.id:
                    embed.add_field(
                        name="Updated by",
                        value=f"{discord.utils.escape_markdown(str(entry.user))} ({entry.user.mention})",
                        inline=False,
                    )
                break
        else:
            async for entry in before.guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
                if entry.target.id == before.id:
                    embed.add_field(
                        name="Updated by",
                        value=f"{discord.utils.escape_markdown(str(entry.user))} ({entry.user.mention})",
                        inline=False,
                    )
                break

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        log_channel = message.guild.get_channel(self.config["channels"]["private_logs"])

        if message.channel == log_channel or not message.content:
            return

        embed = discord.Embed(
            color=discord.Color.red(),
            title="Message Deleted",
        )
        embed.add_field(
            name="User",
            value=f"{discord.utils.escape_markdown(str(message.author))} ({message.author.mention})",  # noqa: E501
        )
        embed.add_field(
            name="Channel",
            value=message.channel.mention,
        )
        embed.add_field(
            name="Message",
            value=textwrap.shorten(message.content, width=1024, placeholder="..."),
            inline=False,
        )

        async for entry in message.guild.audit_logs(
            action=discord.AuditLogAction.message_delete, limit=1, after=message.created_at
        ):
            if entry.target.id == message.id:
                embed.add_field(
                    name="Deleted by",
                    value=f"{discord.utils.escape_markdown(str(entry.user))} ({entry.user.mention})",
                    inline=False,
                )
            break

        embed.add_field(
            name="",
            value=f"[Link to message](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})",  # noqa: E501
            inline=False,
        )

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        log_channel = before.guild.get_channel(self.config["channels"]["private_logs"])

        if before.channel == log_channel or before.author.bot or before.content == after.content:
            return

        embed = discord.Embed(
            color=discord.Color.orange(),
            title="Message Edited",
        )
        embed.add_field(
            name="User",
            value=f"{discord.utils.escape_markdown(str(before.author))} ({before.author.mention})",
        )
        embed.add_field(
            name="Channel",
            value=before.channel.mention,
        )
        embed.add_field(
            name="Old message",
            value=textwrap.shorten(before.content, width=1024, placeholder="..."),
            inline=False,
        )
        embed.add_field(
            name="New message",
            value=textwrap.shorten(after.content, width=1024, placeholder="..."),
        )
        embed.add_field(
            name="",
            value=f"[Link to message](https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id})",
            inline=False,
        )

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User) -> None:
        log_channel = self.bot.get_channel(self.config["channels"]["private_logs"])

        embed = discord.Embed(
            color=discord.Color.orange(),
            title="User Updated",
        )
        embed.add_field(
            name="User",
            value=before.mention,
            inline=False,
        )

        if str(before) != str(after):
            embed.add_field(
                name="Old username",
                value=discord.utils.escape_markdown(str(before)),
                inline=True,
            )
            embed.add_field(
                name="New username",
                value=discord.utils.escape_markdown(str(after)),
                inline=True,
            )

        if len(embed.fields) > 1:
            await log_channel.send(embed=embed)

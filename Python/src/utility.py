# utility.py
import asyncio
import discord
import json
import os

class UtilityActions:
    def __init__(self, bot):
        self.bot = bot

    async def mass_delete_messages(self, guild_id, channel_id, message_count):
        """
        Delete a specified number of messages in a channel.
        
        Parameters:
        - guild_id: The ID of the guild.
        - channel_id: The ID of the channel to delete messages from.
        - message_count: Number of messages to delete.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found in guild {guild_id}.")
            return

        try:
            async for message in channel.history(limit=message_count):
                try:
                    await message.delete()
                    print(f"Deleted message in channel {channel.name} in guild {guild_id}")
                    await asyncio.sleep(0.5)  # Rate limiting
                except Exception as e:
                    print(f"Failed to delete message: {e}")
        except Exception as e:
            print(f"Error during mass_delete_messages: {e}")
            raise

    async def get_server_info(self, guild_id):
        """
        Retrieve and display information about a server.
        
        Parameters:
        - guild_id: The ID of the guild.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        try:
            info = (
                f"Server Name: {guild.name}\n"
                f"Server ID: {guild.id}\n"
                f"Member Count: {guild.member_count}\n"
                f"Owner: {guild.owner}\n"
                f"Created At: {guild.created_at}\n"
                f"Channels: {len(guild.channels)}\n"
                f"Roles: {len(guild.roles)}\n"
                f"Emojis: {len(guild.emojis)}\n"
                f"Region: {guild.region if hasattr(guild, 'region') else 'N/A'}\n"
            )
            print(f"Server Info for Guild ID {guild_id}:\n{info}")
        except Exception as e:
            print(f"Error during get_server_info: {e}")
            raise

    async def get_user_info(self, guild_id, user_id):
        """
        Retrieve and display information about a user in a server.
        
        Parameters:
        - guild_id: The ID of the guild.
        - user_id: The ID of the user.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        member = guild.get_member(user_id)
        if not member:
            print(f"User {user_id} not found in guild {guild_id}.")
            return

        try:
            info = (
                f"User Name: {member.name}\n"
                f"User ID: {member.id}\n"
                f"Joined At: {member.joined_at}\n"
                f"Roles: {', '.join([role.name for role in member.roles])}\n"
                f"Status: {member.status}\n"
                f"Top Role: {member.top_role.name}\n"
                f"Nickname: {member.nick if member.nick else 'None'}\n"
            )
            print(f"User Info for User ID {user_id} in Guild ID {guild_id}:\n{info}")
        except Exception as e:
            print(f"Error during get_user_info: {e}")
            raise

    async def assign_role(self, guild_id, user_id, role_id):
        """
        Assign a role to a user in a server.
        
        Parameters:
        - guild_id: The ID of the guild.
        - user_id: The ID of the user.
        - role_id: The ID of the role to assign.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        member = guild.get_member(user_id)
        if not member:
            print(f"User {user_id} not found in guild {guild_id}.")
            return

        role = guild.get_role(role_id)
        if not role:
            print(f"Role {role_id} not found in guild {guild_id}.")
            return

        try:
            await member.add_roles(role)
            print(f"Assigned role {role.name} to user {member.name} in guild {guild_id}")
        except Exception as e:
            print(f"Error during assign_role: {e}")
            raise

    async def manage_channel_permissions(self, guild_id, channel_id, action):
        """
        Lock or unlock a channel by modifying permissions.
        
        Parameters:
        - guild_id: The ID of the guild.
        - channel_id: The ID of the channel.
        - action: Either "lock" or "unlock".
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        channel = guild.get_channel(channel_id)
        if not channel:
            print(f"Channel {channel_id} not found in guild {guild_id}.")
            return

        try:
            if action == "lock":
                await channel.set_permissions(guild.default_role, send_messages=False, view_channel=True)
                print(f"Locked channel {channel.name} in guild {guild_id}")
            elif action == "unlock":
                await channel.set_permissions(guild.default_role, send_messages=True, view_channel=True)
                print(f"Unlocked channel {channel.name} in guild {guild_id}")
        except Exception as e:
            print(f"Error during manage_channel_permissions: {e}")
            raise

    async def backup_server(self, guild_id):
        """
        Create a backup of the server's structure (roles, channels, categories).
        
        Parameters:
        - guild_id: The ID of the guild to back up.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        try:
            backup_data = {
                "name": guild.name,
                "roles": [],
                "categories": [],
                "channels": []
            }

            # Backup roles (excluding @everyone)
            for role in guild.roles:
                if role.name != "@everyone":
                    role_data = {
                        "name": role.name,
                        "color": role.color.to_rgb(),
                        "permissions": role.permissions.value,
                        "position": role.position
                    }
                    backup_data["roles"].append(role_data)

            # Backup categories and channels
            for category in guild.categories:
                category_data = {
                    "name": category.name,
                    "position": category.position,
                    "channels": []
                }
                for channel in category.channels:
                    channel_data = {
                        "name": channel.name,
                        "type": str(channel.type),
                        "position": channel.position
                    }
                    category_data["channels"].append(channel_data)
                backup_data["categories"].append(category_data)

            # Backup channels not in categories
            for channel in guild.channels:
                if not channel.category:
                    channel_data = {
                        "name": channel.name,
                        "type": str(channel.type),
                        "position": channel.position
                    }
                    backup_data["channels"].append(channel_data)

            # Save backup to a file
            backup_file = f"backup_{guild_id}.json"
            with open(backup_file, "w") as f:
                json.dump(backup_data, f, indent=4)
            print(f"Server backup created for Guild ID {guild_id} at {backup_file}")

        except Exception as e:
            print(f"Error during backup_server: {e}")
            raise

    async def restore_server(self, guild_id, backup_file):
        """
        Restore a server from a backup file.
        
        Parameters:
        - guild_id: The ID of the guild to restore.
        - backup_file: Path to the backup file.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        if not os.path.exists(backup_file):
            print(f"Backup file {backup_file} not found.")
            return

        try:
            # Load backup data
            with open(backup_file, "r") as f:
                backup_data = json.load(f)

            # Clear existing roles (except @everyone)
            for role in guild.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                        print(f"Deleted role {role.name} in guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to delete role {role.name}: {e}")

            # Clear existing channels
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(f"Deleted channel {channel.name} in guild {guild_id}")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Failed to delete channel {channel.name}: {e}")

            # Restore roles
            for role_data in sorted(backup_data["roles"], key=lambda x: x["position"]):
                try:
                    role = await guild.create_role(
                        name=role_data["name"],
                        color=discord.Color.from_rgb(*role_data["color"]),
                        permissions=discord.Permissions(role_data["permissions"])
                    )
                    print(f"Restored role {role.name} in guild {guild_id}")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Failed to restore role {role_data['name']}: {e}")

            # Restore categories and their channels
            for category_data in sorted(backup_data["categories"], key=lambda x: x["position"]):
                try:
                    category = await guild.create_category(category_data["name"])
                    print(f"Restored category {category.name} in guild {guild_id}")
                    await asyncio.sleep(0.5)

                    for channel_data in sorted(category_data["channels"], key=lambda x: x["position"]):
                        try:
                            if channel_data["type"] == "text":
                                await guild.create_text_channel(channel_data["name"], category=category)
                            elif channel_data["type"] == "voice":
                                await guild.create_voice_channel(channel_data["name"], category=category)
                            print(f"Restored channel {channel_data['name']} in category {category.name} in guild {guild_id}")
                            await asyncio.sleep(0.5)
                        except Exception as e:
                            print(f"Failed to restore channel {channel_data['name']}: {e}")
                except Exception as e:
                    print(f"Failed to restore category {category_data['name']}: {e}")

            # Restore channels not in categories
            for channel_data in sorted(backup_data["channels"], key=lambda x: x["position"]):
                try:
                    if channel_data["type"] == "text":
                        await guild.create_text_channel(channel_data["name"])
                    elif channel_data["type"] == "voice":
                        await guild.create_voice_channel(channel_data["name"])
                    print(f"Restored channel {channel_data['name']} in guild {guild_id}")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Failed to restore channel {channel_data['name']}: {e}")

            print(f"Server restore completed for Guild ID {guild_id} from {backup_file}")

        except Exception as e:
            print(f"Error during restore_server: {e}")
            raise

    async def mass_create_roles(self, guild_id, role_count, role_prefix="Utility-Role"):
        """
        Create multiple roles in a server.
        
        Parameters:
        - guild_id: The ID of the guild.
        - role_count: Number of roles to create.
        - role_prefix: Prefix for the role names.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        try:
            for i in range(role_count):
                try:
                    await guild.create_role(name=f"{role_prefix}-{i}")
                    print(f"Created role {role_prefix}-{i} in guild {guild_id}")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"Failed to create role {role_prefix}-{i}: {e}")
        except Exception as e:
            print(f"Error during mass_create_roles: {e}")
            raise

    async def mass_delete_roles(self, guild_id):
        """
        Delete all roles in a server (except @everyone).
        
        Parameters:
        - guild_id: The ID of the guild.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        try:
            for role in guild.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                        print(f"Deleted role {role.name} in guild {guild_id}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"Failed to delete role {role.name}: {e}")
        except Exception as e:
            print(f"Error during mass_delete_roles: {e}")
            raise

    async def export_member_list(self, guild_id):
        """
        Export a list of members in a server to a file.
        
        Parameters:
        - guild_id: The ID of the guild.
        """
        guild = self.bot.bot.get_guild(guild_id)
        if not guild:
            print(f"Guild {guild_id} not found.")
            return

        try:
            members_data = []
            for member in guild.members:
                member_data = {
                    "name": member.name,
                    "id": member.id,
                    "joined_at": str(member.joined_at),
                    "roles": [role.name for role in member.roles]
                }
                members_data.append(member_data)

            # Save member list to a file
            export_file = f"members_{guild_id}.json"
            with open(export_file, "w") as f:
                json.dump(members_data, f, indent=4)
            print(f"Member list exported for Guild ID {guild_id} to {export_file}")

        except Exception as e:
            print(f"Error during export_member_list: {e}")
            raise
import customtkinter as ctk
import tkinter as tk
from bot import DiscordSelfBot
from actions import BotActions
from premium import PremiumActions
from utility import UtilityActions
import threading
import asyncio
import time
from PIL import Image, ImageTk
import os

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Self-Bot - Raid Machine")
        self.root.geometry("1000x700")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.bot = None
        self.actions = None
        self.premium_actions = None
        self.utility_actions = None
        self.global_guild_id = None
        self.bot_thread = None
        self.bot_running = False
        self.is_premium = False

        # Main frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#FFFFFF")
        self.main_frame.pack(fill="both", expand=True)

        # Logo
        self.logo_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF")
        self.logo_frame.pack(fill="x", pady=10)
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((200, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = ctk.CTkLabel(self.logo_frame, image=self.logo_photo, text="")
            self.logo_label.pack()
        except Exception as e:
            print(f"Failed to load logo.png: {e}")

        # Top menu
        self.menu_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF", height=40)
        self.menu_frame.pack(fill="x")

        self.raid_btn = ctk.CTkButton(self.menu_frame, text="Raid", command=self.show_raiding, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", width=100, border_width=1, border_color="#D3D3D3", state="disabled", hover=False)
        self.raid_btn.pack(side="left", padx=2)

        self.nuke_btn = ctk.CTkButton(self.menu_frame, text="Nuke", command=self.show_nuking, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", width=100, border_width=1, border_color="#D3D3D3", state="disabled", hover=False)
        self.nuke_btn.pack(side="left", padx=2)

        self.spam_btn = ctk.CTkButton(self.menu_frame, text="Spam", command=self.show_spamming, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", width=100, border_width=1, border_color="#D3D3D3", state="disabled", hover=False)
        self.spam_btn.pack(side="left", padx=2)

        self.premium_btn = ctk.CTkButton(self.menu_frame, text="Premium", command=self.show_premium, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", width=100, border_width=1, border_color="#D3D3D3", state="disabled", hover=False)
        self.premium_btn.pack(side="left", padx=2)

        self.utility_btn = ctk.CTkButton(self.menu_frame, text="Utility", command=self.show_utility, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", width=100, border_width=1, border_color="#D3D3D3", state="disabled", hover=False)
        self.utility_btn.pack(side="left", padx=2)

        self.settings_btn = ctk.CTkButton(self.menu_frame, text="Settings", command=self.show_settings, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", width=100, border_width=1, border_color="#D3D3D3", state="normal", hover=True)
        self.settings_btn.pack(side="left", padx=2)

        # Status and Stop Action
        self.status_frame = ctk.CTkFrame(self.menu_frame, fg_color="#FFFFFF")
        self.status_frame.pack(side="right", padx=5)

        self.stop_action_btn = ctk.CTkButton(self.status_frame, text="Stop Action", command=self.stop_action, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", width=100, border_width=1, border_color="#D3D3D3")
        self.stop_action_btn.pack(side="right", padx=5)

        self.status_label = ctk.CTkLabel(self.status_frame, text="Bot Offline - Waiting to Start", font=("Helvetica", 12), text_color="red")
        self.status_label.pack(side="right", padx=5)

        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF")
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Footer
        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF", height=20)
        self.footer_frame.pack(side="bottom", fill="x")
        self.footer_label = ctk.CTkLabel(self.footer_frame, text="Powered By Devdo Hacks | Credits To xyzsworld & The Owner Of Project Sol!", font=("Helvetica", 10), text_color="#000000")
        self.footer_label.pack(anchor="center", pady=5)

        # Initialize section frames
        self.nuking_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.raiding_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.spamming_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.premium_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.utility_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")
        self.settings_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFFFFF")

        # Nuking Section (two columns)
        self.nuking_left = ctk.CTkFrame(self.nuking_frame, fg_color="#FFFFFF")
        self.nuking_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.nuking_right = ctk.CTkFrame(self.nuking_frame, fg_color="#FFFFFF")
        self.nuking_right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Nuking Left
        self.nuking_label = ctk.CTkLabel(self.nuking_left, text="Nuking", font=("Helvetica", 14, "bold"), text_color="#000000")
        self.nuking_label.pack(anchor="w", padx=10, pady=5)

        self.nuking_guild_id_label = ctk.CTkLabel(self.nuking_left, text="Guild ID:", font=("Helvetica", 12), text_color="#000000")
        self.nuking_guild_id_label.pack(anchor="w", padx=10, pady=5)

        self.nuking_guild_id_entry = ctk.CTkEntry(self.nuking_left, width=200, placeholder_text="Enter Guild ID", border_color="#D3D3D3")
        self.nuking_guild_id_entry.pack(anchor="w", padx=10, pady=5)

        self.nuke_check = ctk.CTkCheckBox(self.nuking_left, text="Enable Nuke", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.nuke_check.pack(anchor="w", padx=10, pady=5)

        self.role_create_frame = ctk.CTkFrame(self.nuking_left, fg_color="#FFFFFF")
        self.role_create_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.role_create_check = ctk.CTkCheckBox(self.role_create_frame, text="Create Roles", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.role_create_check.pack(side="left")
        self.role_create_btn = ctk.CTkButton(self.role_create_frame, text="Execute", command=self.execute_create_roles, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.role_create_btn.pack(side="right")
        self.role_count_entry = ctk.CTkEntry(self.nuking_left, width=100, placeholder_text="Number of Roles", border_color="#D3D3D3")
        self.role_count_entry.pack(anchor="w", padx=20, pady=2)

        self.channel_create_frame = ctk.CTkFrame(self.nuking_left, fg_color="#FFFFFF")
        self.channel_create_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.channel_create_check = ctk.CTkCheckBox(self.channel_create_frame, text="Create Channels", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.channel_create_check.pack(side="left")
        self.channel_create_btn = ctk.CTkButton(self.channel_create_frame, text="Execute", command=self.execute_create_channels, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.channel_create_btn.pack(side="right")
        self.channel_count_entry = ctk.CTkEntry(self.nuking_left, width=100, placeholder_text="Number of Channels", border_color="#D3D3D3")
        self.channel_count_entry.pack(anchor="w", padx=20, pady=2)

        self.category_create_frame = ctk.CTkFrame(self.nuking_left, fg_color="#FFFFFF")
        self.category_create_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.category_create_check = ctk.CTkCheckBox(self.category_create_frame, text="Create Categories", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.category_create_check.pack(side="left")
        self.category_create_btn = ctk.CTkButton(self.category_create_frame, text="Execute", command=self.execute_create_categories, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.category_create_btn.pack(side="right")
        self.category_count_entry = ctk.CTkEntry(self.nuking_left, width=100, placeholder_text="Number of Categories", border_color="#D3D3D3")
        self.category_count_entry.pack(anchor="w", padx=20, pady=2)

        self.ban_all_frame = ctk.CTkFrame(self.nuking_left, fg_color="#FFFFFF")
        self.ban_all_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.ban_all_check = ctk.CTkCheckBox(self.ban_all_frame, text="Ban All Members", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.ban_all_check.pack(side="left")
        self.ban_all_btn = ctk.CTkButton(self.ban_all_frame, text="Execute", command=self.execute_ban_all, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.ban_all_btn.pack(side="right")

        # Add Execute All Nuke Actions button in Nuking Left
        self.execute_all_nuke_btn = ctk.CTkButton(self.nuking_left, text="Execute All Nuke Actions", command=self.execute_all_nuke_actions, corner_radius=0, fg_color="#FF0000", hover_color="#CC0000", text_color="#FFFFFF", border_width=1, border_color="#D3D3D3", width=200)
        self.execute_all_nuke_btn.pack(anchor="w", padx=10, pady=10)

        # Nuking Right
        self.delete_channels_frame = ctk.CTkFrame(self.nuking_right, fg_color="#FFFFFF")
        self.delete_channels_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.delete_channels_check = ctk.CTkCheckBox(self.delete_channels_frame, text="Delete All Channels", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.delete_channels_check.pack(side="left")
        self.delete_channels_btn = ctk.CTkButton(self.delete_channels_frame, text="Execute", command=self.execute_delete_channels, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.delete_channels_btn.pack(side="right")

        self.delete_roles_frame = ctk.CTkFrame(self.nuking_right, fg_color="#FFFFFF")
        self.delete_roles_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.delete_roles_check = ctk.CTkCheckBox(self.delete_roles_frame, text="Delete All Roles", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.delete_roles_check.pack(side="left")
        self.delete_roles_btn = ctk.CTkButton(self.delete_roles_frame, text="Execute", command=self.execute_delete_roles, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.delete_roles_btn.pack(side="right")

        self.clone_server_frame = ctk.CTkFrame(self.nuking_right, fg_color="#FFFFFF")
        self.clone_server_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.clone_server_check = ctk.CTkCheckBox(self.clone_server_frame, text="Clone Server", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.clone_server_check.pack(side="left")
        self.clone_server_btn = ctk.CTkButton(self.clone_server_frame, text="Execute", command=self.execute_clone_server, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.clone_server_btn.pack(side="right")
        self.clone_source_guild_entry = ctk.CTkEntry(self.nuking_right, width=150, placeholder_text="Source Guild ID", border_color="#D3D3D3")
        self.clone_source_guild_entry.pack(anchor="w", padx=20, pady=2)

        # Raiding Section (two columns)
        self.raiding_left = ctk.CTkFrame(self.raiding_frame, fg_color="#FFFFFF")
        self.raiding_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.raiding_right = ctk.CTkFrame(self.raiding_frame, fg_color="#FFFFFF")
        self.raiding_right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Raiding Left
        self.raiding_label = ctk.CTkLabel(self.raiding_left, text="Raiding", font=("Helvetica", 14, "bold"), text_color="#000000")
        self.raiding_label.pack(anchor="w", padx=10, pady=5)

        self.raiding_guild_id_label = ctk.CTkLabel(self.raiding_left, text="Guild ID:", font=("Helvetica", 12), text_color="#000000")
        self.raiding_guild_id_label.pack(anchor="w", padx=10, pady=5)

        self.raiding_guild_id_entry = ctk.CTkEntry(self.raiding_left, width=200, placeholder_text="Enter Guild ID", border_color="#D3D3D3")
        self.raiding_guild_id_entry.pack(anchor="w", padx=10, pady=5)

        self.raid_check = ctk.CTkCheckBox(self.raiding_left, text="Enable Raid", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.raid_check.pack(anchor="w", padx=10, pady=5)

        self.spam_message_entry = ctk.CTkEntry(self.raiding_left, width=150, placeholder_text="Spam Message", border_color="#D3D3D3")
        self.spam_message_entry.pack(anchor="w", padx=20, pady=2)

        self.spam_count_entry = ctk.CTkEntry(self.raiding_left, width=100, placeholder_text="Spam Count", border_color="#D3D3D3")
        self.spam_count_entry.pack(anchor="w", padx=20, pady=2)

        self.spam_delay_entry = ctk.CTkEntry(self.raiding_left, width=100, placeholder_text="Spam Delay (s)", border_color="#D3D3D3")
        self.spam_delay_entry.pack(anchor="w", padx=20, pady=2)

        self.role_spam_frame = ctk.CTkFrame(self.raiding_left, fg_color="#FFFFFF")
        self.role_spam_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.role_spam_check = ctk.CTkCheckBox(self.role_spam_frame, text="Role Spam Ping", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.role_spam_check.pack(side="left")
        self.role_spam_btn = ctk.CTkButton(self.role_spam_frame, text="Execute", command=self.execute_role_spam, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.role_spam_btn.pack(side="right")

        self.mass_dm_frame = ctk.CTkFrame(self.raiding_left, fg_color="#FFFFFF")
        self.mass_dm_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.mass_dm_check = ctk.CTkCheckBox(self.mass_dm_frame, text="Mass DM Members", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.mass_dm_check.pack(side="left")
        self.mass_dm_btn = ctk.CTkButton(self.mass_dm_frame, text="Execute", command=self.execute_mass_dm, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.mass_dm_btn.pack(side="right")
        self.dm_message_entry = ctk.CTkEntry(self.raiding_left, width=150, placeholder_text="DM Message", border_color="#D3D3D3")
        self.dm_message_entry.pack(anchor="w", padx=20, pady=2)

        # Raiding Right
        self.multi_spam_frame = ctk.CTkFrame(self.raiding_right, fg_color="#FFFFFF")
        self.multi_spam_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.multi_spam_check = ctk.CTkCheckBox(self.multi_spam_frame, text="Multi-Channel Spam", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.multi_spam_check.pack(side="left")
        self.multi_spam_btn = ctk.CTkButton(self.multi_spam_frame, text="Execute", command=self.execute_multi_spam, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.multi_spam_btn.pack(side="right")

        self.webhook_spam_frame = ctk.CTkFrame(self.raiding_right, fg_color="#FFFFFF")
        self.webhook_spam_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.webhook_spam_check = ctk.CTkCheckBox(self.webhook_spam_frame, text="Webhook Spam", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.webhook_spam_check.pack(side="left")
        self.webhook_spam_btn = ctk.CTkButton(self.webhook_spam_frame, text="Execute", command=self.execute_webhook_spam, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.webhook_spam_btn.pack(side="right")

        self.invite_spam_frame = ctk.CTkFrame(self.raiding_right, fg_color="#FFFFFF")
        self.invite_spam_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.invite_spam_check = ctk.CTkCheckBox(self.invite_spam_frame, text="Invite Spam", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.invite_spam_check.pack(side="left")
        self.invite_spam_btn = ctk.CTkButton(self.invite_spam_frame, text="Execute", command=self.execute_invite_spam, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.invite_spam_btn.pack(side="right")

        # Spamming Section (two columns)
        self.spamming_left = ctk.CTkFrame(self.spamming_frame, fg_color="#FFFFFF")
        self.spamming_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.spamming_right = ctk.CTkFrame(self.spamming_frame, fg_color="#FFFFFF")
        self.spamming_right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Spamming Left
        self.spamming_label = ctk.CTkLabel(self.spamming_left, text="Spamming", font=("Helvetica", 14, "bold"), text_color="#000000")
        self.spamming_label.pack(anchor="w", padx=10, pady=5)

        self.spamming_guild_id_label = ctk.CTkLabel(self.spamming_left, text="Guild ID:", font=("Helvetica", 12), text_color="#000000")
        self.spamming_guild_id_label.pack(anchor="w", padx=10, pady=5)

        self.spamming_guild_id_entry = ctk.CTkEntry(self.spamming_left, width=200, placeholder_text="Enter Guild ID", border_color="#D3D3D3")
        self.spamming_guild_id_entry.pack(anchor="w", padx=10, pady=5)

        self.spam_check = ctk.CTkCheckBox(self.spamming_left, text="Enable Spam", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.spam_check.pack(anchor="w", padx=10, pady=5)

        self.spam_message_entry_spam = ctk.CTkEntry(self.spamming_left, width=150, placeholder_text="Spam Message", border_color="#D3D3D3")
        self.spam_message_entry_spam.pack(anchor="w", padx=20, pady=2)

        self.spam_count_entry_spam = ctk.CTkEntry(self.spamming_left, width=100, placeholder_text="Spam Count", border_color="#D3D3D3")
        self.spam_count_entry_spam.pack(anchor="w", padx=20, pady=2)

        self.spam_delay_entry_spam = ctk.CTkEntry(self.spamming_left, width=100, placeholder_text="Spam Delay (s)", border_color="#D3D3D3")
        self.spam_delay_entry_spam.pack(anchor="w", padx=20, pady=2)

        self.multi_spam_frame_spam = ctk.CTkFrame(self.spamming_left, fg_color="#FFFFFF")
        self.multi_spam_frame_spam.pack(anchor="w", padx=10, pady=2, fill="x")
        self.multi_spam_check_spam = ctk.CTkCheckBox(self.multi_spam_frame_spam, text="Multi-Channel Spam", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.multi_spam_check_spam.pack(side="left")
        self.multi_spam_btn_spam = ctk.CTkButton(self.multi_spam_frame_spam, text="Execute", command=self.execute_multi_spam_spam, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.multi_spam_btn_spam.pack(side="right")

        # Spamming Right
        self.webhook_spam_frame_spam = ctk.CTkFrame(self.spamming_right, fg_color="#FFFFFF")
        self.webhook_spam_frame_spam.pack(anchor="w", padx=10, pady=2, fill="x")
        self.webhook_spam_check_spam = ctk.CTkCheckBox(self.webhook_spam_frame_spam, text="Webhook Spam", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.webhook_spam_check_spam.pack(side="left")
        self.webhook_spam_btn_spam = ctk.CTkButton(self.webhook_spam_frame_spam, text="Execute", command=self.execute_webhook_spam_spam, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.webhook_spam_btn_spam.pack(side="right")

        self.invite_spam_frame_spam = ctk.CTkFrame(self.spamming_right, fg_color="#FFFFFF")
        self.invite_spam_frame_spam.pack(anchor="w", padx=10, pady=2, fill="x")
        self.invite_spam_check_spam = ctk.CTkCheckBox(self.invite_spam_frame_spam, text="Invite Spam", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.invite_spam_check_spam.pack(side="left")
        self.invite_spam_btn_spam = ctk.CTkButton(self.invite_spam_frame_spam, text="Execute", command=self.execute_invite_spam_spam, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.invite_spam_btn_spam.pack(side="right")

        # Premium Section (two columns)
        self.premium_left = ctk.CTkFrame(self.premium_frame, fg_color="#FFFFFF")
        self.premium_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.premium_right = ctk.CTkFrame(self.premium_frame, fg_color="#FFFFFF")
        self.premium_right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Premium Left
        self.premium_label = ctk.CTkLabel(self.premium_left, text="Premium Features", font=("Helvetica", 14, "bold"), text_color="#000000")
        self.premium_label.pack(anchor="w", padx=10, pady=5)

        self.premium_guild_id_label = ctk.CTkLabel(self.premium_left, text="Guild ID:", font=("Helvetica", 12), text_color="#000000")
        self.premium_guild_id_label.pack(anchor="w", padx=10, pady=5)

        self.premium_guild_id_entry = ctk.CTkEntry(self.premium_left, width=200, placeholder_text="Enter Guild ID", border_color="#D3D3D3")
        self.premium_guild_id_entry.pack(anchor="w", padx=10, pady=5)

        self.premium_nuke_check = ctk.CTkCheckBox(self.premium_left, text="Enable Premium Nuke (10x)", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.premium_nuke_check.pack(anchor="w", padx=10, pady=5)

        self.kick_all_frame = ctk.CTkFrame(self.premium_left, fg_color="#FFFFFF")
        self.kick_all_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.kick_all_check = ctk.CTkCheckBox(self.kick_all_frame, text="Kick All Members", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.kick_all_check.pack(side="left")
        self.kick_all_btn = ctk.CTkButton(self.kick_all_frame, text="Execute", command=self.execute_kick_all, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.kick_all_btn.pack(side="right")

        self.delete_emojis_frame = ctk.CTkFrame(self.premium_left, fg_color="#FFFFFF")
        self.delete_emojis_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.delete_emojis_check = ctk.CTkCheckBox(self.delete_emojis_frame, text="Delete Emojis", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.delete_emojis_check.pack(side="left")
        self.delete_emojis_btn = ctk.CTkButton(self.delete_emojis_frame, text="Execute", command=self.execute_delete_emojis, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.delete_emojis_btn.pack(side="right")

        self.change_guild_name_frame = ctk.CTkFrame(self.premium_left, fg_color="#FFFFFF")
        self.change_guild_name_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.change_guild_name_check = ctk.CTkCheckBox(self.change_guild_name_frame, text="Change Guild Name", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.change_guild_name_check.pack(side="left")
        self.change_guild_name_btn = ctk.CTkButton(self.change_guild_name_frame, text="Execute", command=self.execute_change_guild_name, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.change_guild_name_btn.pack(side="right")
        self.guild_name_entry = ctk.CTkEntry(self.premium_left, width=150, placeholder_text="New Guild Name", border_color="#D3D3D3")
        self.guild_name_entry.pack(anchor="w", padx=20, pady=2)

        self.mass_nick_frame = ctk.CTkFrame(self.premium_left, fg_color="#FFFFFF")
        self.mass_nick_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.mass_nick_check = ctk.CTkCheckBox(self.mass_nick_frame, text="Mass Nickname Change", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.mass_nick_check.pack(side="left")
        self.mass_nick_btn = ctk.CTkButton(self.mass_nick_frame, text="Execute", command=self.execute_mass_nick, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.mass_nick_btn.pack(side="right")
        self.nick_name_entry = ctk.CTkEntry(self.premium_left, width=150, placeholder_text="New Nickname", border_color="#D3D3D3")
        self.nick_name_entry.pack(anchor="w", padx=20, pady=2)

        # Premium Right
        self.premium_raid_check = ctk.CTkCheckBox(self.premium_right, text="Enable Premium Raid (10x)", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.premium_raid_check.pack(anchor="w", padx=10, pady=5)

        self.voice_chaos_frame = ctk.CTkFrame(self.premium_right, fg_color="#FFFFFF")
        self.voice_chaos_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.voice_chaos_check = ctk.CTkCheckBox(self.voice_chaos_frame, text="Voice Channel Chaos", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.voice_chaos_check.pack(side="left")
        self.voice_chaos_btn = ctk.CTkButton(self.voice_chaos_frame, text="Execute", command=self.execute_voice_chaos, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.voice_chaos_btn.pack(side="right")

        self.bypass_security_frame = ctk.CTkFrame(self.premium_right, fg_color="#FFFFFF")
        self.bypass_security_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.bypass_security_check = ctk.CTkCheckBox(self.bypass_security_frame, text="Bypass Bot Security", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.bypass_security_check.pack(side="left")
        self.bypass_security_btn = ctk.CTkButton(self.bypass_security_frame, text="Execute", command=self.execute_bypass_security, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.bypass_security_btn.pack(side="right")

        self.premium_clone_server_frame = ctk.CTkFrame(self.premium_right, fg_color="#FFFFFF")
        self.premium_clone_server_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.premium_clone_server_check = ctk.CTkCheckBox(self.premium_clone_server_frame, text="Clone Server (10x)", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.premium_clone_server_check.pack(side="left")
        self.premium_clone_server_btn = ctk.CTkButton(self.premium_clone_server_frame, text="Execute", command=self.execute_premium_clone_server, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.premium_clone_server_btn.pack(side="right")
        self.premium_clone_source_guild_entry = ctk.CTkEntry(self.premium_right, width=150, placeholder_text="Source Guild ID", border_color="#D3D3D3")
        self.premium_clone_source_guild_entry.pack(anchor="w", padx=20, pady=2)

        # Utility Section (two columns)
        self.utility_left = ctk.CTkFrame(self.utility_frame, fg_color="#FFFFFF")
        self.utility_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.utility_right = ctk.CTkFrame(self.utility_frame, fg_color="#FFFFFF")
        self.utility_right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Utility Left
        self.utility_label = ctk.CTkLabel(self.utility_left, text="Utility Features", font=("Helvetica", 14, "bold"), text_color="#000000")
        self.utility_label.pack(anchor="w", padx=10, pady=5)

        self.utility_guild_id_label = ctk.CTkLabel(self.utility_left, text="Guild ID:", font=("Helvetica", 12), text_color="#000000")
        self.utility_guild_id_label.pack(anchor="w", padx=10, pady=5)

        self.utility_guild_id_entry = ctk.CTkEntry(self.utility_left, width=200, placeholder_text="Enter Guild ID", border_color="#D3D3D3")
        self.utility_guild_id_entry.pack(anchor="w", padx=10, pady=5)

        self.utility_channel_id_label = ctk.CTkLabel(self.utility_left, text="Channel ID (Optional):", font=("Helvetica", 12), text_color="#000000")
        self.utility_channel_id_label.pack(anchor="w", padx=10, pady=5)

        self.utility_channel_id_entry = ctk.CTkEntry(self.utility_left, width=200, placeholder_text="Enter Channel ID", border_color="#D3D3D3")
        self.utility_channel_id_entry.pack(anchor="w", padx=10, pady=5)

        self.utility_user_id_label = ctk.CTkLabel(self.utility_left, text="User ID (Optional):", font=("Helvetica", 12), text_color="#000000")
        self.utility_user_id_label.pack(anchor="w", padx=10, pady=5)

        self.utility_user_id_entry = ctk.CTkEntry(self.utility_left, width=200, placeholder_text="Enter User ID", border_color="#D3D3D3")
        self.utility_user_id_entry.pack(anchor="w", padx=10, pady=5)

        self.mass_delete_frame = ctk.CTkFrame(self.utility_left, fg_color="#FFFFFF")
        self.mass_delete_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.mass_delete_check = ctk.CTkCheckBox(self.mass_delete_frame, text="Mass Delete Messages", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.mass_delete_check.pack(side="left")
        self.mass_delete_btn = ctk.CTkButton(self.mass_delete_frame, text="Execute", command=self.execute_mass_delete, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.mass_delete_btn.pack(side="right")
        self.mass_delete_count_entry = ctk.CTkEntry(self.utility_left, width=100, placeholder_text="Message Count", border_color="#D3D3D3")
        self.mass_delete_count_entry.pack(anchor="w", padx=20, pady=2)

        self.server_info_frame = ctk.CTkFrame(self.utility_left, fg_color="#FFFFFF")
        self.server_info_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.server_info_check = ctk.CTkCheckBox(self.server_info_frame, text="Get Server Info", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.server_info_check.pack(side="left")
        self.server_info_btn = ctk.CTkButton(self.server_info_frame, text="Execute", command=self.execute_server_info, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.server_info_btn.pack(side="right")

        # Utility Right
        self.user_info_frame = ctk.CTkFrame(self.utility_right, fg_color="#FFFFFF")
        self.user_info_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.user_info_check = ctk.CTkCheckBox(self.user_info_frame, text="Get User Info", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.user_info_check.pack(side="left")
        self.user_info_btn = ctk.CTkButton(self.user_info_frame, text="Execute", command=self.execute_user_info, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.user_info_btn.pack(side="right")

        self.assign_role_frame = ctk.CTkFrame(self.utility_right, fg_color="#FFFFFF")
        self.assign_role_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.assign_role_check = ctk.CTkCheckBox(self.assign_role_frame, text="Assign Role to User", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.assign_role_check.pack(side="left")
        self.assign_role_btn = ctk.CTkButton(self.assign_role_frame, text="Execute", command=self.execute_assign_role, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.assign_role_btn.pack(side="right")
        self.assign_role_id_entry = ctk.CTkEntry(self.utility_right, width=150, placeholder_text="Role ID", border_color="#D3D3D3")
        self.assign_role_id_entry.pack(anchor="w", padx=20, pady=2)

        self.channel_perms_frame = ctk.CTkFrame(self.utility_right, fg_color="#FFFFFF")
        self.channel_perms_frame.pack(anchor="w", padx=10, pady=2, fill="x")
        self.channel_perms_check = ctk.CTkCheckBox(self.channel_perms_frame, text="Lock/Unlock Channel", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.channel_perms_check.pack(side="left")
        self.channel_perms_btn = ctk.CTkButton(self.channel_perms_frame, text="Execute", command=self.execute_channel_perms, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3", width=80)
        self.channel_perms_btn.pack(side="right")
        self.channel_perms_option = ctk.CTkOptionMenu(self.utility_right, values=["Lock", "Unlock"], fg_color="#FFFFFF", button_color="#D3D3D3", button_hover_color="#E0E0E0", text_color="#000000", width=100)
        self.channel_perms_option.pack(anchor="w", padx=20, pady=2)

        # Settings Section (two columns for settings and log)
        self.settings_left = ctk.CTkFrame(self.settings_frame, fg_color="#FFFFFF")
        self.settings_left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.settings_right = ctk.CTkFrame(self.settings_frame, fg_color="#FFFFFF")
        self.settings_right.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Settings Left
        self.settings_label = ctk.CTkLabel(self.settings_left, text="Settings", font=("Helvetica", 14, "bold"), text_color="#000000")
        self.settings_label.pack(anchor="w", padx=10, pady=5)

        self.token_label = ctk.CTkLabel(self.settings_left, text="Manual Token:", font=("Helvetica", 12), text_color="#000000")
        self.token_label.pack(anchor="w", padx=10, pady=5)

        self.token_entry = ctk.CTkEntry(self.settings_left, width=300, placeholder_text="Your Discord Token", border_color="#D3D3D3")
        self.token_entry.pack(anchor="w", padx=10, pady=5)

        self.set_token_btn = ctk.CTkButton(self.settings_left, text="Set Token", command=self.set_token, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.set_token_btn.pack(anchor="w", padx=10, pady=5)

        self.test_token_btn = ctk.CTkButton(self.settings_left, text="Test Token", command=self.test_token, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.test_token_btn.pack(anchor="w", padx=10, pady=5)

        self.start_bot_btn = ctk.CTkButton(self.settings_left, text="Start Bot", command=self.start_bot, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.start_bot_btn.pack(anchor="w", padx=10, pady=5)

        self.stop_bot_btn = ctk.CTkButton(self.settings_left, text="Stop Bot", command=self.stop_bot, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.stop_bot_btn.pack(anchor="w", padx=10, pady=5)

        self.premium_key_label = ctk.CTkLabel(self.settings_left, text="Premium Key:", font=("Helvetica", 12), text_color="#000000")
        self.premium_key_label.pack(anchor="w", padx=10, pady=5)

        self.premium_key_entry = ctk.CTkEntry(self.settings_left, width=300, placeholder_text="Enter Premium Key", border_color="#D3D3D3")
        self.premium_key_entry.pack(anchor="w", padx=10, pady=5)

        self.login_premium_btn = ctk.CTkButton(self.settings_left, text="Login Premium", command=self.login_premium, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.login_premium_btn.pack(anchor="w", padx=10, pady=5)

        self.prefix_label = ctk.CTkLabel(self.settings_left, text="Command Prefix:", font=("Helvetica", 12), text_color="#000000")
        self.prefix_label.pack(anchor="w", padx=10, pady=5)

        self.prefix_entry = ctk.CTkEntry(self.settings_left, width=100, placeholder_text="!", border_color="#D3D3D3")
        self.prefix_entry.pack(anchor="w", padx=10, pady=5)

        self.set_prefix_btn = ctk.CTkButton(self.settings_left, text="Set Prefix", command=self.set_prefix, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.set_prefix_btn.pack(anchor="w", padx=10, pady=5)

        self.vpn_check = ctk.CTkCheckBox(self.settings_left, text="Use VPN (IP Ban Bypass)", border_width=2, corner_radius=0, fg_color="#000000", text_color="#000000")
        self.vpn_check.pack(anchor="w", padx=10, pady=5)

        self.switch_account_btn = ctk.CTkButton(self.settings_left, text="Switch Account", command=self.switch_account, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.switch_account_btn.pack(anchor="w", padx=10, pady=5)

        self.global_guild_id_label = ctk.CTkLabel(self.settings_left, text="Global Guild ID:", font=("Helvetica", 12), text_color="#000000")
        self.global_guild_id_label.pack(anchor="w", padx=10, pady=5)

        self.global_guild_id_entry = ctk.CTkEntry(self.settings_left, width=200, placeholder_text="Enter Global Guild ID", border_color="#D3D3D3")
        self.global_guild_id_entry.pack(anchor="w", padx=10, pady=5)

        self.save_global_guild_id_btn = ctk.CTkButton(self.settings_left, text="Save Global Guild ID", command=self.save_global_guild_id, corner_radius=0, fg_color="#FFFFFF", hover_color="#E0E0E0", text_color="#000000", border_width=1, border_color="#D3D3D3")
        self.save_global_guild_id_btn.pack(anchor="w", padx=10, pady=5)

        # Settings Right (Log)
        self.log_label = ctk.CTkLabel(self.settings_right, text="Log", font=("Helvetica", 14, "bold"), text_color="#000000")
        self.log_label.pack(anchor="w", padx=10, pady=5)

        self.log_text = ctk.CTkTextbox(self.settings_right, width=400, height=400, border_color="#D3D3D3")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_text.insert("end", "Log initialized.\n")
        self.log_text.configure(state="disabled")

        # Show Settings section by default
        self.show_settings()

    def log_message(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

    def enable_menu_buttons(self):
        if self.is_premium:
            self.raid_btn.configure(state="normal", hover=True)
            self.nuke_btn.configure(state="normal", hover=True)
            self.spam_btn.configure(state="normal", hover=True)
            self.premium_btn.configure(state="normal", hover=True)
            self.utility_btn.configure(state="normal", hover=True)
            self.settings_btn.configure(state="normal", hover=True)
            self.status_label.configure(text="Bot Online - All Features Unlocked", text_color="green")
            self.log_message("Menu buttons enabled.")

    def set_token(self):
        try:
            token = self.token_entry.get()
            if token:
                self.bot = DiscordSelfBot(token)
                self.actions = BotActions(self.bot)
                self.premium_actions = PremiumActions(self.bot)
                self.utility_actions = UtilityActions(self.bot)
                self.log_message("Token set successfully.")
                self.status_label.configure(text="Bot Online - Enter Premium Key", text_color="yellow")
            else:
                self.log_message("Error: No token entered. Enter a token!")
        except Exception as e:
            self.log_message(f"Error setting token: {str(e)}")

    def login_premium(self):
        try:
            key = self.premium_key_entry.get()
            if not key:
                self.log_message("Error: No premium key entered. Enter a key!")
                return

            if key == "devhacks":
                self.is_premium = True
                self.log_message("Premium login successful.")
                self.status_label.configure(text="Bot Online - Premium Unlocked", text_color="green")
                self.enable_menu_buttons()
            else:
                self.log_message("Error: Invalid premium key. Try again!")
                self.status_label.configure(text="Bot Online - Invalid Premium Key", text_color="red")
        except Exception as e:
            self.log_message(f"Error during premium login: {str(e)}")

    def test_token(self):
        try:
            if self.bot:
                if self.bot.is_connected():
                    self.log_message("Token is valid.")
                    self.status_label.configure(text="Bot Online", text_color="green")
                else:
                    self.log_message("Error: Token is invalid.")
                    self.status_label.configure(text="Bot Offline - Invalid Token", text_color="red")
            else:
                self.log_message("Error: Set a token first.")
        except Exception as e:
            self.log_message(f"Error testing token: {str(e)}")

    def start_bot(self):
        try:
            if self.bot and not self.bot_running:
                self.bot_thread = threading.Thread(target=self.bot.run)
                self.bot_thread.start()
                self.bot_running = True
                self.status_label.configure(text="Bot Online", text_color="green")
                self.log_message("Bot started successfully.")
            else:
                self.log_message("Error: Bot already running or no token set.")
        except Exception as e:
            self.log_message(f"Error starting bot: {str(e)}")

    def stop_bot(self):
        try:
            if self.bot and self.bot_running:
                self.bot.close()
                self.bot_thread.join()
                self.bot_running = False
                self.status_label.configure(text="Bot Offline - Waiting to Start", text_color="red")
                self.log_message("Bot stopped successfully.")
            else:
                self.log_message("Error: Bot not running.")
        except Exception as e:
            self.log_message(f"Error stopping bot: {str(e)}")

    def set_prefix(self):
        try:
            prefix = self.prefix_entry.get()
            if prefix:
                if self.bot:
                    self.bot.set_prefix(prefix)
                    self.log_message(f"Prefix set to {prefix}.")
                else:
                    self.log_message("Error: Set a token and start the bot first.")
            else:
                self.log_message("Error: No prefix entered.")
        except Exception as e:
            self.log_message(f"Error setting prefix: {str(e)}")

    def switch_account(self):
        self.log_message("Switching account... (Placeholder)")

    def save_global_guild_id(self):
        try:
            guild_id = self.global_guild_id_entry.get()
            if guild_id and guild_id.isdigit():
                self.global_guild_id = int(guild_id)
                self.log_message(f"Global Guild ID saved: {self.global_guild_id}.")
            else:
                self.global_guild_id = None
                self.log_message("Error: Invalid Global Guild ID. Enter a number!")
        except Exception as e:
            self.log_message(f"Error saving global guild ID: {str(e)}")

    def get_guild_id(self, entry_field):
        guild_id = entry_field.get()
        if guild_id and guild_id.isdigit():
            return int(guild_id)
        return self.global_guild_id

    def show_nuking(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        self.raiding_frame.pack_forget()
        self.spamming_frame.pack_forget()
        self.premium_frame.pack_forget()
        self.utility_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.nuking_frame.pack(fill="both", expand=True)

    def show_raiding(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        self.nuking_frame.pack_forget()
        self.spamming_frame.pack_forget()
        self.premium_frame.pack_forget()
        self.utility_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.raiding_frame.pack(fill="both", expand=True)

    def show_spamming(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        self.nuking_frame.pack_forget()
        self.raiding_frame.pack_forget()
        self.premium_frame.pack_forget()
        self.utility_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.spamming_frame.pack(fill="both", expand=True)

    def show_premium(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        self.nuking_frame.pack_forget()
        self.raiding_frame.pack_forget()
        self.spamming_frame.pack_forget()
        self.utility_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.premium_frame.pack(fill="both", expand=True)

    def show_utility(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        self.nuking_frame.pack_forget()
        self.raiding_frame.pack_forget()
        self.spamming_frame.pack_forget()
        self.premium_frame.pack_forget()
        self.settings_frame.pack_forget()
        self.utility_frame.pack(fill="both", expand=True)

    def show_settings(self):
        self.nuking_frame.pack_forget()
        self.raiding_frame.pack_forget()
        self.spamming_frame.pack_forget()
        self.premium_frame.pack_forget()
        self.utility_frame.pack_forget()
        self.settings_frame.pack(fill="both", expand=True)

    def stop_action(self):
        self.log_message("Stopping action... (Placeholder)")

    def run_coroutine(self, coro):
        if self.bot:
            loop = self.bot.bot.loop
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
        else:
            self.log_message("Error: Bot not started.")
            return None

    def run_action_in_thread(self, action_func, *args, **kwargs):
        def wrapper():
            try:
                self.run_coroutine(action_func(*args, **kwargs))
                self.log_message(f"Action {action_func.__name__} completed successfully.")
            except Exception as e:
                self.log_message(f"Error in action {action_func.__name__}: {str(e)}")
        thread = threading.Thread(target=wrapper)
        thread.start()

    def get_custom_settings(self):
        try:
            role_count = self.role_count_entry.get()
            role_count = int(role_count) if role_count and role_count.isdigit() else 10

            channel_count = self.channel_count_entry.get()
            channel_count = int(channel_count) if channel_count and channel_count.isdigit() else 10

            category_count = self.category_count_entry.get()
            category_count = int(category_count) if category_count and category_count.isdigit() else 5

            guild_name = self.guild_name_entry.get() or "NUKED-BY-SELF-BOT"

            nick_name = self.nick_name_entry.get() or "NukedUser"

            spam_message = self.spam_message_entry.get() or self.spam_message_entry_spam.get() or "@everyone Get fucked, losers!"

            spam_count = self.spam_count_entry.get() or self.spam_count_entry_spam.get()
            spam_count = int(spam_count) if spam_count and spam_count.isdigit() else 10

            spam_delay = self.spam_delay_entry.get() or self.spam_delay_entry_spam.get()
            spam_delay = float(spam_delay) if spam_delay and spam_delay.replace('.', '', 1).isdigit() else 0.5

            dm_message = self.dm_message_entry.get() or "You’ve been raided, bitch!"

            mass_delete_count = self.mass_delete_count_entry.get()
            mass_delete_count = int(mass_delete_count) if mass_delete_count and mass_delete_count.isdigit() else 50

            return {
                "role_count": role_count,
                "channel_count": channel_count,
                "category_count": category_count,
                "guild_name": guild_name,
                "nick_name": nick_name,
                "spam_message": spam_message,
                "spam_count": spam_count,
                "spam_delay": spam_delay,
                "dm_message": dm_message,
                "mass_delete_count": mass_delete_count
            }
        except Exception as e:
            self.log_message(f"Error getting custom settings: {str(e)}")
            return {
                "role_count": 10,
                "channel_count": 10,
                "category_count": 5,
                "guild_name": "NUKED-BY-SELF-BOT",
                "nick_name": "NukedUser",
                "spam_message": "@everyone Get fucked, losers!",
                "spam_count": 10,
                "spam_delay": 0.5,
                "dm_message": "You’ve been raided, bitch!",
                "mass_delete_count": 50
            }

    # Nuking Actions
    def execute_create_roles(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Nuking section or Settings. Enter one!")
            return

        if not self.nuke_check.get() or not self.role_create_check.get():
            self.log_message("Error: Nuke or Create Roles not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Create Roles on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.nuke_server, guild_id=guild_id, create_roles=True, create_channels=False, create_categories=False, ban_all=False, delete_channels=False, delete_roles=False, clone_server=False, role_count=settings["role_count"], channel_count=settings["channel_count"], category_count=settings["category_count"])

    def execute_create_channels(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Nuking section or Settings. Enter one!")
            return

        if not self.nuke_check.get() or not self.channel_create_check.get():
            self.log_message("Error: Nuke or Create Channels not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Create Channels on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.nuke_server, guild_id=guild_id, create_roles=False, create_channels=True, create_categories=False, ban_all=False, delete_channels=False, delete_roles=False, clone_server=False, role_count=settings["role_count"], channel_count=settings["channel_count"], category_count=settings["category_count"])

    def execute_create_categories(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Nuking section or Settings. Enter one!")
            return

        if not self.nuke_check.get() or not self.category_create_check.get():
            self.log_message("Error: Nuke or Create Categories not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Create Categories on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.nuke_server, guild_id=guild_id, create_roles=False, create_channels=False, create_categories=True, ban_all=False, delete_channels=False, delete_roles=False, clone_server=False, role_count=settings["role_count"], channel_count=settings["channel_count"], category_count=settings["category_count"])

    def execute_ban_all(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Nuking section or Settings. Enter one!")
            return

        if not self.nuke_check.get() or not self.ban_all_check.get():
            self.log_message("Error: Nuke or Ban All Members not enabled. Enable them!")
            return

        self.log_message(f"Starting Ban All Members on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.nuke_server, guild_id=guild_id, create_roles=False, create_channels=False, create_categories=False, ban_all=True, delete_channels=False, delete_roles=False, clone_server=False)

    def execute_delete_channels(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Nuking section or Settings. Enter one!")
            return

        if not self.nuke_check.get() or not self.delete_channels_check.get():
            self.log_message("Error: Nuke or Delete All Channels not enabled. Enable them!")
            return

        self.log_message(f"Starting Delete All Channels on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.nuke_server, guild_id=guild_id, create_roles=False, create_channels=False, create_categories=False, ban_all=False, delete_channels=True, delete_roles=False, clone_server=False)

    def execute_delete_roles(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Nuking section or Settings. Enter one!")
            return

        if not self.nuke_check.get() or not self.delete_roles_check.get():
            self.log_message("Error: Nuke or Delete All Roles not enabled. Enable them!")
            return

        self.log_message(f"Starting Delete All Roles on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.nuke_server, guild_id=guild_id, create_roles=False, create_channels=False, create_categories=False, ban_all=False, delete_channels=False, delete_roles=True, clone_server=False)

    def execute_clone_server(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        source_guild_id = self.clone_source_guild_entry.get()
        if not guild_id:
            self.log_message("Error: No Target Guild ID set in Nuking section or Settings. Enter one!")
            return
        if not source_guild_id or not source_guild_id.isdigit():
            self.log_message("Error: No Source Guild ID set in Nuking section. Enter a valid ID!")
            return

        if not self.nuke_check.get() or not self.clone_server_check.get():
            self.log_message("Error: Nuke or Clone Server not enabled. Enable them!")
            return

        self.log_message(f"Starting Clone Server from Source Guild ID: {source_guild_id} to Target Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.nuke_server, guild_id=guild_id, create_roles=False, create_channels=False, create_categories=False, ban_all=False, delete_channels=False, delete_roles=False, clone_server=True, source_guild_id=int(source_guild_id))

    def execute_all_nuke_actions(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.nuking_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Nuking section or Settings. Enter one!")
            return

        if not self.nuke_check.get():
            self.log_message("Error: Nuke not enabled. Enable it!")
            return

        settings = self.get_custom_settings()
        source_guild_id = self.clone_source_guild_entry.get()
        if self.clone_server_check.get() and (not source_guild_id or not source_guild_id.isdigit()):
            self.log_message("Error: No Source Guild ID set for Clone Server. Enter a valid ID!")
            return

        self.log_message(f"Starting All Nuke Actions on Guild ID: {guild_id}...")
        self.run_action_in_thread(
            self.actions.nuke_server,
            guild_id=guild_id,
            create_roles=self.role_create_check.get(),
            create_channels=self.channel_create_check.get(),
            create_categories=self.category_create_check.get(),
            ban_all=self.ban_all_check.get(),
            delete_channels=self.delete_channels_check.get(),
            delete_roles=self.delete_roles_check.get(),
            clone_server=self.clone_server_check.get(),
            source_guild_id=int(source_guild_id) if source_guild_id and source_guild_id.isdigit() else None,
            role_count=settings["role_count"],
            channel_count=settings["channel_count"],
            category_count=settings["category_count"]
        )

    # Raiding Actions
    def execute_role_spam(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.raiding_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Raiding section or Settings. Enter one!")
            return

        if not self.raid_check.get() or not self.role_spam_check.get():
            self.log_message("Error: Raid or Role Spam not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Role Spam on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.raid_server, guild_id=guild_id, role_spam=True, multi_spam=False, mass_dm=False, webhook_spam=False, invite_spam=False, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"], dm_message=settings["dm_message"])

    def execute_mass_dm(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.raiding_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Raiding section or Settings. Enter one!")
            return

        if not self.raid_check.get() or not self.mass_dm_check.get():
            self.log_message("Error: Raid or Mass DM not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Mass DM on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.raid_server, guild_id=guild_id, role_spam=False, multi_spam=False, mass_dm=True, webhook_spam=False, invite_spam=False, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"], dm_message=settings["dm_message"])

    def execute_multi_spam(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.raiding_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Raiding section or Settings. Enter one!")
            return

        if not self.raid_check.get() or not self.multi_spam_check.get():
            self.log_message("Error: Raid or Multi-Channel Spam not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Multi-Channel Spam on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.raid_server, guild_id=guild_id, role_spam=False, multi_spam=True, mass_dm=False, webhook_spam=False, invite_spam=False, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"], dm_message=settings["dm_message"])

    def execute_webhook_spam(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.raiding_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Raiding section or Settings. Enter one!")
            return

        if not self.raid_check.get() or not self.webhook_spam_check.get():
            self.log_message("Error: Raid or Webhook Spam not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Webhook Spam on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.raid_server, guild_id=guild_id, role_spam=False, multi_spam=False, mass_dm=False, webhook_spam=True, invite_spam=False, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"], dm_message=settings["dm_message"])

    def execute_invite_spam(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.raiding_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Raiding section or Settings. Enter one!")
            return

        if not self.raid_check.get() or not self.invite_spam_check.get():
            self.log_message("Error: Raid or Invite Spam not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Invite Spam on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.raid_server, guild_id=guild_id, role_spam=False, multi_spam=False, mass_dm=False, webhook_spam=False, invite_spam=True, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"], dm_message=settings["dm_message"])

    # Premium Nuking Actions
    def execute_kick_all(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.premium_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Premium section or Settings. Enter one!")
            return

        if not self.premium_nuke_check.get() or not self.kick_all_check.get():
            self.log_message("Error: Premium Nuke or Kick All Members not enabled. Enable them!")
            return

        self.log_message(f"Starting Kick All Members on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.nuke_server, guild_id=guild_id, create_roles=False, create_channels=False, create_categories= False)

                # Premium Nuking Actions (continued)
        self.log_message(f"Starting Kick All Members on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.premium_nuke, guild_id=guild_id, kick_all=True, delete_emojis=False, change_guild_name=False, mass_nick=False, voice_chaos=False, bypass_security=False, clone_server=False)

    def execute_delete_emojis(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.premium_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Premium section or Settings. Enter one!")
            return

        if not self.premium_nuke_check.get() or not self.delete_emojis_check.get():
            self.log_message("Error: Premium Nuke or Delete Emojis not enabled. Enable them!")
            return

        self.log_message(f"Starting Delete Emojis on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.premium_nuke, guild_id=guild_id, kick_all=False, delete_emojis=True, change_guild_name=False, mass_nick=False, voice_chaos=False, bypass_security=False, clone_server=False)

    def execute_change_guild_name(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.premium_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Premium section or Settings. Enter one!")
            return

        if not self.premium_nuke_check.get() or not self.change_guild_name_check.get():
            self.log_message("Error: Premium Nuke or Change Guild Name not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Change Guild Name on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.premium_nuke, guild_id=guild_id, kick_all=False, delete_emojis=False, change_guild_name=True, mass_nick=False, voice_chaos=False, bypass_security=False, clone_server=False, guild_name=settings["guild_name"])

    def execute_mass_nick(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.premium_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Premium section or Settings. Enter one!")
            return

        if not self.premium_nuke_check.get() or not self.mass_nick_check.get():
            self.log_message("Error: Premium Nuke or Mass Nickname Change not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Mass Nickname Change on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.premium_nuke, guild_id=guild_id, kick_all=False, delete_emojis=False, change_guild_name=False, mass_nick=True, voice_chaos=False, bypass_security=False, clone_server=False, nick_name=settings["nick_name"])

    def execute_voice_chaos(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.premium_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Premium section or Settings. Enter one!")
            return

        if not self.premium_raid_check.get() or not self.voice_chaos_check.get():
            self.log_message("Error: Premium Raid or Voice Channel Chaos not enabled. Enable them!")
            return

        self.log_message(f"Starting Voice Channel Chaos on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.premium_raid, guild_id=guild_id, voice_chaos=True, bypass_security=False, clone_server=False)

    def execute_bypass_security(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.premium_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Premium section or Settings. Enter one!")
            return

        if not self.premium_raid_check.get() or not self.bypass_security_check.get():
            self.log_message("Error: Premium Raid or Bypass Bot Security not enabled. Enable them!")
            return

        self.log_message(f"Starting Bypass Bot Security on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.premium_raid, guild_id=guild_id, voice_chaos=False, bypass_security=True, clone_server=False)

    def execute_premium_clone_server(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.premium_guild_id_entry)
        source_guild_id = self.premium_clone_source_guild_entry.get()
        if not guild_id:
            self.log_message("Error: No Target Guild ID set in Premium section or Settings. Enter one!")
            return
        if not source_guild_id or not source_guild_id.isdigit():
            self.log_message("Error: No Source Guild ID set in Premium section. Enter a valid ID!")
            return

        if not self.premium_raid_check.get() or not self.premium_clone_server_check.get():
            self.log_message("Error: Premium Raid or Clone Server (10x) not enabled. Enable them!")
            return

        self.log_message(f"Starting Premium Clone Server (10x) from Source Guild ID: {source_guild_id} to Target Guild ID: {guild_id}...")
        self.run_action_in_thread(self.premium_actions.premium_raid, guild_id=guild_id, voice_chaos=False, bypass_security=False, clone_server=True, source_guild_id=int(source_guild_id))

    # Spamming Actions
    def execute_multi_spam_spam(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.spamming_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Spamming section or Settings. Enter one!")
            return

        if not self.spam_check.get() or not self.multi_spam_check_spam.get():
            self.log_message("Error: Spam or Multi-Channel Spam not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Multi-Channel Spam on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.spam_server, guild_id=guild_id, multi_spam=True, webhook_spam=False, invite_spam=False, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"])

    def execute_webhook_spam_spam(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.spamming_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Spamming section or Settings. Enter one!")
            return

        if not self.spam_check.get() or not self.webhook_spam_check_spam.get():
            self.log_message("Error: Spam or Webhook Spam not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Webhook Spam on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.spam_server, guild_id=guild_id, multi_spam=False, webhook_spam=True, invite_spam=False, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"])

    def execute_invite_spam_spam(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.spamming_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Spamming section or Settings. Enter one!")
            return

        if not self.spam_check.get() or not self.invite_spam_check_spam.get():
            self.log_message("Error: Spam or Invite Spam not enabled. Enable them!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Invite Spam on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.actions.spam_server, guild_id=guild_id, multi_spam=False, webhook_spam=False, invite_spam=True, spam_message=settings["spam_message"], spam_count=settings["spam_count"], spam_delay=settings["spam_delay"])

    # Utility Actions
    def execute_mass_delete(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.utility_guild_id_entry)
        channel_id = self.utility_channel_id_entry.get()
        if not guild_id:
            self.log_message("Error: No Guild ID set in Utility section or Settings. Enter one!")
            return
        if not channel_id or not channel_id.isdigit():
            self.log_message("Error: No Channel ID set in Utility section. Enter a valid ID!")
            return

        if not self.mass_delete_check.get():
            self.log_message("Error: Mass Delete Messages not enabled. Enable it!")
            return

        settings = self.get_custom_settings()
        self.log_message(f"Starting Mass Delete Messages in Channel ID: {channel_id} on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.utility_actions.mass_delete_messages, guild_id=guild_id, channel_id=int(channel_id), count=settings["mass_delete_count"])

    def execute_server_info(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.utility_guild_id_entry)
        if not guild_id:
            self.log_message("Error: No Guild ID set in Utility section or Settings. Enter one!")
            return

        if not self.server_info_check.get():
            self.log_message("Error: Get Server Info not enabled. Enable it!")
            return

        self.log_message(f"Fetching Server Info for Guild ID: {guild_id}...")
        self.run_action_in_thread(self.utility_actions.get_server_info, guild_id=guild_id)

    def execute_user_info(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.utility_guild_id_entry)
        user_id = self.utility_user_id_entry.get()
        if not guild_id:
            self.log_message("Error: No Guild ID set in Utility section or Settings. Enter one!")
            return
        if not user_id or not user_id.isdigit():
            self.log_message("Error: No User ID set in Utility section. Enter a valid ID!")
            return

        if not self.user_info_check.get():
            self.log_message("Error: Get User Info not enabled. Enable it!")
            return

        self.log_message(f"Fetching User Info for User ID: {user_id} on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.utility_actions.get_user_info, guild_id=guild_id, user_id=int(user_id))

    def execute_assign_role(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.utility_guild_id_entry)
        user_id = self.utility_user_id_entry.get()
        role_id = self.assign_role_id_entry.get()
        if not guild_id:
            self.log_message("Error: No Guild ID set in Utility section or Settings. Enter one!")
            return
        if not user_id or not user_id.isdigit():
            self.log_message("Error: No User ID set in Utility section. Enter a valid ID!")
            return
        if not role_id or not role_id.isdigit():
            self.log_message("Error: No Role ID set in Utility section. Enter a valid ID!")
            return

        if not self.assign_role_check.get():
            self.log_message("Error: Assign Role to User not enabled. Enable it!")
            return

        self.log_message(f"Assigning Role ID: {role_id} to User ID: {user_id} on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.utility_actions.assign_role, guild_id=guild_id, user_id=int(user_id), role_id=int(role_id))

    def execute_channel_perms(self):
        if not self.is_premium:
            self.log_message("Error: Unlock premium first.")
            return
        guild_id = self.get_guild_id(self.utility_guild_id_entry)
        channel_id = self.utility_channel_id_entry.get()
        if not guild_id:
            self.log_message("Error: No Guild ID set in Utility section or Settings. Enter one!")
            return
        if not channel_id or not channel_id.isdigit():
            self.log_message("Error: No Channel ID set in Utility section. Enter a valid ID!")
            return

        if not self.channel_perms_check.get():
            self.log_message("Error: Lock/Unlock Channel not enabled. Enable it!")
            return

        action = self.channel_perms_option.get()
        lock = True if action == "Lock" else False
        self.log_message(f"{'Locking' if lock else 'Unlocking'} Channel ID: {channel_id} on Guild ID: {guild_id}...")
        self.run_action_in_thread(self.utility_actions.lock_unlock_channel, guild_id=guild_id, channel_id=int(channel_id), lock=lock)

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainGUI(root)
    root.mainloop()
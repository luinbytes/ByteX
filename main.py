import asyncio
import importlib
import string
import os
import json
import sys
import webbrowser

import aiohttp
import dearpygui.dearpygui as dpg
import discord
from discord import Webhook, webhook
from discord.ext import commands, tasks
import threading
import requests
import urllib

# Create context
dpg.create_context()

# Create Bot
class ByteX(commands.Bot):
    def __init__(self):
        prefix_str = get_config_element("prefix")
        super().__init__(command_prefix=prefix_str)
        self.client = discord.Client()

    async def on_ready(self):
        await self.load_cogs()
        self.download_avatar()

        # Update Globals
        log(INFO, "Updating globals...", debug=True)
        username = self.user.name
        servers = len(self.guilds)

        dpg.set_value("username", f"Username: {username}")
        dpg.set_value("status", f"Status: {status}")
        dpg.set_value("servers", f"Servers: {servers}")

        log(SUCCESS, "Bot is ready", debug=True)
        log(SUCCESS, f"Logged in as {self.user.name}", debug=False)

    def download_avatar(self):
        bot = ByteX()
        log(INFO, "Downloading avatar...", debug=True)
        try:
            if not os.path.exists(os.path.join(os.getenv("APPDATA"), "ByteX", "avatar", "avatar.png")):
                url = self.user.avatar.url
                requests.get(url)
                img_data = requests.get(url).content
                with open(os.path.join(os.getenv("APPDATA"), "ByteX", "avatar", "avatar.png"), "wb") as f:
                    f.write(img_data)
                log(SUCCESS, "Avatar downloaded successfully", debug=True)
            else:
                log(INFO, "Avatar already exists", debug=True)
        except Exception as e:
            log(ERROR, f"Error downloading avatar, check debug console for more details.", debug=False)
            log(ERROR, f"Error downloading avatar: {e}", debug=True)

        # Set Default Status
        # status = get_config_element("default_status").lower()
        # try:
        #     log(INFO, "Setting default status...", debug=True)
        #     await bot.change_presence(status=status_mapping[status], activity=discord.CustomActivity(name="ByteX"))
        # except Exception as e:
        #     log(ERROR, f"Error setting default status: {e}", debug=True)
        # await bot.change_presence(status=status_mapping[status], activity=discord.CustomActivity(name="ByteX"))

    async def on_message(self, message):
        ctx = await self.get_context(message)
        if message.author == self.user:
            if message.content.startswith(get_config_element("prefix")):
                if self.check_command_exists(message.content.split(" ")[0][2:]):
                    await self.run_command(ctx, message.content.split(" ")[0][2:], message)
                else:
                    await ctx.send("Command not found.")

    async def load_cogs(self):
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    log(ERROR, f"Failed to load extension {extension}: {exception}", debug=True)

    def check_command_exists(self, command_name):
        command = self.get_command(command_name)
        return command is not None

    async def run_command(self, ctx, command_name, message):
        command = self.get_command(command_name)
        if command:
            args = message.content.split()[1:]  # Get the arguments after the command
            log(SUCCESS, f"Command '{command_name}' executed successfully", debug=False)
            await ctx.invoke(command, *args)
        else:
            await ctx.send(f"Command '{command_name}' does not exist.")

    async def stop_bot(self):
        await self.client.close()

global bot

global VERSION
global username
global status
global servers
global friends
global avatar_texture

VERSION = "[Alpha] v0.2.5"
username = None
status = None
servers = None
friends = None
avatar_texture = None

status_mapping = {
    "online": discord.Status.online,
    "offline": discord.Status.offline,
    "idle": discord.Status.idle,
    "dnd": discord.Status.dnd
}

# Set up logging
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
SUCCESS = "SUCCESS"

LOG_TYPES = {
    INFO: "INFO",
    WARNING: "WARNING",
    ERROR: "ERROR",
    SUCCESS: "SUCCESS"
}

# Logging
def log(type, message, debug=False):
    if dpg.does_item_exist("console") is False:
        print(f"[{LOG_TYPES[type]}]: {message}")
    else:
        if debug:
            debug_console = dpg.get_item_info("debug_console")
            debug_console_text = dpg.get_value("debug_console")
            debug_console_text += f"[{LOG_TYPES[type]}]: {message}\n"
            dpg.set_value("debug_console", debug_console_text)
        else:
            console = dpg.get_item_info("console")
            console_text = dpg.get_value("console")
            console_text += f"[{LOG_TYPES[type]}]: {message}\n"
            dpg.set_value("console", console_text)

# Filesystem setup
default_config = {
    "token": "YOUR_TOKEN_HERE",
    "prefix": "//",
    "deletion_delay": "20",
    "default_status": "Online",

    "log_webhook": "WEBHOOK_URL_HERE",
    "theme": "Dark",
}

def setup_filesystem():
    log(INFO, "Running filesystem checks...", debug=True)
    appdata = os.getenv("APPDATA")
    bytex_path = os.path.join(appdata, "ByteX")

    if not os.path.exists(bytex_path):
        os.mkdir(bytex_path)
        log(INFO, f"Path {bytex_path} created", debug=True)

    log(INFO, "Checking if config.json exists...", debug=True)
    config_path = os.path.join(bytex_path, "config.json")

    try:
        if os.path.exists(config_path):
            log(INFO, "Config file exists", debug=True)
        else:
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=4)
            log(INFO, "Config file created", debug=True)
    except Exception as e:
        log(ERROR, f"Error creating config file: {e}", debug=True)

    subdirs = ["resources", "rpc", "img", "sound", "avatar", "cogs"]

    paths = []
    for subdir in subdirs:
        path = os.path.join(bytex_path, subdir)
        paths.append(path)

    for path in paths:
        try:
            if os.path.exists(path):
                log(INFO, f"Path {path} exists", debug=True)
            else:
                os.mkdir(path)
                log(INFO, f"Path {path} created", debug=True)
        except Exception as e:
            log(ERROR, f"Error creating path {path}: {e}", debug=True)
    log(SUCCESS, "Filesystem checks complete", debug=True)

def update_config_element(element, value):
    appdata = os.getenv("APPDATA")
    bytex_path = os.path.join(appdata, "ByteX")
    config_path = os.path.join(bytex_path, "config.json")
    if not os.path.exists(bytex_path):
        try:
            os.mkdir(bytex_path)
            if not os.path.exists(config_path):
                with open(config_path, "w") as f:
                    json.dump(default_config, f)
        except Exception as e:
            log(ERROR, f"Error creating path {bytex_path}: {e}", debug=True)

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            config[element] = value
        with open(config_path, "w") as f:
            json.dump(config, f)
    except Exception as e:
        log(ERROR, f"Error updating config element {element}: {e}", debug=True)

def get_config_element(element):
    appdata = os.getenv("APPDATA")
    bytex_path = os.path.join(appdata, "ByteX")
    config_path = os.path.join(bytex_path, "config.json")

    if not os.path.exists(bytex_path):
        try:
            os.mkdir(bytex_path)
        except Exception as e:
            log(ERROR, f"Error creating path {bytex_path}: {e}", debug=True)
            return None

    if not os.path.exists(config_path):
        try:
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=4)
            log(INFO, "Config file created", debug=True)
        except Exception as e:
            log(ERROR, f"Error creating config file: {e}", debug=True)
            return None

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            if element in config:
                return config[element]
            else:
                log(ERROR, f"Element '{element}' not found in config file", debug=True)
                return None
    except Exception as e:
        log(ERROR, f"Error accessing config element '{element}': {e}", debug=True)
        return None


# Define light theme
with dpg.theme() as light_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (220, 220, 220, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (180, 180, 180, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (220, 220, 220, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (200, 200, 200, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Tab, (190, 190, 190, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (170, 170, 170, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TabActive, (150, 150, 150, 255))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5.0)

# Define dark theme
with dpg.theme() as dark_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Button, (70, 70, 70, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (90, 90, 90, 255))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (110, 110, 110, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (40, 40, 40, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (60, 60, 60, 255))
        dpg.add_theme_color(dpg.mvThemeCol_Tab, (50, 50, 50, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (70, 70, 70, 255))
        dpg.add_theme_color(dpg.mvThemeCol_TabActive, (90, 90, 90, 255))
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5.0)

def bind_theme():
    if get_config_element("theme") == "Light":
        dpg.bind_theme(light_theme)
        log(INFO, "Light theme applied", debug=True)
    else:
        dpg.bind_theme(dark_theme)
        log(INFO, "Dark theme applied", debug=True)

import aiohttp
from discord import Webhook
import asyncio

def save_user_settings(sender, app_data, user_data):
    username = dpg.get_value("username_input")
    status = dpg.get_value("default_startup_status")
    # Save user settings to config.json
    try:
        update_config_element("default_status", status)
        log(INFO, f"Saving User Settings: Status: {status}", debug=True)
    except Exception as e:
        log(ERROR, f"Error saving user settings: {e}", debug=True)


def save_rpc_settings(sender, app_data, user_data):
    rpc_setting = dpg.get_value("rpc_setting_input")
    log(INFO, f"Saving RPC Settings: RPC Setting: {rpc_setting}", debug=True)
    # Implement save logic


def save_config_settings(sender, app_data, user_data):
    config_setting = dpg.get_value("config_setting_input")
    log(INFO, f"Saving Config Settings: Config Setting: {config_setting}", debug=True)
    # Implement save logic


def save_theme_settings(sender, app_data, user_data):
    theme_setting = dpg.get_value("theme_setting_input")
    if theme_setting == "Light":
        dpg.bind_theme(light_theme)
    else:
        dpg.bind_theme(dark_theme)
    # Save theme setting to config.json
    try:
        update_config_element("theme", theme_setting)
        log(INFO, f"Saving Theme Settings: Theme Setting: {theme_setting}", debug=True)
    except Exception as e:
        log(ERROR, f"Error saving theme setting: {e}", debug=True)

def about_bytex():
    log(INFO, f"--- ABOUT ByteX {VERSION} ---", debug=False)
    log(INFO, "ByteX is a Discord bot client that allows you to manage your Discord bot with ease.", debug=False)
    log(INFO, "ByteX is currently in alpha and is not recommended for production use.", debug=False)
    log(INFO, "Infinitely customizable.", debug=False)
    log(INFO, "--- ByteX Credits ---", debug=False)
    log(INFO, "Developed by @0x6c75.", debug=False)
    log(INFO, "ByteX is powered by Discord.py-self and DearPyGui.", debug=False)

def about_developer():
    log(INFO, f"--- ABOUT DEVELOPER ---", debug=False)
    log(INFO, "0x6c75 (luinbytes) is a software developer and cybersecurity enthusiast.", debug=False)
    log(INFO, "He is the developer of ByteX, ByteBot, U-RCS and old gems such as nxzUI.", debug=False)
    log(INFO, "Github: https://github.com/luinytes")
    log(INFO, "Discord: @0x6c75")

def support_server():
    log(INFO, "--- ByteX SUPPORT SERVER ---", debug=False)
    log(INFO, "Need help with ByteX? Join the ByteX support server!", debug=False)
    log(INFO, "Join the ByteX support server: https://discord.gg/ADzuh7EEQB")

def open_folder():
    log(INFO, "Opening ByteX folder...", debug=False)
    try:
        os.system("start %appdata%/ByteX")
    except Exception as e:
        log(ERROR, f"Error opening ByteX folder, check debug console for more details.", debug=False)
        log(ERROR, f"Error opening the ByteX folder: {e}", debug=True)

def browse_cogs():
    log(INFO, "Browsing cogs...", debug=False)
    try:
        webbrowser.open("https://github.com/luinbytes/ByteX-Modules")
    except Exception as e:
        log(ERROR, f"Error browsing cogs, check debug console for more details.", debug=False)
        log(ERROR, f"Error browsing cogs: {e}", debug=True)

async def refresh_cogs():
    bot = ByteX()
    for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            current_cogs.append(extension)

    # Store first cog as default
    if not dpg.does_item_exist("cog_input"):
        return
    else:
        if len(current_cogs) > 0:
            dpg.set_value("cog_input", current_cogs[0])

    try:
        await bot.load_extension(f"cogs.{extension}")
        log(SUCCESS, f"Loaded extension '{extension}'", debug=True)
    except Exception as e:
        exception = f"{type(e).__name__}: {e}"
        log(ERROR, f"Failed to load extension {extension}: {exception}", debug=True)

def show_cogs():
    cog = dpg.get_value("cog_input")
    if not os.path.exists(f"{os.path.realpath(os.path.dirname(__file__))}/cogs/{cog}.py"):
        log(ERROR, f"Cog {cog} not found!", debug=False)
        return

    with open(f"{os.path.realpath(os.path.dirname(__file__))}/cogs/{cog}.py", "r") as f:
        source = f.read()
        dpg.set_value("cog_src_display", source)

def exit():
    log(INFO, "Exiting ByteX...", debug=False)
    try:
        dpg.stop_dearpygui()
        dpg.destroy_context()
    except Exception as e:
        log(ERROR, f"Error exiting ByteX, check debug console for more details.", debug=False)
        log(ERROR, f"Error exiting ByteX: {e}", debug=True)
def force_exit():
    log(INFO, "Force exiting ByteX...", debug=True)
    global bot
    global bot_thread

    try:
        log(INFO, "Stopping bot...", debug=True)
        asyncio.run(bot.close())
        log(INFO, "Joining thread...", debug=True)
        bot_thread.join()
    except Exception as e:
        log(ERROR, f"Error stopping bot: {e}", debug=True)

    # Stop DearPyGui
    log(INFO, "Stopping DearPyGui...", debug=True)
    dpg.stop_dearpygui()

if os.path.exists(os.path.join(os.getenv("APPDATA"), "ByteX", "avatar", "avatar.png")):
    width, height, channels, data = dpg.load_image(os.path.join(os.getenv("APPDATA"), "ByteX", "avatar", "avatar.png"))

    with dpg.texture_registry():
        avatar_texture = dpg.add_static_texture(width, height, data, tag="avatar_texture")

# Main window
with dpg.window(label=f"ByteX {VERSION}", tag="welcome_banner", width=800, height=400, no_collapse=True, no_resize=True, no_move=True, pos=(0, 0), no_close=False, on_close=force_exit):
    with dpg.menu_bar():
        with dpg.menu(label="About"):
            dpg.add_menu_item(label="About ByteX", callback=about_bytex)
            dpg.add_menu_item(label="About Developer", callback=about_developer)

        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="Discord Support Server", callback=support_server)
            dpg.add_menu_item(label="Report Bug", callback=support_server)

        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Open Folder", callback=open_folder)
            dpg.add_menu_item(label="Restart", callback=exit)
            dpg.add_menu_item(label="Exit", callback=exit)

        dpg.add_menu_item(label="Exit", callback=force_exit)

    with dpg.tab_bar():
        # User Settings Tab
        with dpg.tab(label="User Settings"):
            if not os.path.exists(os.path.join(os.getenv("APPDATA"), "ByteX", "avatar", "avatar.png")):
                with dpg.group(horizontal=False, tag="user_settings_group"):
                    dpg.add_text("No avatar found, ByteX should download it automatically.")
                    dpg.add_text("Restart ByteX once authed to show avatar.")
                    dpg.add_text("Or you can set your own. Your Avatar is only downloaded once.")
                    dpg.add_button(label="Open ByteX Folder", callback=open_folder)
            else:
                with dpg.group(horizontal=True, tag="user_settings_group"):
                    dpg.add_image("avatar_texture", width=100, height=100, border_color=(255, 255, 255, 255), tag="avatar_image")

            with dpg.group():
                dpg.add_text("Waiting for auth...", tag="username")
                dpg.add_text("Status: Offline", tag="status")
                dpg.add_text("Servers: 0", tag="servers")

            dpg.add_spacer(height=20)

            dpg.add_text("Edit User Settings")
            dpg.add_combo(label="Startup Status [Broken]", items=["Online", "Idle", "Do Not Disturb", "Invisible"], tag="default_startup_status")
            dpg.add_button(label="Save User Settings", callback=save_user_settings)

        # RPC Settings Tab
        with dpg.tab(label="RPC Settings"):
            dpg.add_combo(label="RPC Profile", items=["Default", "Custom"], tag="rpc_profile_input", default_value="Default", width=200)
            dpg.add_spacer(height=20)
            with dpg.group(horizontal=False):
                dpg.add_text("Main RPC Settings")
                dpg.add_combo(label="Status", items=["Playing", "Watching", "Streaming", "Listening"], tag="rpc_status_input", default_value="Playing")

        # Steam Tools Tab
        with dpg.tab(label="Steam Tools"):
            with dpg.group(horizontal=True):
                with dpg.group(horizontal=False):
                    dpg.add_text("Steam ID")
                    dpg.add_input_text(hint="Enter Steam ID", width=200)
                    dpg.add_button(label="Get Steam Profile")

        # Spy  Settings Tab
        with dpg.tab(label="ByteSpy Settings"):
            with dpg.group(horizontal=True):
                with dpg.group(horizontal=False):
                    dpg.add_text("Users to Spy On")
                    dpg.add_input_text(tag="current_users", hint="Users currently being spied on", width=200, height=140,
                                       multiline=True, readonly=True)

                with dpg.group(horizontal=True):
                    # Recent Messages
                    with dpg.group(horizontal=False):
                        dpg.add_text("Recent Messages")
                        dpg.add_input_text(hint="Recent messages with user", width=390, height=140, multiline=True,
                                           readonly=True)

                with dpg.group(horizontal=False):
                    with dpg.group(horizontal=False):
                        dpg.add_spacer(height=20)
                        dpg.add_input_text(tag="add_user", hint="Enter user ID")
                        dpg.add_button(label="Add User")
                        dpg.add_same_line()
                        dpg.add_spacer(width=17)
                        dpg.add_same_line()
                        dpg.add_button(label="Remove User")

            with dpg.group(horizontal=True):
                #with dpg.group(horizontal=False):
                    #dpg.add_image("avatar_texture2", width=120, height=110, border_color=(255, 255, 255, 255))

                # Spy information
                with dpg.group(horizontal=False):
                    dpg.add_text("Users Spy Information")
                    dpg.add_text("User ID: 0x6c75")
                    dpg.add_text("Status: Online")
                    dpg.add_text("Mutual Servers: 10")
                    dpg.add_text("Mutual Friends: 5")

        # Config Settings Tab
        with dpg.tab(label="Cog Settings"):
            current_cogs = []
            while not os.path.exists(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
                log(INFO, "cogs dir not found! Creating cogs directory...", debug=True)
                os.mkdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs")

            with dpg.group(horizontal=False):
                dpg.add_text("Current Cogs")
                dpg.add_combo(items=current_cogs, tag="cog_input", width=287, default_value="None")
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Refresh Cogs", width=140, callback=asyncio.run(refresh_cogs()))
                    dpg.add_button(label="Show cog", width=140, callback=show_cogs)

            with dpg.group(horizontal=True):
                with dpg.group(horizontal=False):
                    dpg.add_text("Cog Source")
                    dpg.add_input_text(hint="Cog source will appear here.", tag="cog_src_display", width=400, height=200, multiline=True, readonly=True)
            with dpg.group(horizontal=False):
                with dpg.group(horizontal=True):
                    dpg.add_text("Cogs are hosted and updated on github.com/luinytes/ByteX-Modules")
                    dpg.add_button(label="Browse Cogs", width=140, callback=browse_cogs)

        # Theme Settings Tab
        with dpg.tab(label="Theme Settings"):
            if os.path.exists(os.path.join(os.getenv("APPDATA"), "ByteX", "config.json")):
                dpg.add_combo(label="Theme", items=["Light", "Dark"], tag="theme_setting_input", default_value=get_config_element("theme"))
            else:
                dpg.add_combo(label="Theme", items=["Light", "Dark"], tag="theme_setting_input", default_value="Dark")
            dpg.add_button(label="Save Theme Settings", callback=save_theme_settings)

# Console Window
with dpg.window(width=800, height=200, no_collapse=True, no_resize=True, no_title_bar=True, no_move=True, pos=(0, 400), max_size=(800, 200), min_size=(800, 200)):
    with dpg.tab_bar():
        # Console tab
        with dpg.tab(label="Console"):
            dpg.add_input_text(hint="Welcome to ByteX Console", tag="console", multiline=True, readonly=True, width=780, height=160)

        # Debug tab
        with dpg.tab(label="Debug"):
            dpg.add_input_text(hint="Welcome to ByteX Debug Console", tag="debug_console", multiline=True, readonly=True, width=780, height=160)

# Discord Functions
def start_bot():
    global bot
    bot = ByteX()
    try:
        log(INFO, "Starting bot...", debug=False)
        bot.run(get_config_element("token"))
    except Exception as e:
        log(ERROR, f"There was an error starting the bot, check debug for more details...", debug=False)
        log(ERROR, f"Error starting bot: {e}", debug=True)

async def update_status():
    bot = ByteX()
    status = get_config_element("default_status").lower()
    try:
        log(INFO, "Setting default status...", debug=True)
        await bot.change_presence(status=status_mapping[status], activity=discord.CustomActivity(name="ByteX"))
    except Exception as e:
        log(ERROR, f"Error setting default status: {e}", debug=True)
        await bot.change_presence(status=status_mapping[status], activity=discord.CustomActivity(name="ByteX"))

# Main entry point
if __name__ == "__main__":
    global bot
    global bot_thread
    try:
        setup_filesystem()  # Ensure filesystem is set up correctly
    except Exception as e:
        log(ERROR, f"Error setting up filesystem: {e}", debug=True)
    bind_theme()  # Bind the correct theme based on config

    # Start the bot in the main thread
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    asyncio.run(refresh_cogs())

    dpg.create_context()
    dpg.create_viewport(title='ByteX', width=815, height=638, resizable=False, disable_close=True)

    dpg.setup_dearpygui()

    dpg.show_viewport()

    # Start DearPyGui event loop
    dpg.start_dearpygui()

    # Cleanup after DearPyGui exits
    dpg.destroy_context()


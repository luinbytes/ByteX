"""A demo script to showcase the Sun Valley ttk theme."""
import json
import tkinter
import customtkinter as cttk
import os
import sys
import discord
from urllib.request import urlretrieve
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import ImageDraw

class CollapsibleFrame(cttk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self._is_collapsed = False

        self.toggle_button = cttk.CTkButton(self, text="→", command=self.toggle, width=60, height=24, border_spacing=10, border_color="black")
        self.toggle_button.pack(side="bottom", padx=10, pady=10)

        self.user_settings_button = cttk.CTkButton(self, text="⚙️", command=self.app.show_user_settings, width=60, height=24, border_spacing=10)
        self.user_settings_button.pack(padx=10, pady=10)

        self.rpc_settings_button = cttk.CTkButton(self, text="🪧", command=self.app.show_rpc_settings, width=60, height=24, border_spacing=10)
        self.rpc_settings_button.pack(padx=10, pady=(0, 10))

        self.collapse()

    def toggle(self):
        if self._is_collapsed:
            self.expand()
        else:
            self.collapse()

    def collapse(self):
        self._is_collapsed = True
        self.toggle_button.configure(text="→", width=60, height=24)
        self.user_settings_button.configure(text="⚙️", width=60, height=24)
        self.rpc_settings_button.configure(text="🪧", width=60, height=24)


    def expand(self):
        self._is_collapsed = False
        self.toggle_button.configure(text="←", width=120, height=24)
        self.user_settings_button.configure(text="⚙️ User Settings", width=120, height=24)
        self.rpc_settings_button.configure(text="🪧 RPC Settings", width=120, height=24)
class UserInfoPanel(cttk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.username = cttk.StringVar(self, value="luinbytes!")
        self.status = cttk.StringVar(self, value="Online")
        self.servers = cttk.StringVar(self, value="30")

        image_path = "C:/Users/Lu/Pictures/Screenshot 2024-05-13 195753.png"
        border_path = "./resources/img/avatar_border.png"

        img = Image.open(image_path)

        new_size = (100, 90)
        img = img.resize(new_size)

        circle_img = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(circle_img)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
        img.putalpha(circle_img)

        border_img = Image.open(border_path)
        border_img = border_img.resize((125, 110))
        final_img = Image.new('RGBA', border_img.size)

        avatar_position = ((border_img.width - img.width) // 2, (border_img.height - img.height) // 2)
        final_img.paste(img, avatar_position)
        final_img.paste(border_img, (0, 0), border_img)

        self.avatar_image = cttk.CTkImage(final_img, size=(100, 100))
        self.app.log("WARN", f"Avatar image size: {final_img.width}x{final_img.height}")  # Print the size of the image

        self.add_widgets()

    def add_widgets(self):
        self.avatar_label = cttk.CTkLabel(self, image=self.avatar_image, text="")
        self.avatar_label.grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.username_label = cttk.CTkLabel(self, text="Welcome back,", font=("Helvetica", 12, "bold"))
        self.username_label.grid(row=1, column=0, pady=(0, 10), padx=(10, 0), sticky="w")

        self.username_value = cttk.CTkLabel(self, textvariable=self.username, font=("Helvetica", 12))
        self.username_value.grid(row=1, column=1, pady=(0, 10), padx=(10, 0), sticky="w")

        self.status_label = cttk.CTkLabel(self, text="Status:", font=("Helvetica", 12, "bold"))
        self.status_label.grid(row=2, column=0, pady=(0, 10), padx=(10, 0), sticky="w")

        self.status_value = cttk.CTkLabel(self, textvariable=self.status, font=("Helvetica", 12))
        self.status_value.grid(row=2, column=1, pady=(0, 10), padx=(10, 0), sticky="w")

        self.servers_label = cttk.CTkLabel(self, text="Servers:", font=("Helvetica", 12, "bold"))
        self.servers_label.grid(row=3, column=0, pady=(0, 10), padx=(10, 0), sticky="w")

        self.servers_value = cttk.CTkLabel(self, textvariable=self.servers, font=("Helvetica", 12))
        self.servers_value.grid(row=3, column=1, pady=(0, 10), padx=(10, 0), sticky="w")

class UserController(cttk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Store the App instance
        self.add_widgets()

    def add_widgets(self):
        self.status_dropdown = cttk.CTkComboBox(self, values=["Online", "Idle", "Do Not Disturb", "Invisible"], state="readonly")
        self.status_dropdown.set("Online")
        self.status_dropdown.grid(row=0, column=0, pady=(10, 10), padx=(10, 0), sticky="ew")

        self.update_button = cttk.CTkButton(self, text="Update Status", command=self.update_status)
        self.update_button.grid(row=1, column=0, pady=(0, 10), padx=(10, 0), sticky="ew")

    def update_status(self):
        status = self.status_dropdown.get()
        self.app.log("INFO", f"Simulating updating status to {status}...")

class RPCSettings(cttk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app  # Store the App instance
        self.rpc_master_var = cttk.BooleanVar(self, value=False)
        self.add_widgets()

    def add_widgets(self):
        self.rpc_master = cttk.CTkCheckBox(self, text="Enable RPC", variable=self.rpc_master_var)
        self.rpc_master.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.rpc_title_label = cttk.CTkLabel(self, text="Title:", font=("Helvetica", 12, "bold"))
        self.rpc_title_textbox = cttk.CTkEntry(self)
        self.rpc_title_label.grid(row=1, column=0, pady=(0, 10), padx=(10, 0), sticky="w")
        self.rpc_title_textbox.grid(row=1, column=1, pady=(0, 10), padx=(10, 0), sticky="w")

class App(cttk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.sidebar = CollapsibleFrame(self, self)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = cttk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

        # Create a Text widget for console output
        self.console = tkinter.Text(self.main_frame, bd=0, bg="#2b2b2b", fg="white", insertbackground="white", font=("Consolas", 10), wrap="word")
        self.console.grid(row=1, column=0, columnspan=2, padx=(0, 10), pady=(0, 20), sticky="nsew")

        # Set the weight of the first row (row 0) to 3 and the second row (row 1, which contains the console) to 1
        # This means that the first row will take up 75% of the vertical space (3 out of 4 parts), and the second row will take up 25% of the vertical space (1 out of 4 parts)
        self.main_frame.grid_rowconfigure(0, weight=3)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.user_info_panel = UserInfoPanel(self.main_frame, self)
        self.user_info_panel.grid(row=0, column=0, padx=(0, 10), pady=(10, 10), sticky="nsew")
        self.user_controller = UserController(self.main_frame, self)
        self.user_controller.grid(row=0, column=1, padx=(0, 10), pady=(10, 10), sticky="nsew")

        # RPC
        self.rpc_settings = RPCSettings(self.main_frame, self)
        self.rpc_settings.grid(row=0, column=0, padx=(0, 10), pady=(10, 10), sticky="nsew")
        self.rpc_settings.grid_remove()


    SEVERITY_COLORS = {
        "INFO": "white",
        "SUCC": "green",
        "WARN": "orange",
        "ERROR": "red",
    }

    def log(self, severity, message):
        severity = severity.upper()
        color = self.SEVERITY_COLORS.get(severity, "black")

        # Define a tag with the desired color
        self.console.tag_config(severity, foreground=color)

        # Insert the text with the color tag
        self.console.insert(tkinter.END, "[" + severity + "] " + message + "\n", severity)

        self.console.see(tkinter.END)

    def show_user_settings(self):
        self.rpc_settings.grid_remove()

        self.user_info_panel.grid()
        self.user_controller.grid()

        self.log("INFO", "Showing user settings...")

    def show_rpc_settings(self):
        # Hide the UserInfoPanel and UserController
        self.user_info_panel.grid_remove()
        self.user_controller.grid_remove()

        # Show the RPCSettings
        self.rpc_settings.grid()

        self.log("INFO", "Showing RPC settings...")


def main():
    # Create the root window
    root = cttk.CTk()
    root.title("ByteX")

    cttk.set_appearance_mode("dark")
    cttk.set_default_color_theme("blue")


    app = App(root)
    app.pack(expand=True, fill="both")
    app.log("INFO","Starting ByteX...")

    # Create the ByteX folder in the AppData directory
    appdata = os.getenv("APPDATA")
    bytex_path = os.path.join(appdata, 'ByteX')
    resource_path = os.path.join(bytex_path, 'resources')
    img_path = os.path.join(resource_path, 'img')
    rpc_path = os.path.join(bytex_path, 'rpc')


    # Check if the ByteX folder exists
    app.log("INFO", "Checking if ByteX folder exists")
    if not os.path.exists(bytex_path):
        os.makedirs(bytex_path)
        app.log("WARN", "Created ByteX folder in AppData directory")
    else:
        app.log("SUCC", "ByteX folder already exists")

    # Check if the resources folder exists
    app.log("INFO", "Checking if resources folder exists")
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
        app.log("WARN", "Created resources folder in ByteX folder")
    else:
        app.log("SUCC", "resources folder already exists")

    # Check if the img folder exists
    app.log("INFO", "Checking if img folder exists")
    if not os.path.exists(img_path):
        os.makedirs(img_path)
        app.log("WARN", "Created img folder in resources folder")
    else:
        app.log("SUCC", "img folder already exists")

    # Check if the rpc folder exists
    app.log("INFO", "Checking if rpc folder exists")
    if not os.path.exists(rpc_path):
        os.makedirs(rpc_path)
        app.log("WARN", "Created rpc folder in ByteX folder")
    else:
        app.log("SUCC", "rpc folder already exists")

    # Create a default RPC json
    default_rpc_path = os.path.join(rpc_path, 'default.json')
    default_rpc = {
        "title": "ByteX",
        "type": "playing",
        "state": "Dubious Little Guy Inc.",
        "details": "Made By 0x6c75",
        "large_image": "https://media1.tenor.com/m/7sw5JRPIpLMAAAAC/cat-cate.gif",
        "large_text": "ermmmmm",
        "small_image": "https://cdn.discordapp.com/emojis/725077188843667639.gif?size=80&amp;quality=lossless",
        "small_text": "ermmmmm",
        "button_text": "ByteX Discord",
        "button_url": "https://discord.gg/ADzuh7EEQB",
        "button2_text": None,
        "button2_url": None,
        "timer": True,
        "party": [
            None,
            None
        ]
    }

    app.log("INFO", "Checking if RPC default.json exists")
    if not os.path.exists(default_rpc_path):
        with open(default_rpc_path, 'w') as f:
            json.dump(default_rpc, f, indent=4)
        app.log("WARN", "Created default.json in rpc folder")
    else:
        app.log("SUCC", "default.json already exists")

    # Check if the main config.json exists
    config_path = os.path.join(bytex_path, 'config.json')
    default_config = {
        "token": "token",
        "prefix": "//",
        "status": "online",
    }

    app.log("INFO", "Checking if config.json exists")
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        app.log("WARN", "Created config.json in ByteX folder")
    else:
        app.log("SUCC", "config.json already exists")

    root.mainloop()

if __name__ == "__main__":
    main()
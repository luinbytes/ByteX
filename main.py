"""A demo script to showcase the Sun Valley ttk theme."""
import json
import tkinter
import sv_ttk
import os
import sys
import discord
from urllib.request import urlretrieve
from tkinter import ttk
from PIL import Image, ImageTk
from PIL import ImageDraw

class CollapsibleFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self._is_collapsed = False

        style = ttk.Style()

        # Define a new style called 'Pink.TButton' that inherits from 'TButton'
        style.element_create('Pink.TButton', 'from', 'alt')

        # Modify the background field of the layout
        style.layout('Pink.TButton', [
            ('Pink.TButton.button', {'children':
                                         [('Button.focus', {'children':
                                                                [('Button.padding', {'children':
                                                                                         [('Button.label',
                                                                                           {'side': 'left',
                                                                                            'expand': 1})],
                                                                                     'expand': 1})],
                                                            'expand': 1})],
                                     'sticky': 'nswe'})])

        style.configure('Pink.TButton', background='light pink', foreground='black')

        self.toggle_button = ttk.Button(self, text="☰", command=self.toggle, style="Pink.TButton", takefocus=0)
        self.toggle_button.pack(padx=(0, 10), fill='x')

        self.user_settings_label = ttk.Label(self, text="User Settings", font=("Helvetica", 10), anchor="w")
        self.user_settings_button = ttk.Button(self, text="⚙️")
        self.user_settings_button.pack(padx=(0, 10), pady=10, fill='x')

        self.rpc_settings_label = ttk.Label(self, text="RPC Settings", font=("Helvetica", 10), anchor="w")
        self.rpc_settings_button = ttk.Button(self, text="🪧")
        self.rpc_settings_button.pack(padx=(0, 10), fill='x')

        self.collapse()

    def toggle(self):
        if self._is_collapsed:
            self.expand()
        else:
            self.collapse()

    def collapse(self):
        self._is_collapsed = True
        self.user_settings_label.pack_forget()
        self.rpc_settings_label.pack_forget()
        self.rpc_settings_button.pack_forget()
        self.rpc_settings_button.pack(padx=(0, 10), fill='x')

    def expand(self):
        self._is_collapsed = False
        self.rpc_settings_button.pack_forget()
        self.user_settings_label.pack(padx=(0, 10), fill='x')
        self.rpc_settings_button.pack(padx=(0, 10), pady=10, fill='x')
        self.rpc_settings_label.pack(padx=(0, 10), fill='x')
class UserInfoPanel(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="User Info", padding=15)

        self.username = tkinter.StringVar(self, value="luinbytes!")
        self.status = tkinter.StringVar(self, value="Online")
        self.servers = tkinter.StringVar(self, value="30")

        image_path = "C:/Users/Lu/Pictures/Screenshot 2024-05-13 195753.png"
        border_path = "./resources/img/avatar_border.png"

        img = Image.open(image_path)

        max_size = (100, 100)
        img.thumbnail(max_size)

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

        self.avatar_image = ImageTk.PhotoImage(final_img)

        self.add_widgets()

    def add_widgets(self):
        self.avatar_label = ttk.Label(self, image=self.avatar_image)
        self.avatar_label.grid(row=0, column=0, pady=(0, 10), sticky="w")

        self.username_label = ttk.Label(self, text="Welcome back,", font=("Helvetica", 12, "bold"))
        self.username_label.grid(row=1, column=0, pady=(0, 10), padx=(10, 0), sticky="w")

        self.username_value = ttk.Label(self, textvariable=self.username, font=("Helvetica", 12))
        self.username_value.grid(row=1, column=1, pady=(0, 10), padx=(10, 0), sticky="w")

        self.status_label = ttk.Label(self, text="Status:", font=("Helvetica", 12, "bold"))
        self.status_label.grid(row=2, column=0, pady=(0, 10), padx=(10, 0), sticky="w")

        self.status_value = ttk.Label(self, textvariable=self.status, font=("Helvetica", 12))
        self.status_value.grid(row=2, column=1, pady=(0, 10), padx=(10, 0), sticky="w")

        self.servers_label = ttk.Label(self, text="Servers:", font=("Helvetica", 12, "bold"))
        self.servers_label.grid(row=3, column=0, pady=(0, 10), padx=(10, 0), sticky="w")

        self.servers_value = ttk.Label(self, textvariable=self.servers, font=("Helvetica", 12))
        self.servers_value.grid(row=3, column=1, pady=(0, 10), padx=(10, 0), sticky="w")

class UserController(ttk.LabelFrame):
    def __init__(self, parent, app):
        super().__init__(parent, text="User Control", padding=15)
        self.app = app  # Store the App instance
        self.add_widgets()

    def add_widgets(self):
        self.status_dropdown = ttk.Combobox(self, values=["Online", "Idle", "Do Not Disturb", "Invisible"], state="readonly")
        self.status_dropdown.set("Online")
        self.status_dropdown.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        self.update_button = ttk.Button(self, text="Update Status", command=self.update_status)
        self.update_button.grid(row=1, column=0, pady=(0, 10), sticky="ew")

    def update_status(self):
        status = self.status_dropdown.get()
        self.app.log("INFO", f"Simulating updating status to {status}...")

class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.sidebar = CollapsibleFrame(self)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

        UserInfoPanel(self.main_frame).grid(row=0, column=0, padx=(0, 10), pady=(0, 20), sticky="nsew")
        UserController(self.main_frame, self).grid(row=0, column=1, padx=(0, 10), pady=(0, 20), sticky="nsew")

        # Create a Text widget for console output
        self.console = tkinter.Text(self.main_frame, bd=0, bg="#2b2b2b", fg="white", insertbackground="white")
        self.console.grid(row=1, column=0, columnspan=2, padx=(0, 10), pady=(0, 20), sticky="nsew")

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


def main():
    # Create the root window
    root = tkinter.Tk()
    root.title("ByteX")

    sv_ttk.set_theme("dark")

    app = App(root)
    app.pack(expand=True, fill="both")
    app.log("INFO","Starting ByteX...")

    # Create the ByteX folder in the AppData directory
    appdata = os.getenv("APPDATA")
    bytex_path = os.path.join(appdata, 'ByteX')
    resource_path = os.path.join(bytex_path, 'resources')
    img_path = os.path.join(resource_path, 'img')

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
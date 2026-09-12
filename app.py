"""Demo for Serverless Updater
Copyright (c) 2026 Louis Liu  All rights reserved.
"""

import traceback
import tkinter as tk
from tkinter import messagebox

from version import VERSION
import updater


class DemoApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Demo App v{VERSION}")

        self.label = tk.Label(root, text="Serverless Updater Demo")
        self.label.pack()

        self.button = tk.Button(root, text="Check Update", command=self.check_update)
        self.button.pack()

        self.msg = tk.Label(root, text="")
        self.msg.pack()

    def check_update(self):
        self.msg.config(text="Checking for updates...")
        self.root.update()

        try:
            result = updater.check_update(VERSION)
            if result:
                self.msg.config(
                    text=f"Detect new version {result['version']}. Updating..."
                )
                self.root.update()
                updater.download_and_update(result)
                self.msg.config(
                    text="Successfully download and update. Restart to run."
                )
            else:
                self.msg.config(text="It's already the latest version.")
        except Exception as e:
            messagebox.showerror(
                "Fail to update", f"Error occured: \n\n{traceback.format_exc()}"
            )
            self.msg.config(text="Update failed.", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = DemoApp(root)
    root.update_idletasks()
    root.mainloop()

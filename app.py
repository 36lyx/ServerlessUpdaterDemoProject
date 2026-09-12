"""Demo for Serverless Updater
Copyright (c) 2026 Louis Liu  All rights reserved.
"""

import tkinter as tk
import updater
from version import VERSION


def check_update(msg):
    result = updater.check_update(VERSION)
    if result:
        msg.config(text=f"Detect new version {result['version']}.")
        updater.download_and_update(result)
    else:
        msg.config(text="It's already the latest version.")


def main():
    root = tk.Tk()
    root.title("Demo App")

    label = tk.Label(root, text="Serverless Updater Demo")
    msg = tk.Label(root, text="")
    button = tk.Button(root, text="Check Update", command=lambda: check_update(msg))

    label.pack()
    button.pack()
    msg.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

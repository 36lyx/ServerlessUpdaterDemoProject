import tkinter as tk


def check_update(msg):
    msg.config(text="Sorry, update checker is unavailable")


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

"""Demo for Serverless Updater
Copyright (c) 2026 Louis Liu  All rights reserved.
"""

import updater
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from version import VERSION


class DemoApp(App):

    def build(self):
        self.title = "Demo App"

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.label = Label(text="Serverless Updater Demo", size_hint_y=None, height=40)
        self.msg = Label(text="", size_hint_y=None, height=40)

        self.button = Button(
            text="Check Update",
            size_hint_y=None,
            height=50,
            on_press=self.check_update,
        )

        layout.add_widget(self.label)
        layout.add_widget(self.button)
        layout.add_widget(self.msg)

        return layout

    def check_update(self, instance):
        result = updater.check_update(VERSION)
        if result:
            self.msg.text = f"Detect new version {result['version']}. Updating..."
            updater.download_and_update(result)
            self.msg.text = "Successfully download and update. Restart to run."
        else:
            self.msg.text = "It's already the latest version."


if __name__ == "__main__":
    DemoApp().run()

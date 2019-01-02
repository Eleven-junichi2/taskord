from pathlib import Path
import sys
# import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    ObjectProperty, NumericProperty, StringProperty, ReferenceListProperty)
from kivy.resources import resource_add_path, resource_find
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

__file__ = sys.argv[0]
resource_add_path(str(Path(__file__).parent / "resources"))

LabelBase.register(DEFAULT_FONT, "fonts/NotoSansCJKjp-Regular.otf")
LabelBase.register("code_input", "fonts/NotoSansMonoCJKjp-Regular.otf")


class IconBase:
    icon = StringProperty("")
    padding_left = NumericProperty(0)
    padding_top = NumericProperty(0)
    padding_right = NumericProperty(0)
    padding_bottom = NumericProperty(0)
    padding = ReferenceListProperty(
        padding_left, padding_top, padding_right, padding_bottom)


class IconWidget(IconBase, Widget):
    pass


class IconButton(IconBase, Button):
    pass


class IconToggleButton(IconBase, ToggleButton):
    pass


class ClosablePopup(Popup):
    def __init__(self, content, close_function=None, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.content.close = self.dismiss
        self.close_function = close_function

        def close():
            self.dismiss()
            if self.close_function:
                self.close_function()


class MsgPopupLayout(RelativeLayout):
    close = ObjectProperty(None)
    msg_label = ObjectProperty(None)


class MsgPopup(ClosablePopup):
    def __init__(self, msg_text, close_function=None, **kwargs):
        super().__init__(MsgPopupLayout(), **kwargs)
        self.content.msg_label.text = msg_text


# class SaveFilePopupLayout(RelativeLayout):
#     close = ObjectProperty(None)
#     save_file = ObjectProperty(None)


# class SaveFilePopup(ClosablePopup):
#     def __init__(self, save_function, close_function=None, **kwargs):
#         super().__init__(SaveFilePopupLayout(), **kwargs)
#         self.content.save_file = save_function


# class OpenFilePopupLayout(RelativeLayout):
#     close = ObjectProperty(None)
#     open_file = ObjectProperty(None)

#     def on_close_now(self, instance, close_now):
#         if close_now:
#             instance.close()


# class OpenFilePopup(Popup):
#     def __init__(self, open_function, close_function=None, **kwargs):
#         super().__init__(**kwargs)
#         self.content = OpenFilePopupLayout()
#         self.content.open_file = open_function
#         self.close_function = close_function

#         def close():
#             self.dismiss()
#             if self.close_function:
#                 self.close_function()
#         self.content.close = close


LICENSE_SHOWING = """
(C) 2018 Eleven-junichi2:
https://eleven-junichi2.github.io/
Property(None)

    def __init__(se
This app's repository
https://github.com/Eleven-junichi2/Taskord

The copyright of the following libraries and resources belongs to their
respective rights holders:

Kivy:
https://github.com/kivy/kivy/blob/master/LICENSE

Noto:
https://scripts.sil.org/cms/scripts/page.php?site_id=nrsi&id=OFL

Pygments:
https://bitbucket.org/birkenfeld/pygments-main/src/tip/LICENSE

SDL:
https://www.libsdl.org/license.php

GLEW:
http://glew.sourceforge.net/glew.txt
"""


class LicensePopupLayout(RelativeLayout):
    close = ObjectProperty(None)
    license_showing = StringProperty(LICENSE_SHOWING)


class LicensePopup(ClosablePopup):
    def __init__(self, close_function=None, **kwargs):
        super().__init__(LicensePopupLayout(), **kwargs)


class TaskListItemCard(BoxLayout):
    task_description = ObjectProperty(None)
    duration = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def remove_task(self):
        self.parent.remove_widget(self)


class ShowingCurrentTaskPopupLayout(RelativeLayout):
    task_description = ObjectProperty(None)
    duration = ObjectProperty(None)


class ShowingCurrentTaskPopup(Popup):
    def __init__(self, task_description_text, duration, **kwargs):
        super().__init__(**kwargs)
        self.content = ShowingCurrentTaskPopupLayout()
        self.content.task_description.text = task_description_text
        self.content.duration.text = duration
        self.auto_dismiss = False


class MainScreen(Screen):
    task_list = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_task(self):
        self.task_list.add_widget(TaskListItemCard())

    def start_tasks(self):
        sound = SoundLoader.load(resource_find(
            "sounds/se_maoudamashii_jingle11.wav"))
        for child in self.task_list.children:
            error = False
            if not child.duration.text.isnumeric():
                popup = MsgPopup("Error: Please input number in duration.")
                popup.open()
                error = True
            if not child.task_description.text:
                popup = MsgPopup("Error: Please input task description.")
                popup.open()
                error = True
            if error:
                break
            popup = ShowingCurrentTaskPopup(
                child.task_description.text, child.duration.text)
            popup.open()
            Clock.schedule_once(popup.dismiss,
                                int(child.duration.text))
            Clock.schedule_once(lambda dt: sound.play(),
                                int(child.duration.text) - 0.5)

        # print(child.task_description.text, child.duration.text)
# se_maoudamashii_jingle11.mp3


class TaskordScreenManager(ScreenManager):
    pass


class TaskordApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "images/icon.png"
        self.title = "Taskord"

    def build(self):
        root_widget = TaskordScreenManager()
        root_widget.add_widget(MainScreen(name="main"))
        return root_widget

    def show_license(self):
        popup = LicensePopup()
        popup.open()


def main():
    TaskordApp().run()


if __name__ == "__main__":
    main()

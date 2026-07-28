# pet.py

import os
import sys
import json
import random
import math

from PySide6.QtWidgets import QLabel, QMenu
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QTimer, QPoint


from animation import Animation
from speech import Speech
from tray import Tray


def get_base():

    if getattr(sys, "frozen", False):

        return os.path.dirname(
            sys.executable
        )

    return os.path.dirname(
        os.path.abspath(__file__)
    )



BASE = get_base()

ASSETS = os.path.join(
    BASE,
    "assets"
)

CONFIG = os.path.join(
    BASE,
    "config.json"
)


DEFAULT_CONFIG = {
    "scale": 0.075,
    "speed": 3,
    "wander": True,
    "auto_talk": True
}



class Pet(QLabel):


    def __init__(self):

        super().__init__()


        self.setWindowFlags(
            Qt.FramelessWindowHint
            |
            Qt.WindowStaysOnTopHint
            |
            Qt.Tool
        )


        self.setAttribute(
            Qt.WA_TranslucentBackground
        )


        self.load_config()


        self.dragging = False

        self.drag_offset = QPoint()


        self.direction_x = 1

        self.direction_y = 0


        self.float_time = 0


        self.load_image()


        self.animation = Animation(
            self
        )


        self.speech = Speech()


        self.tray = Tray(
            self
        )


        self.move_timer = QTimer()

        self.move_timer.timeout.connect(
            self.update_movement
        )

        self.move_timer.start(
            30
        )


        self.talk_timer = QTimer()

        self.talk_timer.timeout.connect(
            self.random_talk
        )

        self.talk_timer.start(
            30000
        )


        self.start_idle()



    # =================
    # config
    # =================


    def load_config(self):

        if not os.path.exists(CONFIG):

            self.scale = 0.075
            self.speed = 3
            self.wander = True
            self.auto_talk = True

            self.save_config()

            return


        with open(
            CONFIG,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)


        self.scale = data.get(
            "scale",
            0.075
        )

        self.speed = data.get(
            "speed",
            3
        )

        self.wander = data.get(
            "wander",
            True
        )

        self.auto_talk = data.get(
            "auto_talk",
            True
        )



    def save_config(self):

        with open(
            CONFIG,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "scale": self.scale,
                    "speed": self.speed,
                    "wander": self.wander,
                    "auto_talk": self.auto_talk
                },
                f,
                indent=4,
                ensure_ascii=False
            )



    # =================
    # image
    # =================


    def load_image(self):

        path = os.path.join(
            ASSETS,
            "pet.png"
        )


        self.original = QPixmap(
            path
        )


        self.resize_pet()



    def resize_pet(self):

        img = self.original.scaled(
            int(
                self.original.width()
                *
                self.scale
            ),
            int(
                self.original.height()
                *
                self.scale
            ),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.setPixmap(
            img
        )


        self.resize(
            img.size()
        )

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

# pet.py
# continuation


    # =================
    # movement
    # =================


    def update_movement(self):

        if not self.wander:

            return


        screen = self.screen().availableGeometry()


        x = self.x()

        y = self.y()


        width = self.width()

        height = self.height()



        # 提前转向，避免撞墙

        if x < 80:

            self.direction_x = 1


        elif x + width > screen.width() - 80:

            self.direction_x = -1



        if y < 80:

            self.direction_y = 1


        elif y + height > screen.height() - 120:

            self.direction_y = -1



        # 随机改变方向

        if random.random() < 0.01:

            self.direction_x = random.choice(
                [-1, 1]
            )


        if random.random() < 0.02:

            self.direction_y = random.choice(
                [-1, 0, 1]
            )



        x += self.direction_x * self.speed

        y += self.direction_y * self.speed



        self.move(
            x,
            y
        )



    # =================
    # speech
    # =================


    def random_talk(self):

        if self.auto_talk:

            if random.random() < 0.5:

                self.show_speech()



    def show_speech(self):

        self.speech.move(
            self.x(),
            self.y() - 80
        )


        self.speech.show_message()



    # =================
    # animation
    # =================


    def start_idle(self):

        self.animation.play(
            "idle"
        )



    # =================
    # menu
    # =================


    def show_menu(self, event):

        menu = QMenu(
            self
        )


        talk = QAction(
            "让派蒙说话"
        )


        bigger = QAction(
            "放大"
        )


        smaller = QAction(
            "缩小"
        )


        faster = QAction(
            "加速"
        )


        slower = QAction(
            "减速"
        )


        pause = QAction(
            "暂停移动"
        )


        resume = QAction(
            "继续移动"
        )


        quit_action = QAction(
            "退出"
        )


        menu.addAction(
            talk
        )

        menu.addAction(
            bigger
        )

        menu.addAction(
            smaller
        )

        menu.addAction(
            faster
        )

        menu.addAction(
            slower
        )

        menu.addAction(
            pause
        )

        menu.addAction(
            resume
        )

        menu.addAction(
            quit_action
        )


        action = menu.exec(
            event.globalPosition()
            .toPoint()
        )


        if action == talk:

            self.show_speech()


        elif action == bigger:

            self.scale += 0.01

            self.resize_pet()

            self.save_config()


        elif action == smaller:

            self.scale -= 0.01

            if self.scale < 0.02:

                self.scale = 0.02

            self.resize_pet()

            self.save_config()


        elif action == faster:

            self.speed += 1

            self.save_config()


        elif action == slower:

            self.speed = max(
                1,
                self.speed - 1
            )

            self.save_config()


        elif action == pause:

            self.wander = False


        elif action == resume:

            self.wander = True


        elif action == quit_action:

            self.close_app()

# pet.py
# continuation


    # =================
    # mouse
    # =================


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_offset = (
                event.globalPosition()
                .toPoint()
                -
                self.pos()
            )


        elif event.button() == Qt.RightButton:

            self.show_menu(
                event
            )



    def mouseMoveEvent(self, event):

        if self.dragging:

            self.move(
                event.globalPosition()
                .toPoint()
                -
                self.drag_offset
            )



    def mouseReleaseEvent(self, event):

        self.dragging = False



    # =================
    # close
    # =================


    def close_app(self):

        self.speech.close()

        self.close()

        from PySide6.QtWidgets import QApplication

        QApplication.quit()

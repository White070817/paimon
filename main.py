import sys
import os
import json
import random
import math

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu
)

from PySide6.QtGui import (
    QPixmap,
    QAction
)

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPoint
)


from animation import Animation
from speech import Speech
from tray import Tray


if getattr(sys, "frozen", False):
    BASE = os.path.dirname(sys.executable)
else:
    BASE = os.path.dirname(
        os.path.abspath(__file__)
    )


ASSETS = os.path.join(
    BASE,
    "assets"
)


PET_IMAGE = os.path.join(
    ASSETS,
    "pet.png"
)


CONFIG = os.path.join(
    BASE,
    "config.json"
)



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


        self.scale = 0.075
        self.speed = 3


        self.dragging = False
        self.drag_offset = QPoint()


        self.dx = self.speed
        self.dy = 2


        self.float_time = 0
        self.float_strength = 2


        self.load_config()


        self.load_image()


        self.animation = Animation(
            self
        )


        self.speech = Speech()



        self.start_idle()



        self.timer = QTimer()

        self.timer.timeout.connect(
            self.move_pet
        )

        self.timer.timeout.connect(
            self.float_pet
        )

        self.timer.timeout.connect(
            self.update_speech_position
        )

        self.timer.start(30)



        self.talk_timer = QTimer()

        self.talk_timer.timeout.connect(
            self.random_talk
        )

        self.talk_timer.start(
            30000
        )



        self.tray = Tray(
            self
        )



    # =====================
    # config
    # =====================


    def load_config(self):

        if not os.path.exists(CONFIG):

            self.save_config()

            return


        try:

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


        except:

            self.save_config()



    def save_config(self):

        with open(
            CONFIG,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "scale": self.scale,
                    "speed": self.speed
                },
                f,
                indent=4,
                ensure_ascii=False
            )



    # =====================
    # image
    # =====================


    def load_image(self):

        if not os.path.exists(PET_IMAGE):

            self.setText(
                "Missing assets/pet.png"
            )

            return


        self.pixmap_original = QPixmap(
            PET_IMAGE
        )


        self.resize_pet()

    def resize_pet(self):

        pix = self.pixmap_original.scaled(
            int(
                self.pixmap_original.width()
                * self.scale
            ),
            int(
                self.pixmap_original.height()
                * self.scale
            ),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.setPixmap(
            pix
        )

        self.resize(
            pix.size()
        )



    # =====================
    # animation
    # =====================


    def start_idle(self):

        folder = os.path.join(
            ASSETS,
            "animations",
            "idle"
        )

        self.animation.load_frames(
            folder
        )

        self.animation.start(
            5
        )



    def play_animation(self, name):

        folder = os.path.join(
            ASSETS,
            "animations",
            name
        )

        self.animation.load_frames(
            folder
        )

        self.animation.start(
            8
        )



    # =====================
    # speech
    # =====================


    def show_speech(self):

        self.speech.move(
            self.x(),
            self.y()-80
        )

        self.speech.speak()



    def random_talk(self):

        if random.random() < 0.5:

            self.show_speech()



    def update_speech_position(self):

        try:

            if self.speech.isVisible():

                self.speech.move(
                    self.x(),
                    self.y()-80
                )

        except:

            pass



    # =====================
    # movement
    # =====================


    def move_pet(self):

        screen = QApplication.primaryScreen().availableGeometry()


        x = self.x() + self.dx
        y = self.y() + self.dy


        if x <= 0 or x+self.width() >= screen.width():

            self.dx *= -1



        if y <= 0 or y+self.height() >= screen.height():

            self.dy *= -1



        self.move(
            x,
            y
        )



    def float_pet(self):

        self.float_time += 0.08


        offset = int(
            math.sin(
                self.float_time
            )
            *
            self.float_strength
        )


        self.move(
            self.x(),
            self.y()+offset
        )



    # =====================
    # menu
    # =====================


    def show_menu(self, event):

        menu = QMenu()


        talk = QAction(
            "让派蒙说话",
            self
        )


        bigger = QAction(
            "放大",
            self
        )


        smaller = QAction(
            "缩小",
            self
        )


        faster = QAction(
            "加速",
            self
        )


        slower = QAction(
            "减速",
            self
        )


        pause = QAction(
            "暂停移动",
            self
        )


        resume = QAction(
            "继续移动",
            self
        )


        quit_action = QAction(
            "退出",
            self
        )


        menu.addAction(talk)

        menu.addSeparator()

        menu.addAction(bigger)

        menu.addAction(smaller)

        menu.addSeparator()

        menu.addAction(faster)

        menu.addAction(slower)

        menu.addSeparator()

        menu.addAction(pause)

        menu.addAction(resume)

        menu.addSeparator()

        menu.addAction(quit_action)



        action = menu.exec(
            event.globalPosition().toPoint()
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

            self.dx = self.speed

            self.save_config()


        elif action == slower:

            self.speed -= 1

            if self.speed < 1:

                self.speed = 1

            self.dx = self.speed

            self.save_config()

        elif action == pause:

            self.timer.stop()


        elif action == resume:

            self.timer.start(30)


        elif action == quit_action:

            QApplication.quit()



    # =====================
    # mouse
    # =====================


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




# =====================
# start
# =====================


if __name__ == "__main__":


    app = QApplication(
        sys.argv
    )


    pet = Pet()


    pet.show()


    sys.exit(
        app.exec()
    )

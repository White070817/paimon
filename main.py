import sys
import os
import json
import random

from PySide6.QtWidgets import QApplication, QLabel, QMenu
from animation import Animation
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QTimer, QPoint


BASE = os.path.dirname(
    sys.executable if getattr(sys, "frozen", False)
    else __file__
)


ASSET = os.path.join(
    BASE,
    "assets",
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
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )


        self.setAttribute(
            Qt.WA_TranslucentBackground
        )


        self.scale = 1.0


        self.load_config()


        self.load_image()

        self.animation = Animation(self)

        self.start_idle()

        self.animation = Animation(self)


        self.dx = self.speed
        self.dy = 2


        self.drag = False
        self.offset = QPoint()


        self.timer = QTimer()
        self.timer.timeout.connect(
            self.move_pet
        )

        self.timer.start(30)

        self.start_idle()



    def load_config(self):

        self.speed = 3

        if os.path.exists(CONFIG):

            with open(CONFIG,"r",
                      encoding="utf8") as f:

                data=json.load(f)

                self.scale=data.get(
                    "scale",
                    1.0
                )

                self.speed=data.get(
                    "speed",
                    3
                )



    def save_config(self):

        with open(CONFIG,"w",
                  encoding="utf8") as f:

            json.dump(
                {
                    "scale":self.scale,
                    "speed":self.speed
                },
                f,
                indent=4
            )



    def load_image(self):

        if not os.path.exists(ASSET):

            self.setText(
                "缺少 assets/pet.png"
            )

            return


        pix=QPixmap(ASSET)


        pix=pix.scaled(
            int(pix.width()*self.scale),
            int(pix.height()*self.scale),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.setPixmap(pix)

        self.resize(
            pix.size()
        )

    def start_idle(self):

    folder = os.path.join(
        BASE,
        "assets",
        "animations",
        "idle"
    )

    self.animation.load_frames(folder)

    self.animation.start(5)


    def move_pet(self):

        if self.drag:
            return


        screen=QApplication.primaryScreen().availableGeometry()


        x=self.x()+self.dx
        y=self.y()+self.dy


        if x<0 or x+self.width()>screen.width():

            self.dx*=-1


        if y<0 or y+self.height()>screen.height():

            self.dy*=-1


        self.move(
            self.x()+self.dx,
            self.y()+self.dy
        )



    def mousePressEvent(self,e):

        if e.button()==Qt.LeftButton:

            self.drag=True

            self.offset=(
                e.globalPosition().toPoint()
                -
                self.pos()
            )


        elif e.button()==Qt.RightButton:

            self.menu(e)



    def mouseMoveEvent(self,e):

        if self.drag:

            self.move(
                e.globalPosition().toPoint()
                -
                self.offset
            )



    def mouseReleaseEvent(self,e):

        self.drag=False



    def menu(self,e):

        menu=QMenu()


        big=QAction("放大",self)
        small=QAction("缩小",self)

        stop=QAction("停止",self)
        start=QAction("移动",self)

        quit=QAction("退出",self)


        menu.addAction(big)
        menu.addAction(small)

        menu.addSeparator()

        menu.addAction(stop)
        menu.addAction(start)

        menu.addSeparator()

        menu.addAction(quit)


        a=menu.exec(
            e.globalPosition().toPoint()
        )


        if a==big:

            self.scale+=0.1
            self.save_config()
            self.load_image()


        elif a==small:

            self.scale=max(
                0.3,
                self.scale-0.1
            )

            self.save_config()
            self.load_image()


        elif a==stop:

            self.timer.stop()


        elif a==start:

            self.timer.start(30)


        elif a==quit:

            QApplication.quit()



app=QApplication(sys.argv)

pet=Pet()

pet.show()

sys.exit(app.exec())

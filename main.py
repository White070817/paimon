import sys
import os
import json

from PySide6.QtWidgets import QApplication, QLabel, QMenu
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QTimer, QPoint

from animation import Animation


BASE = os.path.dirname(
    sys.executable if getattr(sys, "frozen", False)
    else __file__
)


PET_IMAGE = os.path.join(
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


        self.scale = 0.075
        self.speed = 3


        self.load_config()


        self.drag = False
        self.offset = QPoint()


        self.load_image()


        # 动画系统
        self.animation = Animation(self)

        self.start_idle()


        # 移动
        self.dx = self.speed
        self.dy = 2


        self.timer = QTimer()

        self.timer.timeout.connect(
            self.move_pet
        )

        self.timer.start(30)



    def load_config(self):

        if os.path.exists(CONFIG):

            try:

                with open(
                    CONFIG,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data=json.load(f)

                    self.scale=data.get(
                        "scale",
                        0.075
                    )

                    self.speed=data.get(
                        "speed",
                        3
                    )

            except:

                pass



    def save_config(self):

        with open(
            CONFIG,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "scale":self.scale,
                    "speed":self.speed
                },
                f,
                indent=4
            )



    def load_image(self):

        if not os.path.exists(PET_IMAGE):

            self.setText(
                "缺少 assets/pet.png"
            )

            return


        pix=QPixmap(
            PET_IMAGE
        )


        pix=pix.scaled(
            int(pix.width()*self.scale),
            int(pix.height()*self.scale),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.setPixmap(
            pix
        )


        self.resize(
            pix.size()
        )



    def start_idle(self):

        folder=os.path.join(
            BASE,
            "assets",
            "animations",
            "idle"
        )


        self.animation.load_frames(
            folder
        )


        self.animation.start(
            5
        )



    def move_pet(self):

        screen=QApplication.primaryScreen().availableGeometry()


        x=self.x()+self.dx
        y=self.y()+self.dy


        if x<=0 or x+self.width()>=screen.width():

            self.dx*=-1


        if y<=0 or y+self.height()>=screen.height():

            self.dy*=-1


        self.move(
            self.x()+self.dx,
            self.y()+self.dy
        )



    def mousePressEvent(self,event):

        if event.button()==Qt.LeftButton:

            self.drag=True

            self.offset=(
                event.globalPosition().toPoint()
                -
                self.pos()
            )


        elif event.button()==Qt.RightButton:

            self.show_menu(event)



    def mouseMoveEvent(self,event):

        if self.drag:

            self.move(
                event.globalPosition().toPoint()
                -
                self.offset
            )



    def mouseReleaseEvent(self,event):

        self.drag=False



    def show_menu(self,event):

        menu=QMenu()


        big=QAction(
            "放大",
            self
        )

        small=QAction(
            "缩小",
            self
        )

        stop=QAction(
            "停止移动",
            self
        )

        start=QAction(
            "开始移动",
            self
        )

        quit_action=QAction(
            "退出",
            self
        )


        menu.addAction(big)
        menu.addAction(small)

        menu.addSeparator()

        menu.addAction(stop)
        menu.addAction(start)

        menu.addSeparator()

        menu.addAction(quit_action)


        action=menu.exec(
            event.globalPosition().toPoint()
        )


        if action==big:

            self.scale+=0.01

            self.save_config()

            self.load_image()



        elif action==small:

            self.scale=max(
                0.02,
                self.scale-0.01
            )

            self.save_config()

            self.load_image()



        elif action==stop:

            self.timer.stop()



        elif action==start:

            self.timer.start(30)



        elif action==quit_action:

            QApplication.quit()



if __name__=="__main__":

    app=QApplication(sys.argv)

    pet=Pet()

    pet.show()

    sys.exit(
        app.exec()
    )

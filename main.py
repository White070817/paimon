import sys
import os
import json
import random
import math

from PySide6.QtWidgets import QApplication, QLabel, QMenu
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QTimer, QPoint

from animation import Animation
from speech import Speech
from tray import Tray


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


        # 默认参数

        self.scale = 0.075
        self.speed = 3

        self.wander = True
        self.auto_talk = True

        self.talk_interval = 30

        self.float_strength = 2

        self.random_move = True



        self.load_config()



        self.drag = False
        self.offset = QPoint()


        self.float_time = 0


        self.wait_time = 0


        self.load_image()



        # 动画

        self.animation = Animation(
            self
        )

        self.start_idle()



        # 气泡

        self.speech = Speech()



        # 移动方向

        self.dx = self.speed
        self.dy = 2



        # 移动计时器

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



        # 自动眨眼

        self.blink_timer = QTimer()

        self.blink_timer.timeout.connect(
            self.random_blink
        )

        self.blink_timer.start(
            10000
        )



        # 自动说话

        self.talk_timer = QTimer()

        self.talk_timer.timeout.connect(
            self.random_talk
        )

        self.talk_timer.start(
            self.talk_interval * 1000
        )



        # 托盘

        self.tray = Tray(
            self
        )

    # ======================
    # 配置
    # ======================

    def load_config(self):

        if not os.path.exists(CONFIG):
            return


        try:

            with open(
                CONFIG,
                "r",
                encoding="utf-8"
            ) as f:

                data=json.load(f)


            self.scale=data.get(
                "scale",
                self.scale
            )

            self.speed=data.get(
                "speed",
                self.speed
            )

            self.wander=data.get(
                "wander",
                True
            )

            self.auto_talk=data.get(
                "auto_talk",
                True
            )

            self.talk_interval=data.get(
                "talk_interval",
                30
            )

            self.float_strength=data.get(
                "float_strength",
                2
            )

            self.random_move=data.get(
                "random_move",
                True
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
                    "speed":self.speed,
                    "wander":self.wander,
                    "auto_talk":self.auto_talk,
                    "talk_interval":self.talk_interval,
                    "float_strength":self.float_strength,
                    "random_move":self.random_move
                },
                f,
                indent=4,
                ensure_ascii=False
            )



    # ======================
    # 图片
    # ======================

    def load_image(self):

        if not os.path.exists(PET_IMAGE):

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



    # ======================
    # 动画
    # ======================

    def play_animation(
        self,
        name,
        fps=5
    ):

        folder=os.path.join(
            BASE,
            "assets",
            "animations",
            name
        )


        self.animation.play(
            folder,
            fps
        )



    def start_idle(self):

        self.play_animation(
            "idle",
            5
        )



    def random_blink(self):

        if random.random()<0.4:

            self.play_animation(
                "blink",
                8
            )


            QTimer.singleShot(
                1500,
                self.start_idle
            )



    def happy(self):

        self.play_animation(
            "happy",
            8
        )


        QTimer.singleShot(
            2000,
            self.start_idle
        )



    # ======================
    # 说话
    # ======================

    def show_speech(self):

        self.speech.move(
            self.x(),
            self.y()-80
        )

        self.speech.speak()



    def random_talk(self):

        if self.auto_talk:

            if random.random()<0.5:

                self.show_speech()



    # ======================
    # 智能移动
    # ======================

    def change_direction(self):

        if not self.random_move:
            return


        if random.random()<0.05:

            self.dx=random.choice(
                [-self.speed, self.speed]
            )


        if random.random()<0.05:

            self.dy=random.choice(
                [-2,2]
            )



    def move_pet(self):

        if not self.wander:
            return


        screen=QApplication.primaryScreen().availableGeometry()


        x=self.x()+self.dx
        y=self.y()+self.dy


        if x<=0 or x+self.width()>=screen.width():

            self.dx*=-1



        if y<=0 or y+self.height()>=screen.height():

            self.dy*=-1



        self.change_direction()



        self.move(
            self.x()+self.dx,
            self.y()+self.dy
        )



    def float_pet(self):

        self.float_time+=0.08


        offset=int(
            math.sin(self.float_time)
            *
            self.float_strength
        )


        self.move(
            self.x(),
            self.y()+offset
        )

    # ======================
    # 鼠标互动
    # ======================

    def mousePressEvent(self,event):

        if event.button()==Qt.LeftButton:

            self.happy()

            self.show_speech()


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



    # ======================
    # 托盘控制
    # ======================

    def pause_move(self):

        self.timer.stop()



    def resume_move(self):

        self.timer.start(30)



    def close_app(self):

        QApplication.quit()



    # ======================
    # 右键菜单
    # ======================

    def show_menu(self,event):

        menu=QMenu()


        talk=QAction(
            "让派蒙说话",
            self
        )


        pause=QAction(
            "暂停移动",
            self
        )


        resume=QAction(
            "继续移动",
            self
        )


        quit_action=QAction(
            "退出",
            self
        )


        menu.addAction(
            talk
        )

        menu.addSeparator()

        menu.addAction(
            pause
        )

        menu.addAction(
            resume
        )

        menu.addSeparator()

        menu.addAction(
            quit_action
        )


        action=menu.exec(
            event.globalPosition().toPoint()
        )


        if action==talk:

            self.show_speech()



        elif action==pause:

            self.pause_move()



        elif action==resume:

            self.resume_move()



        elif action==quit_action:

            self.close_app()



if __name__=="__main__":


    app=QApplication(
        sys.argv
    )


    pet=Pet()


    pet.show()


    sys.exit(
        app.exec()
    )

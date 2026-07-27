import sys
import os
import random
from PySide6.QtWidgets import QApplication, QLabel, QMenu
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QTimer, QPoint


def resource_path(name):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, name)
    return os.path.join(os.path.dirname(__file__), name)


class Pet(QLabel):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.size_scale = 1.0

        self.load_image()

        self.dx = 3
        self.dy = 2

        self.dragging = False
        self.offset = QPoint()

        self.timer = QTimer()
        self.timer.timeout.connect(self.move_pet)
        self.timer.start(30)


    def load_image(self):

        path = resource_path("pet.png")

        pix = QPixmap(path)

        if pix.isNull():
            self.setText("pet.png missing")
            return


        # 自动缩放
        pix = pix.scaled(
            int(pix.width()*self.size_scale),
            int(pix.height()*self.size_scale),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.setPixmap(pix)
        self.resize(pix.size())


    def move_pet(self):

        if self.dragging:
            return

        screen = QApplication.primaryScreen().availableGeometry()

        x = self.x()+self.dx
        y = self.y()+self.dy


        if x < 0 or x+self.width()>screen.width():
            self.dx *= -1

        if y < 0 or y+self.height()>screen.height():
            self.dy *= -1


        self.move(
            self.x()+self.dx,
            self.y()+self.dy
        )


    def mousePressEvent(self,event):

        if event.button()==Qt.LeftButton:

            self.dragging=True

            self.offset=(
                event.globalPosition().toPoint()
                -
                self.pos()
            )


        elif event.button()==Qt.RightButton:

            self.menu(event)


    def mouseMoveEvent(self,event):

        if self.dragging:

            self.move(
                event.globalPosition().toPoint()
                -
                self.offset
            )


    def mouseReleaseEvent(self,event):

        self.dragging=False



    def menu(self,event):

        menu=QMenu()


        bigger=QAction("放大",self)
        smaller=QAction("缩小",self)

        stop=QAction("停止移动",self)
        start=QAction("继续移动",self)

        quit=QAction("退出",self)


        menu.addAction(bigger)
        menu.addAction(smaller)

        menu.addSeparator()

        menu.addAction(stop)
        menu.addAction(start)

        menu.addSeparator()

        menu.addAction(quit)


        action=menu.exec(
            event.globalPosition().toPoint()
        )


        if action==bigger:

            self.size_scale=min(
                self.size_scale+0.1,
                2
            )

            self.load_image()



        elif action==smaller:

            self.size_scale=max(
                self.size_scale-0.1,
                0.3
            )

            self.load_image()



        elif action==stop:

            self.timer.stop()



        elif action==start:

            self.timer.start(30)



        elif action==quit:

            QApplication.quit()



if __name__=="__main__":

    app=QApplication(sys.argv)

    pet=Pet()

    pet.show()

    sys.exit(app.exec())

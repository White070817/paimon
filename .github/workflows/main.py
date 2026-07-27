import sys
import random

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
)


class DesktopPet(QLabel):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.pix = QPixmap("pet.png")

        if self.pix.isNull():
            self.setText("请上传 pet.png 到仓库")
            self.adjustSize()
        else:
            self.setPixmap(self.pix)
            self.resize(self.pix.size())

        screen = QApplication.primaryScreen().availableGeometry()

        self.move(
            random.randint(0, max(0, screen.width() - self.width())),
            random.randint(0, max(0, screen.height() - self.height())),
        )

        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])

        self.drag = False
        self.offset = QPoint()

        self.timer = QTimer()
        self.timer.timeout.connect(self.walk)
        self.timer.start(30)

    def walk(self):
        if self.drag:
            return

        screen = QApplication.primaryScreen().availableGeometry()

        x = self.x() + self.dx
        y = self.y() + self.dy

        if x <= 0 or x >= screen.width() - self.width():
            self.dx *= -1

        if y <= 0 or y >= screen.height() - self.height():
            self.dy *= -1

        self.move(self.x() + self.dx, self.y() + self.dy)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drag = True
            self.offset = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

        elif e.button() == Qt.RightButton:
            menu = QMenu()

            stop = QAction("停止", self)
            start = QAction("继续", self)
            quit = QAction("退出", self)

            menu.addAction(stop)
            menu.addAction(start)
            menu.addSeparator()
            menu.addAction(quit)

            action = menu.exec(e.globalPosition().toPoint())

            if action == stop:
                self.timer.stop()

            elif action == start:
                self.timer.start(30)

            elif action == quit:
                QApplication.quit()

    def mouseMoveEvent(self, e):
        if self.drag:
            self.move(e.globalPosition().toPoint() - self.offset)

    def mouseReleaseEvent(self, e):
        self.drag = False


if __name__ == "__main__":
    app = QApplication(sys.argv)

    pet = DesktopPet()
    pet.show()

    sys.exit(app.exec())

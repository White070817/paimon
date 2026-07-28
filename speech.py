# speech.py

from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QTimer


class Speech(QLabel):

    def __init__(self):

        super().__init__()


        self.setWindowFlags(
            Qt.FramelessWindowHint
            |
            Qt.Tool
            |
            Qt.WindowStaysOnTopHint
        )


        self.setAttribute(
            Qt.WA_TranslucentBackground
        )


        self.setStyleSheet(
            """
            QLabel {
                background-color: rgba(0,0,0,160);
                color:white;
                border-radius:10px;
                padding:10px;
                font-size:16px;
            }
            """
        )


        self.hide()


        self.texts = [
            "旅行者！派蒙来啦！",
            "今天也要加油哦！",
            "派蒙肚子饿了……",
            "不要忘记休息！",
            "嘿！看看派蒙！"
        ]



    def show_message(self):

        import random


        self.setText(
            random.choice(
                self.texts
            )
        )


        self.adjustSize()


        self.show()


        QTimer.singleShot(
            3000,
            self.hide
        )

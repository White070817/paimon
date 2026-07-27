from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import random


class Speech(QLabel):

    texts = [
        "派蒙才不是应急食品！",
        "旅行者，今天也要加油！",
        "派蒙饿了……",
        "不要一直盯着派蒙看啦！",
        "嘿嘿，派蒙来了！",
        "今天也要努力哦！"
    ]


    def __init__(self):

        super().__init__()


        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )


        self.setStyleSheet(
            """
            background:white;
            border-radius:10px;
            padding:8px;
            color:black;
            """
        )


        self.setFont(
            QFont(
                "Microsoft YaHei",
                12
            )
        )


        self.hide()



    def show_text(self):

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

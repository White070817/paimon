# animation.py

import os

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap


class Animation:

    def __init__(self, pet):

        self.pet = pet

        self.frames = []

        self.index = 0

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.next_frame
        )


    def play(self, name):

        folder = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "assets",
            "animations",
            name
        )


        self.frames.clear()

        if not os.path.exists(folder):

            return


        files = sorted(
            os.listdir(folder)
        )


        for file in files:

            if file.lower().endswith(
                (".png", ".jpg", ".jpeg")
            ):

                self.frames.append(
                    os.path.join(
                        folder,
                        file
                    )
                )


        if len(self.frames) == 0:

            return


        self.index = 0

        self.timer.start(
            200
        )


    def next_frame(self):

        if len(self.frames) == 0:

            return


        pix = QPixmap(
            self.frames[self.index]
        )


        pix = pix.scaled(
            self.pet.size(),
            aspectMode=1
        )


        self.pet.setPixmap(
            pix
        )


        self.index += 1


        if self.index >= len(self.frames):

            self.index = 0

import os
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap


class Animation:

    def __init__(self, label):

        self.label = label

        self.frames = []
        self.index = 0

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.next_frame
        )


    def load_frames(self, folder):

        self.frames.clear()

        if not os.path.exists(folder):
            return


        files = sorted(
            [
                f for f in os.listdir(folder)
                if f.endswith(".png")
            ]
        )


        for f in files:

            self.frames.append(
                QPixmap(
                    os.path.join(folder,f)
                )
            )


    def start(self, fps=5):

        if len(self.frames)==0:
            return


        self.index=0

        self.timer.start(
            int(1000/fps)
        )


    def stop(self):

        self.timer.stop()



    def next_frame(self):

        if len(self.frames)==0:
            return


        self.label.setPixmap(
            self.frames[self.index]
        )


        self.index+=1


        if self.index>=len(self.frames):

            self.index=0

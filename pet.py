# pet.py

import random
import math

from PySide6.QtCore import QTimer


class PetMovement:

    def __init__(self, pet):

        self.pet = pet

        self.speed = 3

        self.direction_x = 1
        self.direction_y = 0

        self.float_time = 0

        self.target_change = 0


        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update
        )


    def start(self):

        self.timer.start(30)



    def update(self):

        screen = self.pet.screen().availableGeometry()


        x = self.pet.x()
        y = self.pet.y()


        width = self.pet.width()
        height = self.pet.height()



        # 提前转向，不撞墙

        if x < 80:

            self.direction_x = 1


        elif x + width > screen.width() - 80:

            self.direction_x = -1



        if y < 80:

            self.direction_y = 1


        elif y + height > screen.height() - 120:

            self.direction_y = -1



        # 随机改变方向

        self.target_change += 1


        if self.target_change > 150:

            self.target_change = 0


            if random.random() < 0.5:

                self.direction_x = random.choice(
                    [-1, 1]
                )


            if random.random() < 0.3:

                self.direction_y = random.choice(
                    [-1, 0, 1]
                )



        x += self.direction_x * self.speed

        y += self.direction_y * self.speed



        self.pet.move(
            x,
            y
        )



        # 漂浮效果

        self.float_time += 0.08


        offset = math.sin(
            self.float_time
        ) * 1.5


        self.pet.move(
            x,
            int(y + offset)
        )

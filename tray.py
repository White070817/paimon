from PySide6.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QApplication
)

from PySide6.QtGui import (
    QAction,
    QIcon
)

import os
import sys



class Tray:

    def __init__(self, pet):

        self.pet = pet


        self.tray = QSystemTrayIcon()


        # 获取资源路径
        if getattr(sys, "frozen", False):

            base = os.path.dirname(
                sys.executable
            )

        else:

            base = os.path.dirname(
                os.path.abspath(__file__)
            )


        icon_path = os.path.join(
            base,
            "assets",
            "pet.png"
        )


        # 设置托盘图标
        if os.path.exists(icon_path):

            self.tray.setIcon(
                QIcon(icon_path)
            )


        self.tray.setToolTip(
            "Paimon Desktop Pet"
        )


        self.create_menu()


        self.tray.show()



    def create_menu(self):

        menu = QMenu()


        show = QAction(
            "显示派蒙"
        )


        hide = QAction(
            "隐藏派蒙"
        )


        quit_action = QAction(
            "退出"
        )


        show.triggered.connect(
            self.show_pet
        )


        hide.triggered.connect(
            self.hide_pet
        )


        quit_action.triggered.connect(
            self.close_app
        )


        menu.addAction(show)

        menu.addAction(hide)

        menu.addSeparator()

        menu.addAction(quit_action)


        self.tray.setContextMenu(
            menu
        )



    def show_pet(self):

        self.pet.show()



    def hide_pet(self):

        self.pet.hide()



    def close_app(self):

        QApplication.quit()

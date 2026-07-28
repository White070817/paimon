# tray.py

from PySide6.QtWidgets import (
    QSystemTrayIcon,
    QMenu
)

from PySide6.QtGui import (
    QAction,
    QIcon
)


class Tray:

    def __init__(self, pet):

        self.pet = pet


        self.tray = QSystemTrayIcon()


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
            self.pet.close_app
        )


        menu.addAction(
            show
        )

        menu.addAction(
            hide
        )

        menu.addSeparator()

        menu.addAction(
            quit_action
        )


        self.tray.setContextMenu(
            menu
        )



    def show_pet(self):

        self.pet.show()



    def hide_pet(self):

        self.pet.hide()

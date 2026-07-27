from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction


class Tray:

    def __init__(self, pet):

        self.pet = pet


        self.tray = QSystemTrayIcon()


        # 没有图标时使用空图标
        self.tray.setIcon(
            QIcon()
        )


        menu = QMenu()


        show_action = QAction(
            "显示派蒙",
            self.tray
        )


        hide_action = QAction(
            "隐藏派蒙",
            self.tray
        )


        talk_action = QAction(
            "让派蒙说话",
            self.tray
        )


        pause_action = QAction(
            "暂停移动",
            self.tray
        )


        resume_action = QAction(
            "继续移动",
            self.tray
        )


        quit_action = QAction(
            "退出",
            self.tray
        )


        menu.addAction(
            show_action
        )

        menu.addAction(
            hide_action
        )

        menu.addSeparator()

        menu.addAction(
            talk_action
        )

        menu.addSeparator()

        menu.addAction(
            pause_action
        )

        menu.addAction(
            resume_action
        )

        menu.addSeparator()

        menu.addAction(
            quit_action
        )


        self.tray.setContextMenu(
            menu
        )


        show_action.triggered.connect(
            self.pet.show
        )


        hide_action.triggered.connect(
            self.pet.hide
        )


        talk_action.triggered.connect(
            self.pet.show_speech
        )


        pause_action.triggered.connect(
            self.pet.pause_move
        )


        resume_action.triggered.connect(
            self.pet.resume_move
        )


        quit_action.triggered.connect(
            self.pet.close_app
        )


        self.tray.show()

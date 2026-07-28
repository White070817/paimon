# main.py

import sys

from PySide6.QtWidgets import QApplication

from pet import Pet


def main():

    app = QApplication(sys.argv)

    app.setQuitOnLastWindowClosed(False)

    pet = Pet()

    pet.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()

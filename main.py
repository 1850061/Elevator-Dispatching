import sys

from PyQt5.QtWidgets import  QApplication

from ElevatorInterface import ElevatorInterface


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ElevatorInterface()
    sys.exit(app.exec_())
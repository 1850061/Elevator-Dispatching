from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtWidgets

from Elevator import Elevator


class Elevator_Manage:

    def __init__(self, Elev):
        self.elev = Elev
        self.elevList = []
        self.outElevList = []
        self.freezeList = [0] * 5
        self.freezeNum = 0
        for i in range(21):
            self.outElevList.append([0, 0])
        for i in range(5):
            self.elevList.append(Elevator(Elev, i + 1))
            self.elevList[i].start()

    def addElev(self, elev, flr):
        self.elevList[elev - 1].addElev(flr)

    def delOutElev(self, flr, status):
        self.outElevList[flr][1 if status == 1 else 0] = 0

    def alarm(self, elev):
        self.elevList[elev - 1].alarm()
        self.freezeList[elev - 1] = 1
        self.freezeNum += 1
        self.distributionOutElev(elev)
        if self.freezeNum == 5:
            QtWidgets.QMessageBox.information(self.elev, "警告", "所有电梯已损坏!")

    def distributionOutElev(self, elev):
        outList = self.elevList[elev - 1].getOutElevQueue()
        for i in range(1, 21):
            if outList[i] != 0:
                self.elevDistribution(i, outList[i], True)

    def elevDistribution(self, flr, status, isAlarm=False):
        if self.outElevList[flr][1 if status == 1 else 0] == 1 and isAlarm == False:
            return
        self.outElevList[flr][1 if status == 1 else 0] = 1
        minElev = 0
        minDis = 1000000
        for i in range(5):
            if self.elevList[i].getOutElevQueue()[flr] != 0 or self.freezeList[i] == 1:
                continue
            score = self.elevList[i].calDist(flr, status) + self.elevList[i].getTaskNum() * 2
            if score < minDis:
                minElev = i
                minDis = score
        if minDis < 1000000:
            self.elevList[minElev].addElev(flr)
            self.elevList[minElev].addOutElev(flr, status)
        elif status == -1:
            self.elev.findChild(QPushButton, "down{0}".format(flr)).setStyleSheet(
                "QPushButton{}")
        elif status == 1:
            self.elev.findChild(QPushButton, "up{0}".format(flr)).setStyleSheet(
                "QPushButton{}")

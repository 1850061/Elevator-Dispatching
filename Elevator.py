import time

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QPushButton


class Elevator(QThread):
    # 这是模拟20层楼全被点亮的情况
    allLight = (1 << 21) - 1

    def __init__(self, Elev, name):
        super(Elevator, self).__init__()
        self.elev = Elev
        self.name = name
        # 当前楼层
        self.nowFloor = 1
        # 当前状态，0为不运行，1为向上运动，-1为向下运动
        self.status = 0
        # 当前任务数量
        self.taskNum = 0
        # 总电梯队列，包括走廊中分配的以及电梯内按下的
        self.elevQueue = 0
        # 记录走廊中分配的电梯
        self.outElevQueue = [0] * 21
        # 记录电梯经过楼层时是否要无视这层楼。例如，当楼梯向上前行经过某层楼，但是当前楼层的人想要向下
        self.isIgnore = [0] * 21

    def getOutElevQueue(self):
        return self.outElevQueue

    def getTaskNum(self):
        return self.taskNum

    def alarm(self):
        self.elevQueue = 0
        self.status = 0
        self.taskNum = 0

    def calDist(self, flr, status):
        if self.status == 0 or self.elevQueue == 0:
            self.status = 0
            return abs(flr - self.nowFloor)
        if self.status == 1:
            if status == 1:
                if flr >= self.nowFloor:
                    return flr - self.nowFloor
                else:
                    # 电梯上到最高的地方再下来
                    return 2 * (self.getHighestElev() - self.nowFloor) + (self.nowFloor - flr)
            elif status == -1:
                if flr >= self.nowFloor:
                    return self.getHighestElev() - self.nowFloor + abs(self.getHighestElev() - flr)
                else:
                    # 电梯上到最高的地方再下来
                    return 2 * (self.getHighestElev() - self.nowFloor) + (self.nowFloor - flr)
        elif self.status == -1:
            if status == -1:
                if flr <= self.nowFloor:
                    return abs(self.nowFloor - flr)
                else:
                    # 电梯下到最低的地方再上来
                    return 2 * abs(self.getLowestElev() - self.nowFloor) + abs(self.nowFloor - flr)
            elif status == 1:
                if flr <= self.nowFloor:
                    return abs(self.getLowestElev() - self.nowFloor) + abs(self.getLowestElev() - flr)
                else:
                    # 电梯下到最低的地方再上来
                    return 2 * abs(self.getLowestElev() - self.nowFloor) + abs(self.nowFloor - flr)
        return 0

    def addElev(self, flr):
        self.taskNum = self.taskNum + 1
        if (1 << flr & self.elevQueue) == 0:
            self.elevQueue = self.elevQueue + (1 << flr)

    def addOutElev(self, flr, status):
        if self.outElevQueue[flr] == 0:
            self.outElevQueue[flr] = status
            if self.status == 1:
                if self.nowFloor < flr < self.getHighestElev() and status == -1:
                    self.isIgnore[flr] = 1
            elif self.status == -1:
                if self.getLowestElev() < flr < self.nowFloor and status == 1:
                    self.isIgnore[flr] = -1

    def delElev(self):
        self.taskNum = self.taskNum - 1
        self.elevQueue = self.elevQueue ^ (1 << self.nowFloor)
        self.elev.findChild(QPushButton, "{0}+{1}".format(self.name, self.nowFloor)).setStyleSheet(
            "QPushButton{}")
        if (self.outElevQueue[self.nowFloor]) == 1:
            self.outElevQueue[self.nowFloor] = 0
            self.elev.findChild(QPushButton, "up{0}".format(self.nowFloor)).setStyleSheet(
                "QPushButton{}")
            self.elev.delOutElev(self.nowFloor, 1)
        if (self.outElevQueue[self.nowFloor]) == -1:
            self.outElevQueue[self.nowFloor] = 0
            self.elev.findChild(QPushButton, "down{0}".format(self.nowFloor)).setStyleSheet(
                "QPushButton{}")
            self.elev.delOutElev(self.nowFloor, -1)

    # 获取电梯队列中最高的那个
    def getHighestElev(self):
        for i in range(1, 21):
            if (self.elevQueue & (1 << (21 - i))) != 0:
                return 21 - i
        return 20

    # 获取电梯队列中最低的那个
    def getLowestElev(self):
        for i in range(1, 21):
            if (self.elevQueue & (1 << i)) != 0:
                return i
        return 1

    # nowFloor以上是否有电梯
    def hasFloorUp(self):
        # nowFloor以下的全为1，以上的全为0
        down = (1 << self.nowFloor) - 1
        # nowFloor及以上的全为1，nowFloor以下的全为0
        up = down ^ Elevator.allLight
        if self.elevQueue & up == 0:
            return False
        else:
            return True

    # nowFloor以下是否有电梯
    def hasFloorDown(self):
        # nowFloor 以上的楼层全为0，nowFloor及以下的全为1
        down = (1 << (self.nowFloor + 1)) - 1
        if self.elevQueue & down == 0:
            return False
        else:
            return True

    # 电梯向上运行
    def turnUp(self):
        self.nowFloor = self.nowFloor + 1
        self.elev.setFloorNumber(self.name, self.nowFloor)

    # 电梯向下运行
    def turnDown(self):
        self.nowFloor = self.nowFloor - 1
        self.elev.setFloorNumber(self.name, self.nowFloor)

    def showStatus(self):
        if self.status == 0:
            self.elev.findChild(QPushButton, "status{0}".format(self.name)).setText("")
        elif self.status == 1:
            self.elev.findChild(QPushButton, "status{0}".format(self.name)).setText("▲")
        elif self.status == -1:
            self.elev.findChild(QPushButton, "status{0}".format(self.name)).setText("▼")

    def run(self):
        while True:
            time.sleep(1)
            if self.elevQueue != 0:
                if (self.elevQueue & (1 << self.nowFloor)) != 0:
                    if self.isIgnore[self.nowFloor] == 0:
                        self.delElev()
                        self.elev.openDoor(self.name)
                        time.sleep(2)
                        self.elev.closeDoor(self.name)
                        if self.elevQueue == 0:
                            self.status = 0
                            self.taskNum = 0
                        elif self.status == 1:
                            if self.hasFloorUp():
                                self.status = 1
                            else:
                                self.status = -1
                        elif self.status == -1:
                            if self.hasFloorDown():
                                self.status = -1
                            else:
                                self.status = 1
                    else:
                        temp = self.isIgnore[self.nowFloor]
                        self.isIgnore[self.nowFloor] = 0
                        if temp == 1:
                            self.turnUp()
                        elif temp == -1:
                            self.turnDown()
                elif self.status == 0:
                    if self.hasFloorUp():
                        self.status = 1
                        self.turnUp()
                    else:
                        self.status = -1
                        self.turnDown()
                elif self.status == 1:
                    self.turnUp()
                elif self.status == -1:
                    self.turnDown()
            else:
                self.status = 0
                self.taskNum = 0

            self.showStatus()

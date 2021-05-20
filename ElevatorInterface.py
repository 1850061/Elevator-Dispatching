# -*- coding: utf-8 -*-
# @Time    : 2021/05/18
# @Author  : rcw
# @Email   : 1763244792@qq.com
# @File    : ElevatorInterface.py
# @Software: PyCharm
from PyQt5.uic.properties import QtWidgets

from Elevator_Manage import Elevator_Manage
from functools import partial

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QPushButton, QLCDNumber, QLabel


class ElevatorInterface(QWidget):  # 主窗口

    def __init__(self):
        super().__init__()
        self.initUI()
        self.elevator_Manage = Elevator_Manage(self)

    def initUI(self):
        # 水平布局管理
        layout = QHBoxLayout()

        # 左边部分（走廊上）部件准备
        gridLayoutLeft = QGridLayout()
        gridLayoutLeft.setSpacing(0)
        leftWidget = QWidget()
        leftWidget.setLayout(gridLayoutLeft)

        # 左边部分（电梯内）部件准备
        grid = QGridLayout()
        grid.setSpacing(0)
        gwg = QWidget()
        gwg.setLayout(grid)

        # 部件加至全局布局
        layout.addWidget(leftWidget)
        layout.addWidget(gwg)

        # 窗体本体设置全局布局
        self.setLayout(layout)

        # --------------------------------------下面是左边布局--------------------------------------#
        # 走廊里的按钮，向上
        outsideElevatorUp = [('▲ %s' % i) for i in range(1, 21)]
        # 走廊里的按钮，向下
        outsideElevatorDown = [('▼ %s' % (21 - i)) for i in range(1, 21)]
        floor = 0
        # 向上按钮的设置
        for i in outsideElevatorUp:
            self.button = QPushButton(i)
            self.button.setFont(QFont("Microsoft YaHei"))
            self.button.setObjectName("up{0}".format(floor + 1))
            self.button.setMinimumHeight(42)
            self.button.clicked.connect(partial(self.set_global_goal_up, floor + 1))
            gridLayoutLeft.addWidget(self.button, 20 - floor, 0)
            floor = floor + 1

        # 向下按钮的设置
        for i in outsideElevatorDown:
            self.button = QPushButton(i)
            self.button.setFont(QFont("Microsoft YaHei"))
            self.button.setObjectName("down{0}".format(floor))
            self.button.setMinimumHeight(42)
            self.button.clicked.connect(partial(self.set_global_goal_down, floor))
            gridLayoutLeft.addWidget(self.button, 20 - floor + 1, 1)
            floor = floor - 1

        # ----------------------------------------------------------------------------------------#

        # --------------------------------------下面是右边布局--------------------------------------#
        # 电梯按钮编号
        names = [('%s' % i) for i in range(1, 21)]
        # 位置
        positions = [(i, j) for j in range(2) for i in range(10)]

        # 电梯内部按键布置
        for elev in range(5):
            floor = 1
            for position, name in zip(positions, names):
                if name == '':
                    continue
                self.button = QPushButton(name)
                self.button.setFont(QFont("Microsoft YaHei", 12))
                self.button.setObjectName("{0}+{1}".format(elev + 1, floor))
                self.button.clicked.connect(partial(self.set_goal, elev + 1, floor))
                floor = floor + 1
                # 按钮最大高度
                self.button.setMaximumHeight(60)
                grid.addWidget(self.button, 9 - position[0] + 2, position[1] + elev * 3)

        # 上下行显示
        for i in range(5):
            self.status = QPushButton()
            self.status.setObjectName("status{0}".format(i + 1))
            self.status.setMinimumHeight(60)
            grid.addWidget(self.status, 0, 3 * i)

        # 数字显示
        for i in range(5):
            self.lcd = QLCDNumber()
            self.lcd.setObjectName("lcd{0}".format(i + 1))
            self.lcd.display(1)
            grid.addWidget(self.lcd, 0, 3 * i, 2, 2)
            # 这几个label是为了增加缝隙
            self.lab = QLabel(self)
            grid.addWidget(self.lab, 0, 3 * i + 2, 1, 1)

        for i in range(grid.rowCount()):
            grid.setRowMinimumHeight(i, 60)

        # 警报器按钮
        for i in range(5):
            self.button = QPushButton("警报器")
            self.button.setFont(QFont("Microsoft YaHei", 12))
            self.button.setObjectName("alarm{0}".format(i + 1))
            self.button.setMinimumHeight(40)
            self.button.clicked.connect(partial(self.alarm, i + 1))
            grid.addWidget(self.button, 12, 3 * i, 1, 2)

        # 开门键，当电梯开门时，按钮上会显示OPEN
        for i in range(5):
            self.button = QPushButton()
            self.button.setObjectName("open{0}".format(i + 1))
            self.button.setMinimumHeight(80)
            grid.addWidget(self.button, 13, 3 * i, 1, 2)

        self.move(10, 10)
        self.setWindowTitle('Elevator-Dispatching 阮辰伟')
        self.show()

    # 设定走廊里上楼请求所在的楼层
    def set_global_goal_up(self, flr):
        self.findChild(QPushButton, "up{0}".format(flr)).setStyleSheet(
            "QPushButton{background-image: url(resource/background.png)}")
        self.elevator_Manage.elevDistribution(flr, 1)

    # 设定走廊里下楼请求所在的楼层
    def set_global_goal_down(self, flr):
        self.findChild(QPushButton, "down{0}".format(flr)).setStyleSheet(
            "QPushButton{background-image: url(resource/background.png)}")
        self.elevator_Manage.elevDistribution(flr, -1)

    # 设定电梯内部目标楼层
    def set_goal(self, elev, flr):
        self.findChild(QPushButton, "{0}+{1}".format(elev, flr)).setStyleSheet(
            "QPushButton{background-image: url(resource/background.png)}")
        self.elevator_Manage.addElev(elev, flr)

    def alarm(self, elev):
        self.findChild(QPushButton, "alarm{0}".format(elev)).setStyleSheet(
            "QPushButton{background-image: url(resource/background.png)}")
        self.findChild(QPushButton, "alarm{0}".format(elev)).setEnabled(False)
        self.findChild(QPushButton, "open{0}".format(elev)).setEnabled(False)
        self.findChild(QLCDNumber, "lcd{0}".format(elev)).setEnabled(False)
        self.elevator_Manage.alarm(elev)
        for floor in range(1, 21):
            self.findChild(QPushButton, "{0}+{1}".format(elev, floor)).setEnabled(False)

    def openDoor(self, elev):
        self.findChild(QPushButton, "open{0}".format(elev)).setStyleSheet(
            "QPushButton{background-image: url(resource/open.png)}")

    def closeDoor(self, elev):
        self.findChild(QPushButton, "open{0}".format(elev)).setStyleSheet(
            "QPushButton{}")

    def setFloorNumber(self, elev, floor):
        self.findChild(QLCDNumber, "lcd{0}".format(elev)).display(floor)

    def delOutElev(self, flr, status):
        self.elevator_Manage.delOutElev(flr, status)

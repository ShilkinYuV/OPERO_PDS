# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_forms\MainWindow_new.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 641)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/bank.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(45, 59, 68);\n"
"color: white;\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(200, 90))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icon/bank.png"))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.horizontalLayout_2.addWidget(self.frame)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setStyleSheet(".QPushButton {\n"
"color: white;\n"
"border: none;\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
".QPushButton:hover {\n"
"color: red;\n"
"border: none;\n"
"padding-left: 20px;\n"
"padding-right: 20px;\n"
"}\n"
"QWidget{\n"
"    background-color: #607E91;\n"
"}\n"
"")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("QWidget{\n"
"    background-color: #607E91\n"
"}\n"
"\n"
".QPushButton {\n"
"color: white;\n"
"background-color: #607E91;\n"
"border-radius: 5px;\n"
"}\n"
".QPushButton:hover {\n"
"background-color: #8AB6D1;\n"
"border-radius: 5px;\n"
"\n"
"}")
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chekDocuments = QtWidgets.QPushButton(self.widget)
        self.chekDocuments.setMinimumSize(QtCore.QSize(200, 50))
        self.chekDocuments.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.chekDocuments.setIcon(icon1)
        self.chekDocuments.setIconSize(QtCore.QSize(35, 35))
        self.chekDocuments.setObjectName("chekDocuments")
        self.verticalLayout_3.addWidget(self.chekDocuments)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.PESSEND = QtWidgets.QPushButton(self.widget)
        self.PESSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.PESSEND.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PESSEND.setIcon(icon2)
        self.PESSEND.setIconSize(QtCore.QSize(35, 35))
        self.PESSEND.setObjectName("PESSEND")
        self.verticalLayout.addWidget(self.PESSEND)
        self.ZVPSEND = QtWidgets.QPushButton(self.widget)
        self.ZVPSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.ZVPSEND.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ZVPSEND.setIcon(icon2)
        self.ZVPSEND.setIconSize(QtCore.QSize(35, 35))
        self.ZVPSEND.setObjectName("ZVPSEND")
        self.verticalLayout.addWidget(self.ZVPSEND)
        self.ZINFSEND = QtWidgets.QPushButton(self.widget)
        self.ZINFSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.ZINFSEND.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ZINFSEND.setIcon(icon2)
        self.ZINFSEND.setIconSize(QtCore.QSize(35, 35))
        self.ZINFSEND.setObjectName("ZINFSEND")
        self.verticalLayout.addWidget(self.ZINFSEND)
        self.ZONDSEND = QtWidgets.QPushButton(self.widget)
        self.ZONDSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.ZONDSEND.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ZONDSEND.setIcon(icon2)
        self.ZONDSEND.setIconSize(QtCore.QSize(35, 35))
        self.ZONDSEND.setObjectName("ZONDSEND")
        self.verticalLayout.addWidget(self.ZONDSEND)
        self.OTZVSEND = QtWidgets.QPushButton(self.widget)
        self.OTZVSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.OTZVSEND.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.OTZVSEND.setIcon(icon2)
        self.OTZVSEND.setIconSize(QtCore.QSize(35, 35))
        self.OTZVSEND.setObjectName("OTZVSEND")
        self.verticalLayout.addWidget(self.OTZVSEND)
        self.RNPSEND = QtWidgets.QPushButton(self.widget)
        self.RNPSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.RNPSEND.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RNPSEND.setIcon(icon2)
        self.RNPSEND.setIconSize(QtCore.QSize(35, 35))
        self.RNPSEND.setObjectName("RNPSEND")
        self.verticalLayout.addWidget(self.RNPSEND)
        self.OTVSEND = QtWidgets.QPushButton(self.widget)
        self.OTVSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.OTVSEND.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.OTVSEND.setStyleSheet("")
        self.OTVSEND.setIcon(icon2)
        self.OTVSEND.setIconSize(QtCore.QSize(35, 35))
        self.OTVSEND.setObjectName("OTVSEND")
        self.verticalLayout.addWidget(self.OTVSEND)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.RNPSEND_PUDS = QtWidgets.QPushButton(self.widget)
        self.RNPSEND_PUDS.setMinimumSize(QtCore.QSize(0, 35))
        self.RNPSEND_PUDS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RNPSEND_PUDS.setIcon(icon2)
        self.RNPSEND_PUDS.setIconSize(QtCore.QSize(35, 35))
        self.RNPSEND_PUDS.setObjectName("RNPSEND_PUDS")
        self.verticalLayout_2.addWidget(self.RNPSEND_PUDS)
        self.OTVSEND_PUDS = QtWidgets.QPushButton(self.widget)
        self.OTVSEND_PUDS.setMinimumSize(QtCore.QSize(0, 35))
        self.OTVSEND_PUDS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.OTVSEND_PUDS.setStyleSheet("")
        self.OTVSEND_PUDS.setIcon(icon2)
        self.OTVSEND_PUDS.setIconSize(QtCore.QSize(35, 35))
        self.OTVSEND_PUDS.setObjectName("OTVSEND_PUDS")
        self.verticalLayout_2.addWidget(self.OTVSEND_PUDS)
        self.ZINFSEND_PUDS = QtWidgets.QPushButton(self.widget)
        self.ZINFSEND_PUDS.setEnabled(False)
        self.ZINFSEND_PUDS.setMinimumSize(QtCore.QSize(0, 35))
        self.ZINFSEND_PUDS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ZINFSEND_PUDS.setIcon(icon2)
        self.ZINFSEND_PUDS.setIconSize(QtCore.QSize(35, 35))
        self.ZINFSEND_PUDS.setObjectName("ZINFSEND_PUDS")
        self.verticalLayout_2.addWidget(self.ZINFSEND_PUDS)
        self.ZONDSEND_PUDS = QtWidgets.QPushButton(self.widget)
        self.ZONDSEND_PUDS.setEnabled(False)
        self.ZONDSEND_PUDS.setMinimumSize(QtCore.QSize(0, 35))
        self.ZONDSEND_PUDS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ZONDSEND_PUDS.setIcon(icon2)
        self.ZONDSEND_PUDS.setIconSize(QtCore.QSize(35, 35))
        self.ZONDSEND_PUDS.setObjectName("ZONDSEND_PUDS")
        self.verticalLayout_2.addWidget(self.ZONDSEND_PUDS)
        self.ZVPSEND_PUDS = QtWidgets.QPushButton(self.widget)
        self.ZVPSEND_PUDS.setEnabled(False)
        self.ZVPSEND_PUDS.setMinimumSize(QtCore.QSize(0, 35))
        self.ZVPSEND_PUDS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ZVPSEND_PUDS.setIcon(icon2)
        self.ZVPSEND_PUDS.setIconSize(QtCore.QSize(35, 35))
        self.ZVPSEND_PUDS.setObjectName("ZVPSEND_PUDS")
        self.verticalLayout_2.addWidget(self.ZVPSEND_PUDS)
        self.PESSEND_PUDS = QtWidgets.QPushButton(self.widget)
        self.PESSEND_PUDS.setEnabled(False)
        self.PESSEND_PUDS.setMinimumSize(QtCore.QSize(0, 35))
        self.PESSEND_PUDS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PESSEND_PUDS.setIcon(icon2)
        self.PESSEND_PUDS.setIconSize(QtCore.QSize(35, 35))
        self.PESSEND_PUDS.setObjectName("PESSEND_PUDS")
        self.verticalLayout_2.addWidget(self.PESSEND_PUDS)
        self.OTZVSEND_PUDS = QtWidgets.QPushButton(self.widget)
        self.OTZVSEND_PUDS.setEnabled(False)
        self.OTZVSEND_PUDS.setMinimumSize(QtCore.QSize(0, 35))
        self.OTZVSEND_PUDS.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.OTZVSEND_PUDS.setIcon(icon2)
        self.OTZVSEND_PUDS.setIconSize(QtCore.QSize(35, 35))
        self.OTZVSEND_PUDS.setObjectName("OTZVSEND_PUDS")
        self.verticalLayout_2.addWidget(self.OTZVSEND_PUDS)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.day = QtWidgets.QPushButton(self.widget)
        self.day.setMinimumSize(QtCore.QSize(0, 35))
        self.day.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/code.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.day.setIcon(icon3)
        self.day.setIconSize(QtCore.QSize(35, 35))
        self.day.setObjectName("day")
        self.verticalLayout_3.addWidget(self.day)
        self.night = QtWidgets.QPushButton(self.widget)
        self.night.setMinimumSize(QtCore.QSize(0, 35))
        self.night.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.night.setIcon(icon3)
        self.night.setIconSize(QtCore.QSize(35, 35))
        self.night.setObjectName("night")
        self.verticalLayout_3.addWidget(self.night)
        self.clearWindow = QtWidgets.QPushButton(self.widget)
        self.clearWindow.setMinimumSize(QtCore.QSize(0, 35))
        self.clearWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.clearWindow.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearWindow.setIcon(icon4)
        self.clearWindow.setIconSize(QtCore.QSize(40, 40))
        self.clearWindow.setObjectName("clearWindow")
        self.verticalLayout_3.addWidget(self.clearWindow)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_3.setStyleSheet(".QTextEdit{\n"
"    background-color: rgb(45, 59, 68);\n"
"    border: none;\n"
"    color: white;\n"
"    padding: 20px;\n"
"}\n"
"\n"
"")
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.textEdit = QtWidgets.QTextEdit(self.widget_3)
        self.textEdit.setEnabled(True)
        self.textEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_5.addWidget(self.textEdit)
        self.horizontalLayout_4.addWidget(self.widget_3)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 4)
        self.verticalLayout_4.addWidget(self.widget)
        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 6)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Настройки"))
        self.pushButton_2.setText(_translate("MainWindow", "О программе"))
        self.chekDocuments.setText(_translate("MainWindow", "Проверить документы"))
        self.label_2.setText(_translate("MainWindow", "АСФК"))
        self.PESSEND.setText(_translate("MainWindow", "PESSEND"))
        self.ZVPSEND.setText(_translate("MainWindow", "ZVPSEND"))
        self.ZINFSEND.setText(_translate("MainWindow", "ZINFSEND"))
        self.ZONDSEND.setText(_translate("MainWindow", "ZONDSEND"))
        self.OTZVSEND.setText(_translate("MainWindow", "OTZVSEND"))
        self.RNPSEND.setText(_translate("MainWindow", "RNPSEND"))
        self.OTVSEND.setText(_translate("MainWindow", "OTVSEND"))
        self.label_3.setText(_translate("MainWindow", "ПУДС"))
        self.RNPSEND_PUDS.setText(_translate("MainWindow", "RNPSEND"))
        self.OTVSEND_PUDS.setText(_translate("MainWindow", "OTVSEND"))
        self.ZINFSEND_PUDS.setText(_translate("MainWindow", "ZINFSEND"))
        self.ZONDSEND_PUDS.setText(_translate("MainWindow", "ZONDSEND"))
        self.ZVPSEND_PUDS.setText(_translate("MainWindow", "ZVPSEND"))
        self.PESSEND_PUDS.setText(_translate("MainWindow", "PESSEND"))
        self.OTZVSEND_PUDS.setText(_translate("MainWindow", "OTZVSEND"))
        self.day.setText(_translate("MainWindow", "ЭПД день"))
        self.night.setText(_translate("MainWindow", "ЭПД ночь"))
from ui_forms import icons_rc

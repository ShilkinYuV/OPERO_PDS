# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainapp_new.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import icons_rc

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1017, 715)
        MainWindow.setStyleSheet("background-color: rgb(45, 59, 68);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 90))
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 90))
        self.widget_2.setStyleSheet("QWidget{\n"
"    background-color: #607E91;\n"
"}\n"
"")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_4 = QtWidgets.QFrame(self.widget_2)
        self.frame_4.setStyleSheet("QWidget{\n"
"background-color: #364752;\n"
"}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_4)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":icon/bank.png"))
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout.addWidget(self.frame_4)
        self.widget_5 = QtWidgets.QWidget(self.widget_2)
        self.widget_5.setStyleSheet(".QPushButton {\n"
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
"}")
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton = QtWidgets.QPushButton(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_5)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget_5)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.verticalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget1 = QtWidgets.QWidget(self.widget)
        self.widget1.setStyleSheet("QWidget{\n"
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
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 25, 0, 25)
        self.verticalLayout_3.setSpacing(15)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chekDocuments = QtWidgets.QPushButton(self.widget1)
        self.chekDocuments.setMinimumSize(QtCore.QSize(0, 35))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":icon/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.chekDocuments.setIcon(icon)
        self.chekDocuments.setIconSize(QtCore.QSize(35, 35))
        self.chekDocuments.setObjectName("chekDocuments")
        self.verticalLayout_3.addWidget(self.chekDocuments)
        self.PESSEND = QtWidgets.QPushButton(self.widget1)
        self.PESSEND.setMinimumSize(QtCore.QSize(0, 35))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":icon/copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PESSEND.setIcon(icon1)
        self.PESSEND.setIconSize(QtCore.QSize(35, 35))
        self.PESSEND.setObjectName("PESSEND")
        self.verticalLayout_3.addWidget(self.PESSEND)
        self.ZVPSEND = QtWidgets.QPushButton(self.widget1)
        self.ZVPSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.ZVPSEND.setIcon(icon1)
        self.ZVPSEND.setIconSize(QtCore.QSize(35, 35))
        self.ZVPSEND.setObjectName("ZVPSEND")
        self.verticalLayout_3.addWidget(self.ZVPSEND)
        self.ZINFSEND = QtWidgets.QPushButton(self.widget1)
        self.ZINFSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.ZINFSEND.setIcon(icon1)
        self.ZINFSEND.setIconSize(QtCore.QSize(35, 35))
        self.ZINFSEND.setObjectName("ZINFSEND")
        self.verticalLayout_3.addWidget(self.ZINFSEND)
        self.ZONDSEND = QtWidgets.QPushButton(self.widget1)
        self.ZONDSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.ZONDSEND.setIcon(icon1)
        self.ZONDSEND.setIconSize(QtCore.QSize(35, 35))
        self.ZONDSEND.setObjectName("ZONDSEND")
        self.verticalLayout_3.addWidget(self.ZONDSEND)
        self.OTZVSEND = QtWidgets.QPushButton(self.widget1)
        self.OTZVSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.OTZVSEND.setIcon(icon1)
        self.OTZVSEND.setIconSize(QtCore.QSize(35, 35))
        self.OTZVSEND.setObjectName("OTZVSEND")
        self.verticalLayout_3.addWidget(self.OTZVSEND)
        self.RNPSEND = QtWidgets.QPushButton(self.widget1)
        self.RNPSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.RNPSEND.setIcon(icon1)
        self.RNPSEND.setIconSize(QtCore.QSize(35, 35))
        self.RNPSEND.setObjectName("RNPSEND")
        self.verticalLayout_3.addWidget(self.RNPSEND)
        self.OTVSEND = QtWidgets.QPushButton(self.widget1)
        self.OTVSEND.setMinimumSize(QtCore.QSize(0, 35))
        self.OTVSEND.setStyleSheet("")
        self.OTVSEND.setIcon(icon1)
        self.OTVSEND.setIconSize(QtCore.QSize(35, 35))
        self.OTVSEND.setObjectName("OTVSEND")
        self.verticalLayout_3.addWidget(self.OTVSEND)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.day = QtWidgets.QPushButton(self.widget1)
        self.day.setMinimumSize(QtCore.QSize(0, 35))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":icon/code.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.day.setIcon(icon2)
        self.day.setIconSize(QtCore.QSize(35, 35))
        self.day.setObjectName("day")
        self.verticalLayout_3.addWidget(self.day)
        self.night = QtWidgets.QPushButton(self.widget1)
        self.night.setMinimumSize(QtCore.QSize(0, 35))
        self.night.setIcon(icon2)
        self.night.setIconSize(QtCore.QSize(35, 35))
        self.night.setObjectName("night")
        self.verticalLayout_3.addWidget(self.night)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.clearWindow = QtWidgets.QPushButton(self.widget1)
        self.clearWindow.setMinimumSize(QtCore.QSize(0, 35))
        self.clearWindow.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":icon/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearWindow.setIcon(icon3)
        self.clearWindow.setIconSize(QtCore.QSize(40, 40))
        self.clearWindow.setObjectName("clearWindow")
        self.verticalLayout_3.addWidget(self.clearWindow)
        self.horizontalLayout_2.addWidget(self.widget1)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.widget_3.setFont(font)
        self.widget_3.setStyleSheet(".QTextEdit{\n"
"    background-color: rgb(45, 59, 68);\n"
"    border: none;\n"
"    color: white;\n"
"    padding: 20px;\n"
"}\n"
"\n"
"")
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.textEdit = QtWidgets.QTextEdit(self.widget_3)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(False)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_5.addWidget(self.textEdit)
        self.horizontalLayout_2.addWidget(self.widget_3)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.settings = QtWidgets.QAction(MainWindow)
        self.settings.setObjectName("settings")
        self.about = QtWidgets.QAction(MainWindow)
        self.about.setObjectName("about")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Настройки"))
        self.pushButton_2.setText(_translate("MainWindow", "О программе"))
        self.chekDocuments.setText(_translate("MainWindow", "Проверить документы"))
        self.PESSEND.setText(_translate("MainWindow", "PESSEND"))
        self.ZVPSEND.setText(_translate("MainWindow", "ZVPSEND"))
        self.ZINFSEND.setText(_translate("MainWindow", "ZINFSEND"))
        self.ZONDSEND.setText(_translate("MainWindow", "ZONDSEND"))
        self.OTZVSEND.setText(_translate("MainWindow", "OTZVSEND"))
        self.RNPSEND.setText(_translate("MainWindow", "RNPSEND"))
        self.OTVSEND.setText(_translate("MainWindow", "OTVSEND"))
        self.day.setText(_translate("MainWindow", "ЭПД день"))
        self.night.setText(_translate("MainWindow", "ЭПД ночь"))
        self.settings.setText(_translate("MainWindow", "Настройки"))
        self.about.setText(_translate("MainWindow", "О программе"))
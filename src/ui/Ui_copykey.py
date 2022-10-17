# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file
# '/home/kale/github/fast-translate/src/ui/copykey.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Copykey(object):
    def setupUi(self, Preference):
        Preference.setObjectName("Preference")
        Preference.setEnabled(True)
        Preference.resize(364, 130)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Preference.sizePolicy().hasHeightForWidth())
        Preference.setSizePolicy(sizePolicy)
        Preference.setMaximumSize(QtCore.QSize(800, 350))
        Preference.setSizeIncrement(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./data/icon/settings.svg"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        Preference.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Preference)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.copykeySettingLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        self.copykeySettingLabel.setFont(font)
        self.copykeySettingLabel.setMouseTracking(False)
        self.copykeySettingLabel.setScaledContents(False)
        self.copykeySettingLabel.setObjectName("copykeySettingLabel")
        self.gridLayout.addWidget(self.copykeySettingLabel, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.copykeyLabel = QtWidgets.QLabel(self.centralwidget)
        self.copykeyLabel.setObjectName("copykeyLabel")
        self.horizontalLayout_2.addWidget(self.copykeyLabel)
        self.copykeyTextLabel = QtWidgets.QLabel(self.centralwidget)
        self.copykeyTextLabel.setText("")
        self.copykeyTextLabel.setObjectName("copykeyTextLabel")
        self.horizontalLayout_2.addWidget(self.copykeyTextLabel)
        self.copykeyResetButton = QtWidgets.QPushButton(self.centralwidget)
        self.copykeyResetButton.setObjectName("copykeyResetButton")
        self.horizontalLayout_2.addWidget(self.copykeyResetButton)
        self.copykeySaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.copykeySaveButton.setObjectName("copykeySaveButton")
        self.horizontalLayout_2.addWidget(self.copykeySaveButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        Preference.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Preference)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 364, 32))
        self.menubar.setObjectName("menubar")
        Preference.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Preference)
        self.statusbar.setObjectName("statusbar")
        Preference.setStatusBar(self.statusbar)

        self.retranslateUi(Preference)
        QtCore.QMetaObject.connectSlotsByName(Preference)

    def retranslateUi(self, Preference):
        _translate = QtCore.QCoreApplication.translate
        Preference.setWindowTitle(_translate("Preference", "设置"))
        self.copykeySettingLabel.setText(_translate("Preference", "修改复制热键"))
        self.copykeyLabel.setText(_translate("Preference", "复制"))
        self.copykeyResetButton.setText(_translate("Preference", "重置"))
        self.copykeySaveButton.setText(_translate("Preference", "保存"))

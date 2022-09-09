# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kale/github/fast-translate/src/ui/translate.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(633, 767)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./config/icon/logo.svg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.originalText = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.originalText.sizePolicy().hasHeightForWidth())
        self.originalText.setSizePolicy(sizePolicy)
        self.originalText.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.originalText.setObjectName("originalText")
        self.verticalLayout_3.addWidget(self.originalText)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.targetBox = QtWidgets.QComboBox(self.centralwidget)
        self.targetBox.setObjectName("targetBox")
        self.horizontalLayout_2.addWidget(self.targetBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.translateButton = QtWidgets.QPushButton(self.centralwidget)
        self.translateButton.setObjectName("translateButton")
        self.horizontalLayout_2.addWidget(self.translateButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.instantTranslateMode = QtWidgets.QComboBox(self.centralwidget)
        self.instantTranslateMode.setObjectName("instantTranslateMode")
        self.horizontalLayout_2.addWidget(self.instantTranslateMode)
        self.translateNowBox = QtWidgets.QCheckBox(self.centralwidget)
        self.translateNowBox.setObjectName("translateNowBox")
        self.horizontalLayout_2.addWidget(self.translateNowBox)
        self.additionalBox = QtWidgets.QCheckBox(self.centralwidget)
        self.additionalBox.setObjectName("additionalBox")
        self.horizontalLayout_2.addWidget(self.additionalBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.baiduBox = QtWidgets.QCheckBox(self.centralwidget)
        self.baiduBox.setObjectName("baiduBox")
        self.horizontalLayout_3.addWidget(self.baiduBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.googleBox = QtWidgets.QCheckBox(self.centralwidget)
        self.googleBox.setObjectName("googleBox")
        self.horizontalLayout_3.addWidget(self.googleBox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.googleCNBox = QtWidgets.QCheckBox(self.centralwidget)
        self.googleCNBox.setObjectName("googleCNBox")
        self.horizontalLayout_3.addWidget(self.googleCNBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.baiduLabel = QtWidgets.QLabel(self.centralwidget)
        self.baiduLabel.setObjectName("baiduLabel")
        self.verticalLayout_3.addWidget(self.baiduLabel)
        self.baiduText = QtWidgets.QTextEdit(self.centralwidget)
        self.baiduText.setObjectName("baiduText")
        self.verticalLayout_3.addWidget(self.baiduText)
        self.googleLable = QtWidgets.QLabel(self.centralwidget)
        self.googleLable.setObjectName("googleLable")
        self.verticalLayout_3.addWidget(self.googleLable)
        self.googleText = QtWidgets.QTextEdit(self.centralwidget)
        self.googleText.setObjectName("googleText")
        self.verticalLayout_3.addWidget(self.googleText)
        self.googleCNLable = QtWidgets.QLabel(self.centralwidget)
        self.googleCNLable.setObjectName("googleCNLable")
        self.verticalLayout_3.addWidget(self.googleCNLable)
        self.googleCNText = QtWidgets.QTextEdit(self.centralwidget)
        self.googleCNText.setObjectName("googleCNText")
        self.verticalLayout_3.addWidget(self.googleCNText)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 633, 32))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.translateSetting = QtWidgets.QAction(MainWindow)
        self.translateSetting.setObjectName("translateSetting")
        self.aboutSetting = QtWidgets.QAction(MainWindow)
        self.aboutSetting.setObjectName("aboutSetting")
        self.menu.addAction(self.translateSetting)
        self.menu.addAction(self.aboutSetting)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Fast-Translate"))
        self.translateButton.setText(_translate("MainWindow", "翻译"))
        self.translateNowBox.setText(_translate("MainWindow", "即时翻译"))
        self.additionalBox.setText(_translate("MainWindow", "追加翻译"))
        self.baiduBox.setText(_translate("MainWindow", "百度翻译"))
        self.googleBox.setText(_translate("MainWindow", "谷歌翻译"))
        self.googleCNBox.setText(_translate("MainWindow", "谷歌翻译[CN源]"))
        self.baiduLabel.setText(_translate("MainWindow", "百度翻译"))
        self.googleLable.setText(_translate("MainWindow", "谷歌翻译"))
        self.googleCNLable.setText(_translate("MainWindow", "谷歌翻译[CN源]"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.translateSetting.setText(_translate("MainWindow", "翻译设置"))
        self.aboutSetting.setText(_translate("MainWindow", "关于"))

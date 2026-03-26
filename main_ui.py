# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDateEdit, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTextBrowser, QTimeEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(874, 771)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_8 = QGridLayout(self.tab_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_4 = QSpacerItem(17, 28, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Start_Button = QPushButton(self.tab_3)
        self.Start_Button.setObjectName(u"Start_Button")

        self.horizontalLayout_3.addWidget(self.Start_Button)

        self.Pause_checkBox = QCheckBox(self.tab_3)
        self.Pause_checkBox.setObjectName(u"Pause_checkBox")

        self.horizontalLayout_3.addWidget(self.Pause_checkBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.OpenResButton = QPushButton(self.tab_3)
        self.OpenResButton.setObjectName(u"OpenResButton")
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentPageSetup))
        self.OpenResButton.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.OpenResButton)

        self.horizontalSpacer_7 = QSpacerItem(5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.OpenFileFolderButton = QPushButton(self.tab_3)
        self.OpenFileFolderButton.setObjectName(u"OpenFileFolderButton")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
        self.OpenFileFolderButton.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.OpenFileFolderButton)

        self.horizontalLayout_5.setStretch(0, 7)
        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer_7)

        self.OpenPriceFileButton = QPushButton(self.tab_3)
        self.OpenPriceFileButton.setObjectName(u"OpenPriceFileButton")
        self.OpenPriceFileButton.setIcon(icon)

        self.verticalLayout_2.addWidget(self.OpenPriceFileButton)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.OpenArchiveDirButton = QPushButton(self.tab_3)
        self.OpenArchiveDirButton.setObjectName(u"OpenArchiveDirButton")

        self.verticalLayout_2.addWidget(self.OpenArchiveDirButton)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)


        self.horizontalLayout_11.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_4 = QSpacerItem(25, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.tab_3)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setInputMethodHints(Qt.InputMethodHint.ImhSensitiveData)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.groupBox = QGroupBox(self.tab_3)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_4 = QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout.addWidget(self.label_8)

        self.ozon_extra_col_timeEdit = QTimeEdit(self.groupBox)
        self.ozon_extra_col_timeEdit.setObjectName(u"ozon_extra_col_timeEdit")

        self.horizontalLayout.addWidget(self.ozon_extra_col_timeEdit)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.ozon_extra_col_timeEdit_2 = QTimeEdit(self.groupBox)
        self.ozon_extra_col_timeEdit_2.setObjectName(u"ozon_extra_col_timeEdit_2")

        self.horizontalLayout_2.addWidget(self.ozon_extra_col_timeEdit_2)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.gridLayout_4.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_6 = QGridLayout(self.groupBox_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.horizontalLayout_13.addWidget(self.label_11)

        self.wb_extra_col_timeEdit = QTimeEdit(self.groupBox_2)
        self.wb_extra_col_timeEdit.setObjectName(u"wb_extra_col_timeEdit")

        self.horizontalLayout_13.addWidget(self.wb_extra_col_timeEdit)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.horizontalLayout_13.addWidget(self.label_12)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_20)


        self.gridLayout_6.addLayout(self.horizontalLayout_13, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_9)

        self.wb_extra_col_timeEdit_2 = QTimeEdit(self.groupBox_2)
        self.wb_extra_col_timeEdit_2.setObjectName(u"wb_extra_col_timeEdit_2")

        self.horizontalLayout_6.addWidget(self.wb_extra_col_timeEdit_2)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.horizontalLayout_6.addWidget(self.label_10)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_19)


        self.gridLayout_6.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.tab_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_17 = QLabel(self.groupBox_3)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_17)

        self.ya_extra_col_timeEdit = QTimeEdit(self.groupBox_3)
        self.ya_extra_col_timeEdit.setObjectName(u"ya_extra_col_timeEdit")

        self.horizontalLayout_9.addWidget(self.ya_extra_col_timeEdit)

        self.label_16 = QLabel(self.groupBox_3)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_16)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_17)


        self.gridLayout_2.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_19 = QLabel(self.groupBox_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_19)

        self.ya_extra_col_timeEdit_2 = QTimeEdit(self.groupBox_3)
        self.ya_extra_col_timeEdit_2.setObjectName(u"ya_extra_col_timeEdit_2")

        self.horizontalLayout_10.addWidget(self.ya_extra_col_timeEdit_2)

        self.label_18 = QLabel(self.groupBox_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_18)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_23)


        self.gridLayout_2.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_3, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_7)


        self.horizontalLayout_11.addLayout(self.verticalLayout)

        self.horizontalSpacer_2 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_8 = QSpacerItem(13, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)

        self.BadArticleCountLabel = QLabel(self.tab_3)
        self.BadArticleCountLabel.setObjectName(u"BadArticleCountLabel")
        self.BadArticleCountLabel.setFont(font)

        self.horizontalLayout_4.addWidget(self.BadArticleCountLabel)

        self.horizontalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.OpenReportButton = QPushButton(self.tab_3)
        self.OpenReportButton.setObjectName(u"OpenReportButton")
        self.OpenReportButton.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.OpenReportButton)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_14)

        self.ApiData_label = QLabel(self.tab_3)
        self.ApiData_label.setObjectName(u"ApiData_label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.ApiData_label.setFont(font1)

        self.horizontalLayout_4.addWidget(self.ApiData_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.Logs_pushButton = QPushButton(self.tab_3)
        self.Logs_pushButton.setObjectName(u"Logs_pushButton")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FormatJustifyLeft))
        self.Logs_pushButton.setIcon(icon2)

        self.horizontalLayout_4.addWidget(self.Logs_pushButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.Log_textBrowser = QTextBrowser(self.tab_3)
        self.Log_textBrowser.setObjectName(u"Log_textBrowser")

        self.verticalLayout_3.addWidget(self.Log_textBrowser)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 7)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 1)
        self.verticalLayout_3.setStretch(4, 17)

        self.gridLayout_8.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.gridLayout_3 = QGridLayout(self.tab_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.Start_Button_2 = QPushButton(self.tab_4)
        self.Start_Button_2.setObjectName(u"Start_Button_2")

        self.horizontalLayout_7.addWidget(self.Start_Button_2)

        self.horizontalSpacer_13 = QSpacerItem(30, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_13)

        self.label_5 = QLabel(self.tab_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.dateEdit_1 = QDateEdit(self.tab_4)
        self.dateEdit_1.setObjectName(u"dateEdit_1")
        self.dateEdit_1.setDateTime(QDateTime(QDate(2025, 12, 27), QTime(0, 0, 0)))
        self.dateEdit_1.setTime(QTime(0, 0, 0))

        self.horizontalLayout_7.addWidget(self.dateEdit_1)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)

        self.label_6 = QLabel(self.tab_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_6)

        self.dateEdit_2 = QDateEdit(self.tab_4)
        self.dateEdit_2.setObjectName(u"dateEdit_2")
        self.dateEdit_2.setDateTime(QDateTime(QDate(2025, 12, 31), QTime(9, 0, 0)))

        self.horizontalLayout_7.addWidget(self.dateEdit_2)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_12)

        self.autoData_pushButton = QPushButton(self.tab_4)
        self.autoData_pushButton.setObjectName(u"autoData_pushButton")

        self.horizontalLayout_7.addWidget(self.autoData_pushButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.widget = QWidget(self.tab_4)
        self.widget.setObjectName(u"widget")

        self.verticalLayout_4.addWidget(self.widget)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_10)

        self.Logs_pushButton_2 = QPushButton(self.tab_4)
        self.Logs_pushButton_2.setObjectName(u"Logs_pushButton_2")
        self.Logs_pushButton_2.setIcon(icon2)

        self.horizontalLayout_8.addWidget(self.Logs_pushButton_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.Log_textBrowser_2 = QTextBrowser(self.tab_4)
        self.Log_textBrowser_2.setObjectName(u"Log_textBrowser_2")

        self.verticalLayout_4.addWidget(self.Log_textBrowser_2)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 10)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 6)

        self.gridLayout_3.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_5 = QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.Start_tg_Button_4 = QPushButton(self.tab_2)
        self.Start_tg_Button_4.setObjectName(u"Start_tg_Button_4")
        font2 = QFont()
        font2.setPointSize(9)
        self.Start_tg_Button_4.setFont(font2)

        self.horizontalLayout_14.addWidget(self.Start_tg_Button_4)

        self.Stop_tg_Button_4 = QPushButton(self.tab_2)
        self.Stop_tg_Button_4.setObjectName(u"Stop_tg_Button_4")
        self.Stop_tg_Button_4.setFont(font2)

        self.horizontalLayout_14.addWidget(self.Stop_tg_Button_4)

        self.horizontalSpacer_21 = QSpacerItem(30, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_21)

        self.TgStatus_label = QLabel(self.tab_2)
        self.TgStatus_label.setObjectName(u"TgStatus_label")

        self.horizontalLayout_14.addWidget(self.TgStatus_label)

        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_22)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_18)

        self.Logs_pushButton_4_ = QPushButton(self.tab_2)
        self.Logs_pushButton_4_.setObjectName(u"Logs_pushButton_4_")
        self.Logs_pushButton_4_.setIcon(icon2)

        self.horizontalLayout_12.addWidget(self.Logs_pushButton_4_)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.Log_textBrowser_4 = QTextBrowser(self.tab_2)
        self.Log_textBrowser_4.setObjectName(u"Log_textBrowser_4")

        self.verticalLayout_7.addWidget(self.Log_textBrowser_4)

        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(2, 12)

        self.gridLayout_5.addLayout(self.verticalLayout_7, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 874, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Start_Button.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.Pause_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0443\u0437\u043b\u0430", None))
        self.OpenResButton.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0441 \u043a\u043e\u043b-\u0432\u043e\u043c", None))
        self.OpenFileFolderButton.setText("")
        self.OpenPriceFileButton.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0441 \u0446\u0435\u043d\u0430\u043c\u0438", None))
        self.OpenArchiveDirButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043f\u0430\u043f\u043a\u0443 \u0441 \u0430\u0440\u0445\u0438\u0432\u0430\u043c\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0434\u0435\u043b\u044c\u043d\u043e \u0432\u044b\u0432\u043e\u0434\u0438\u0442\u044c \u043f\u043e\u0437\u0438\u0446\u0438\u0438:", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Ozon", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0441:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"(\u0412\u0447\u0435\u0440\u0430)", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0434\u043e:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"(\u0421\u0435\u0433\u043e\u0434\u043d\u044f)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"WB", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u0441:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"(\u0412\u0447\u0435\u0440\u0430)", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u0434\u043e:", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"(\u0421\u0435\u0433\u043e\u0434\u043d\u044f)", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Yandex", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u0441:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"(\u0412\u0447\u0435\u0440\u0430)", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u0434\u043e:", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"(\u0421\u0435\u0433\u043e\u0434\u043d\u044f)", None))
        self.BadArticleCountLabel.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0442\u0435\u0440\u044f\u043d\u043d\u044b\u0435 \u0430\u0440\u0442\u0438\u043a\u0443\u043b\u044b: 0", None))
        self.OpenReportButton.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0441\u043f\u0438\u0441\u043e\u043a", None))
        self.ApiData_label.setText(QCoreApplication.translate("MainWindow", u"API \u0442\u043e\u043a\u0435\u043d\u044b \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0442\u0435\u043b\u044c\u043d\u044b \u0434\u043e -", None))
        self.Logs_pushButton.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0445\u043e\u0434", None))
        self.Start_Button_2.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0437\u0430\u043a\u0430\u0437\u044b \u0441", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u043f\u043e", None))
        self.autoData_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0432\u0442\u043e\u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0434\u0430\u0442 (\u0441\u0435\u0433\u043e\u0434\u043d\u044f \u043c\u0438\u043d\u0443\u0441 \u043d\u0435\u0434\u0435\u043b\u044f)", None))
        self.Logs_pushButton_2.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u0420\u0430\u0441\u0445\u043e\u0434 \u0437\u0430 \u043f\u0435\u0440\u0438\u043e\u0434", None))
        self.Start_tg_Button_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))
        self.Stop_tg_Button_4.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u043e\u043f", None))
        self.TgStatus_label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0443\u0441: \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d", None))
        self.Logs_pushButton_4_.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Telegram \u0431\u043e\u0442", None))
    # retranslateUi


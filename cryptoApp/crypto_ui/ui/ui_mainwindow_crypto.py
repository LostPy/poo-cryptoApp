# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow_crypto.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTabWidget, QVBoxLayout,
    QWidget)

from ..widgets import PortfolioChart
from ressources import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(919, 655)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setBaseSize(QSize(5, 0))
        self.mainPage = QWidget()
        self.mainPage.setObjectName(u"mainPage")
        self.horizontalLayout_5 = QHBoxLayout(self.mainPage)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.tabWidget = QTabWidget(self.mainPage)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setIconSize(QSize(50, 50))
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.portfolio_chart = PortfolioChart(self.widget)
        self.portfolio_chart.setObjectName(u"portfolio_chart")

        self.horizontalLayout_6.addWidget(self.portfolio_chart)

        self.horizontalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.listWidget_top10 = QListWidget(self.widget)
        self.listWidget_top10.setObjectName(u"listWidget_top10")

        self.horizontalLayout_6.addWidget(self.listWidget_top10)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.listWidget_tr = QListWidget(self.widget)
        self.listWidget_tr.setObjectName(u"listWidget_tr")

        self.verticalLayout_6.addWidget(self.listWidget_tr)

        icon = QIcon()
        icon.addFile(u":/finance/bitcoin-black.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.widget, icon, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        icon1 = QIcon()
        icon1.addFile(u":/chart/line-chart-black.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab, icon1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        icon2 = QIcon()
        icon2.addFile(u":/finance/exchange-black.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon2, "")

        self.horizontalLayout_5.addWidget(self.tabWidget)

        self.stackedWidget.addWidget(self.mainPage)
        self.loginPage = QWidget()
        self.loginPage.setObjectName(u"loginPage")
        self.verticalLayout_2 = QVBoxLayout(self.loginPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 171, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.groupBoxLogin = QGroupBox(self.loginPage)
        self.groupBoxLogin.setObjectName(u"groupBoxLogin")
        self.groupBoxLogin.setMinimumSize(QSize(200, 200))
        self.verticalLayout_3 = QVBoxLayout(self.groupBoxLogin)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.groupBoxLogin)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.comboBoxPortfolio = QComboBox(self.groupBoxLogin)
        self.comboBoxPortfolio.setObjectName(u"comboBoxPortfolio")

        self.verticalLayout_3.addWidget(self.comboBoxPortfolio)

        self.label_2 = QLabel(self.groupBoxLogin)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.lineEditPw = QLineEdit(self.groupBoxLogin)
        self.lineEditPw.setObjectName(u"lineEditPw")
        self.lineEditPw.setEchoMode(QLineEdit.Password)

        self.verticalLayout_3.addWidget(self.lineEditPw)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.line = QFrame(self.groupBoxLogin)
        self.line.setObjectName(u"line")
        self.line.setBaseSize(QSize(10, 0))
        font = QFont()
        font.setPointSize(14)
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.buttonNewPortfolio = QPushButton(self.groupBoxLogin)
        self.buttonNewPortfolio.setObjectName(u"buttonNewPortfolio")

        self.horizontalLayout_2.addWidget(self.buttonNewPortfolio)

        self.buttonDelPortfolio = QPushButton(self.groupBoxLogin)
        self.buttonDelPortfolio.setObjectName(u"buttonDelPortfolio")

        self.horizontalLayout_2.addWidget(self.buttonDelPortfolio)

        self.buttonLogin = QPushButton(self.groupBoxLogin)
        self.buttonLogin.setObjectName(u"buttonLogin")

        self.horizontalLayout_2.addWidget(self.buttonLogin)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addWidget(self.groupBoxLogin)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 170, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.loginPage)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_5 = QVBoxLayout(self.page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_4 = QSpacerItem(20, 148, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.groupBox = QGroupBox(self.page)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_4.addWidget(self.label_4)

        self.lineEditNewName = QLineEdit(self.groupBox)
        self.lineEditNewName.setObjectName(u"lineEditNewName")
        self.lineEditNewName.setEchoMode(QLineEdit.Normal)

        self.verticalLayout_4.addWidget(self.lineEditNewName)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_6)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_4.addWidget(self.label_5)

        self.lineEditNewPw = QLineEdit(self.groupBox)
        self.lineEditNewPw.setObjectName(u"lineEditNewPw")
        self.lineEditNewPw.setEchoMode(QLineEdit.Password)

        self.verticalLayout_4.addWidget(self.lineEditNewPw)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setBaseSize(QSize(10, 0))
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.buttonOkNp = QPushButton(self.groupBox)
        self.buttonOkNp.setObjectName(u"buttonOkNp")

        self.horizontalLayout_3.addWidget(self.buttonOkNp)

        self.buttonCancelNp = QPushButton(self.groupBox)
        self.buttonCancelNp.setObjectName(u"buttonCancelNp")

        self.horizontalLayout_3.addWidget(self.buttonCancelNp)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addWidget(self.groupBox)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_5 = QSpacerItem(20, 147, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.stackedWidget.addWidget(self.page)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "")
        self.groupBoxLogin.setTitle(QCoreApplication.translate("MainWindow", u"Login", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Portfolio", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.buttonNewPortfolio.setText(QCoreApplication.translate("MainWindow", u"New portfolio", None))
        self.buttonDelPortfolio.setText(QCoreApplication.translate("MainWindow", u"Del portfolio", None))
        self.buttonLogin.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"New Portfolio", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"New Portfolio Name", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"New Password", None))
        self.buttonOkNp.setText(QCoreApplication.translate("MainWindow", u"Ok", None))
        self.buttonCancelNp.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow_crypto.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QDoubleSpinBox, QFrame, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStackedWidget,
    QTabWidget, QTreeView, QVBoxLayout, QWidget)

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

        self.listWidget_top10 = QListWidget(self.widget)
        self.listWidget_top10.setObjectName(u"listWidget_top10")

        self.horizontalLayout_6.addWidget(self.listWidget_top10)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.listWidget_fav = QListWidget(self.widget)
        self.listWidget_fav.setObjectName(u"listWidget_fav")
        self.listWidget_fav.setMovement(QListView.Static)
        self.listWidget_fav.setResizeMode(QListView.Adjust)

        self.verticalLayout_6.addWidget(self.listWidget_fav)

        icon = QIcon()
        icon.addFile(u":/finance/bitcoin-black.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.widget, icon, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_21 = QVBoxLayout(self.tab)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_20 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_17.addWidget(self.label_7)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_17.addWidget(self.label_8)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_17.addWidget(self.label_9)


        self.horizontalLayout_10.addLayout(self.verticalLayout_17)

        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.comboBoxCrypto = QComboBox(self.groupBox_2)
        self.comboBoxCrypto.setObjectName(u"comboBoxCrypto")

        self.verticalLayout_18.addWidget(self.comboBoxCrypto)

        self.comboBoxFiat = QComboBox(self.groupBox_2)
        self.comboBoxFiat.setObjectName(u"comboBoxFiat")

        self.verticalLayout_18.addWidget(self.comboBoxFiat)

        self.comboBoxDays = QComboBox(self.groupBox_2)
        self.comboBoxDays.addItem("")
        self.comboBoxDays.addItem("")
        self.comboBoxDays.addItem("")
        self.comboBoxDays.addItem("")
        self.comboBoxDays.addItem("")
        self.comboBoxDays.addItem("")
        self.comboBoxDays.setObjectName(u"comboBoxDays")

        self.verticalLayout_18.addWidget(self.comboBoxDays)


        self.horizontalLayout_10.addLayout(self.verticalLayout_18)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.lineEditCrypto = QLineEdit(self.groupBox_2)
        self.lineEditCrypto.setObjectName(u"lineEditCrypto")

        self.verticalLayout_19.addWidget(self.lineEditCrypto)

        self.lineEditFiat = QLineEdit(self.groupBox_2)
        self.lineEditFiat.setObjectName(u"lineEditFiat")

        self.verticalLayout_19.addWidget(self.lineEditFiat)

        self.verticalSpacer_9 = QSpacerItem(20, 22, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_19.addItem(self.verticalSpacer_9)


        self.horizontalLayout_10.addLayout(self.verticalLayout_19)


        self.verticalLayout_20.addLayout(self.horizontalLayout_10)

        self.buttonUpdateMarketChart = QPushButton(self.groupBox_2)
        self.buttonUpdateMarketChart.setObjectName(u"buttonUpdateMarketChart")

        self.verticalLayout_20.addWidget(self.buttonUpdateMarketChart)


        self.verticalLayout_21.addWidget(self.groupBox_2)

        self.graphicsView = QChartView(self.tab)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_21.addWidget(self.graphicsView)

        icon1 = QIcon()
        icon1.addFile(u":/chart/line-chart-black.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.tabWidget.addTab(self.tab, icon1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_11 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.splitter = QSplitter(self.tab_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_12 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.treeView = QTreeView(self.layoutWidget)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout_12.addWidget(self.treeView)

        self.groupBoxTransactions = QGroupBox(self.layoutWidget)
        self.groupBoxTransactions.setObjectName(u"groupBoxTransactions")
        self.verticalLayout_11 = QVBoxLayout(self.groupBoxTransactions)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_3 = QLabel(self.groupBoxTransactions)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_7.addWidget(self.label_3)

        self.label_6 = QLabel(self.groupBoxTransactions)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_7.addWidget(self.label_6)


        self.horizontalLayout_8.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.comboBoxSend = QComboBox(self.groupBoxTransactions)
        self.comboBoxSend.setObjectName(u"comboBoxSend")

        self.verticalLayout_8.addWidget(self.comboBoxSend)

        self.comboBoxReceive = QComboBox(self.groupBoxTransactions)
        self.comboBoxReceive.setObjectName(u"comboBoxReceive")

        self.verticalLayout_8.addWidget(self.comboBoxReceive)


        self.horizontalLayout_8.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.lineEditSend = QLineEdit(self.groupBoxTransactions)
        self.lineEditSend.setObjectName(u"lineEditSend")

        self.verticalLayout_9.addWidget(self.lineEditSend)

        self.lineEditReceive = QLineEdit(self.groupBoxTransactions)
        self.lineEditReceive.setObjectName(u"lineEditReceive")

        self.verticalLayout_9.addWidget(self.lineEditReceive)


        self.horizontalLayout_8.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.spinBoxSpend = QDoubleSpinBox(self.groupBoxTransactions)
        self.spinBoxSpend.setObjectName(u"spinBoxSpend")
        self.spinBoxSpend.setMinimum(0.000000000000000)
        self.spinBoxSpend.setMaximum(100000000.000000000000000)

        self.verticalLayout_10.addWidget(self.spinBoxSpend)

        self.spinBoxReceive = QDoubleSpinBox(self.groupBoxTransactions)
        self.spinBoxReceive.setObjectName(u"spinBoxReceive")
        self.spinBoxReceive.setMinimum(0.000000000000000)
        self.spinBoxReceive.setMaximum(100000000.000000000000000)

        self.verticalLayout_10.addWidget(self.spinBoxReceive)


        self.horizontalLayout_8.addLayout(self.verticalLayout_10)


        self.verticalLayout_11.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)

        self.buttonAdd = QPushButton(self.groupBoxTransactions)
        self.buttonAdd.setObjectName(u"buttonAdd")
        self.buttonAdd.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.buttonAdd)


        self.verticalLayout_11.addLayout(self.horizontalLayout_7)


        self.verticalLayout_12.addWidget(self.groupBoxTransactions)

        self.splitter.addWidget(self.layoutWidget)
        self.groupBoxFilter = QGroupBox(self.splitter)
        self.groupBoxFilter.setObjectName(u"groupBoxFilter")
        self.groupBoxFilter.setMaximumSize(QSize(400, 16777215))
        self.groupBoxFilter.setCheckable(True)
        self.verticalLayout_15 = QVBoxLayout(self.groupBoxFilter)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.checkBoxSpentFilter = QCheckBox(self.groupBoxFilter)
        self.checkBoxSpentFilter.setObjectName(u"checkBoxSpentFilter")

        self.verticalLayout_13.addWidget(self.checkBoxSpentFilter)

        self.checkBoxReceivedFilter = QCheckBox(self.groupBoxFilter)
        self.checkBoxReceivedFilter.setObjectName(u"checkBoxReceivedFilter")

        self.verticalLayout_13.addWidget(self.checkBoxReceivedFilter)

        self.checkBoxRangeDateFilter = QCheckBox(self.groupBoxFilter)
        self.checkBoxRangeDateFilter.setObjectName(u"checkBoxRangeDateFilter")

        self.verticalLayout_13.addWidget(self.checkBoxRangeDateFilter)


        self.horizontalLayout_9.addLayout(self.verticalLayout_13)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.comboBoxSendFilter = QComboBox(self.groupBoxFilter)
        self.comboBoxSendFilter.setObjectName(u"comboBoxSendFilter")

        self.verticalLayout_14.addWidget(self.comboBoxSendFilter)

        self.comboBoxReceiveFilter = QComboBox(self.groupBoxFilter)
        self.comboBoxReceiveFilter.setObjectName(u"comboBoxReceiveFilter")

        self.verticalLayout_14.addWidget(self.comboBoxReceiveFilter)

        self.dateEditFromFilter = QDateEdit(self.groupBoxFilter)
        self.dateEditFromFilter.setObjectName(u"dateEditFromFilter")
        self.dateEditFromFilter.setMinimumDateTime(QDateTime(QDate(2007, 12, 31), QTime(20, 0, 0)))

        self.verticalLayout_14.addWidget(self.dateEditFromFilter)


        self.horizontalLayout_9.addLayout(self.verticalLayout_14)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.spinBoxSpendFilter = QDoubleSpinBox(self.groupBoxFilter)
        self.spinBoxSpendFilter.setObjectName(u"spinBoxSpendFilter")
        self.spinBoxSpendFilter.setMinimum(0.000000000000000)
        self.spinBoxSpendFilter.setMaximum(100000000.000000000000000)

        self.verticalLayout_16.addWidget(self.spinBoxSpendFilter)

        self.spinBoxReceiveFilter = QDoubleSpinBox(self.groupBoxFilter)
        self.spinBoxReceiveFilter.setObjectName(u"spinBoxReceiveFilter")
        self.spinBoxReceiveFilter.setMinimum(0.000000000000000)
        self.spinBoxReceiveFilter.setMaximum(100000000.000000000000000)

        self.verticalLayout_16.addWidget(self.spinBoxReceiveFilter)

        self.dateEditToFilter = QDateEdit(self.groupBoxFilter)
        self.dateEditToFilter.setObjectName(u"dateEditToFilter")
        self.dateEditToFilter.setMinimumDateTime(QDateTime(QDate(2007, 12, 31), QTime(20, 0, 0)))

        self.verticalLayout_16.addWidget(self.dateEditToFilter)


        self.horizontalLayout_9.addLayout(self.verticalLayout_16)


        self.verticalLayout_15.addLayout(self.horizontalLayout_9)

        self.buttonUpdateFilter = QPushButton(self.groupBoxFilter)
        self.buttonUpdateFilter.setObjectName(u"buttonUpdateFilter")

        self.verticalLayout_15.addWidget(self.buttonUpdateFilter)

        self.verticalSpacer_8 = QSpacerItem(20, 384, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer_8)

        self.splitter.addWidget(self.groupBoxFilter)

        self.horizontalLayout_11.addWidget(self.splitter)

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
        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), "")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Crypto", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Fiat", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Days", None))
#if QT_CONFIG(tooltip)
        self.comboBoxCrypto.setToolTip(QCoreApplication.translate("MainWindow", u"Currency", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBoxFiat.setToolTip(QCoreApplication.translate("MainWindow", u"Currency", None))
#endif // QT_CONFIG(tooltip)
        self.comboBoxDays.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBoxDays.setItemText(1, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBoxDays.setItemText(2, QCoreApplication.translate("MainWindow", u"14", None))
        self.comboBoxDays.setItemText(3, QCoreApplication.translate("MainWindow", u"30", None))
        self.comboBoxDays.setItemText(4, QCoreApplication.translate("MainWindow", u"180", None))
        self.comboBoxDays.setItemText(5, QCoreApplication.translate("MainWindow", u"365", None))

        self.buttonUpdateMarketChart.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "")
        self.groupBoxTransactions.setTitle(QCoreApplication.translate("MainWindow", u"Add Transactions", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Spend", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Receive", None))
#if QT_CONFIG(tooltip)
        self.comboBoxSend.setToolTip(QCoreApplication.translate("MainWindow", u"Currency", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBoxReceive.setToolTip(QCoreApplication.translate("MainWindow", u"Currency", None))
#endif // QT_CONFIG(tooltip)
        self.spinBoxSpend.setPrefix("")
#if QT_CONFIG(tooltip)
        self.buttonAdd.setToolTip(QCoreApplication.translate("MainWindow", u"Add a transaction", None))
#endif // QT_CONFIG(tooltip)
        self.buttonAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.groupBoxFilter.setTitle(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.checkBoxSpentFilter.setText(QCoreApplication.translate("MainWindow", u"Spent", None))
        self.checkBoxReceivedFilter.setText(QCoreApplication.translate("MainWindow", u"Received", None))
#if QT_CONFIG(tooltip)
        self.checkBoxRangeDateFilter.setToolTip(QCoreApplication.translate("MainWindow", u"RangeDate from ... to ...", None))
#endif // QT_CONFIG(tooltip)
        self.checkBoxRangeDateFilter.setText(QCoreApplication.translate("MainWindow", u"RangeDate", None))
#if QT_CONFIG(tooltip)
        self.comboBoxSendFilter.setToolTip(QCoreApplication.translate("MainWindow", u"Currency", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBoxReceiveFilter.setToolTip(QCoreApplication.translate("MainWindow", u"Currency", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.dateEditFromFilter.setToolTip(QCoreApplication.translate("MainWindow", u"RangeDate from ... to ...", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.dateEditToFilter.setToolTip(QCoreApplication.translate("MainWindow", u"RangeDate from ... to ...", None))
#endif // QT_CONFIG(tooltip)
        self.buttonUpdateFilter.setText(QCoreApplication.translate("MainWindow", u"Update", None))
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


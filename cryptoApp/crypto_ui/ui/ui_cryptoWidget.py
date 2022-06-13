# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cryptoWidget.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDoubleSpinBox, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_CryptoWidget(object):
    def setupUi(self, CryptoWidget):
        if not CryptoWidget.objectName():
            CryptoWidget.setObjectName(u"CryptoWidget")
        CryptoWidget.resize(624, 120)
        self.horizontalLayout_5 = QHBoxLayout(CryptoWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.labelLogo = QLabel(CryptoWidget)
        self.labelLogo.setObjectName(u"labelLogo")
        self.labelLogo.setMinimumSize(QSize(100, 100))
        self.labelLogo.setMaximumSize(QSize(100, 100))

        self.horizontalLayout_5.addWidget(self.labelLogo)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labelName = QLabel(CryptoWidget)
        self.labelName.setObjectName(u"labelName")
        font = QFont()
        font.setFamilies([u"Liberation Sans Narrow"])
        font.setPointSize(18)
        font.setBold(True)
        self.labelName.setFont(font)

        self.horizontalLayout_3.addWidget(self.labelName)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.labelRank = QLabel(CryptoWidget)
        self.labelRank.setObjectName(u"labelRank")
        font1 = QFont()
        font1.setFamilies([u"Liberation Sans"])
        font1.setPointSize(15)
        font1.setBold(True)
        font1.setItalic(True)
        self.labelRank.setFont(font1)

        self.horizontalLayout_3.addWidget(self.labelRank)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(CryptoWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.label_2 = QLabel(CryptoWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.spinBoxAmount = QDoubleSpinBox(CryptoWidget)
        self.spinBoxAmount.setObjectName(u"spinBoxAmount")
        self.spinBoxAmount.setFrame(True)
        self.spinBoxAmount.setReadOnly(True)
        self.spinBoxAmount.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBoxAmount.setKeyboardTracking(True)
        self.spinBoxAmount.setMaximum(999999999999.000000000000000)

        self.verticalLayout.addWidget(self.spinBoxAmount)

        self.spinBoxValue = QDoubleSpinBox(CryptoWidget)
        self.spinBoxValue.setObjectName(u"spinBoxValue")
        self.spinBoxValue.setReadOnly(True)
        self.spinBoxValue.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBoxValue.setMaximum(999999999.000000000000000)

        self.verticalLayout.addWidget(self.spinBoxValue)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.horizontalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(CryptoWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_3 = QLabel(CryptoWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineEditTicker = QLineEdit(CryptoWidget)
        self.lineEditTicker.setObjectName(u"lineEditTicker")
        self.lineEditTicker.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.lineEditTicker)

        self.spinBoxCirculatingSupply = QSpinBox(CryptoWidget)
        self.spinBoxCirculatingSupply.setObjectName(u"spinBoxCirculatingSupply")
        self.spinBoxCirculatingSupply.setReadOnly(True)
        self.spinBoxCirculatingSupply.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBoxCirculatingSupply.setMaximum(999999999)

        self.verticalLayout_2.addWidget(self.spinBoxCirculatingSupply)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)


        self.retranslateUi(CryptoWidget)

        QMetaObject.connectSlotsByName(CryptoWidget)
    # setupUi

    def retranslateUi(self, CryptoWidget):
        CryptoWidget.setWindowTitle(QCoreApplication.translate("CryptoWidget", u"Form", None))
        self.labelLogo.setText("")
        self.labelName.setText(QCoreApplication.translate("CryptoWidget", u"Crypto name", None))
        self.labelRank.setText(QCoreApplication.translate("CryptoWidget", u"#rank", None))
        self.label.setText(QCoreApplication.translate("CryptoWidget", u"Amount", None))
        self.label_2.setText(QCoreApplication.translate("CryptoWidget", u"Value", None))
        self.label_4.setText(QCoreApplication.translate("CryptoWidget", u"Ticker", None))
        self.label_3.setText(QCoreApplication.translate("CryptoWidget", u"Circulating supply", None))
    # retranslateUi


from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPixmap

from crypto_core.objects import Currency
from ..ui import Ui_CryptoWidget

from ressources import icons_rc


class CryptoWidget(QWidget, Ui_CryptoWidget):
    """A widget to display informations on an owned currency."""

    def __init__(self, currency: Currency, amount: float, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.currency = currency
        self.amount = amount
        self.init_widget()

    def init_widget(self):
        """Initialize widget content."""
        self.labelName.setText(self.currency.name)
        self.labelRank.setText(
            f"#{self.currency.rank}" if self.currency.rank else '#Unknow')
        self.spinBoxAmount.setValue(self.amount)
        self.spinBoxAmount.setSuffix(" " + self.currency.ticker.upper())
        self.spinBoxValue.setValue(self.currency.price)
        self.spinBoxValue.setSuffix(" €")
        self.spinBoxCirculatingSupply.setValue(self.currency.circulating_supply // 1e6)
        self.spinBoxCirculatingSupply.setSuffix(" M")
        self.lineEditTicker.setText(self.currency.ticker)
        self.labelLogo.setPixmap(QPixmap(":/finance/bitcoin-black.svg"))


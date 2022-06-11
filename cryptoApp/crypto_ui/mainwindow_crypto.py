from .ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Slot, Qt
from crypto_core.objects import Portfolio, Currency, Cryptocurrency, Transaction
from .models import TransactionTableModel
from .widgets import CryptoWidget
from crypto_core.db import CryptoDatabase
from utils.hashstring import hash_string
from datetime import datetime, timedelta


class MainWindowCrypto(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = CryptoDatabase.create_connection()
        self.init_login_page()
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.portfolio = None
        self.send_amount = 0
        self.receive_amount = 0

    def init_login_page(self):
        self.comboBoxPortfolio.clear()
        self.portfolios = Portfolio.get_all_portfolios(self.db)
        self.comboBoxPortfolio.addItems([portfolio.name for portfolio in self.portfolios])
        self.buttonDelPortfolio.setEnabled(len(self.portfolios) > 0)
        self.buttonLogin.setEnabled(len(self.portfolios) > 0)
        self.buttonAdd.setEnabled(True)

    def init_model_transaction(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        #Informations des transactions sur 30 jours
        self.model_transaction = TransactionTableModel(self.portfolio.get_transactions(self.db, start_date, end_date))
        self.treeView.setModel(self.model_transaction)

    def init_tab_transaction(self):
        self.init_model_transaction()

    def init_comboBox_currency(self):
        self.currencies = list(Currency.CURRENCIES.values()) + list(Cryptocurrency.CRYPTOCURRENCIES.values())
        currencies_name = ["Other"] + [currency.name for currency in self.currencies]
        self.comboBoxSend.addItems(currencies_name)
        self.comboBoxReceive.addItems(currencies_name)
        self.comboBoxSendFilter.addItems(currencies_name)
        self.comboBoxReceiveFilter.addItems(currencies_name)

    def init_spinBox_line_edit(self):
        self.send_amount = self.spinBoxSpend.value()
        self.receive_amount = self.spinBoxReceive.value()

    def init_list_currencies(self):
        self.widgets_currencies = [
            CryptoWidget(currency, amount)
            for currency, amount in self.portfolio.cryptocurrencies.items()
        ]
        self.listWidget_fav.addItems(self.widgets_currencies)

    @Slot(int)
    def on_comboBoxSend_currentIndexChanged(self, index: int):
        if index == 0:
            self.lineEditSend.setEnabled(True)
            self.lineEditSend.setText("")
        else:
            self.lineEditSend.setText(self.currencies[index - 1].name)
            self.lineEditSend.setEnabled(False)

    @Slot(int)
    def on_comboBoxReceive_currentIndexChanged(self, index: int):
        if index == 0:
            self.lineEditReceive.setEnabled(True)
            self.lineEditReceive.setText("")
        else:
            self.lineEditReceive.setText(self.currencies[index - 1].name)
            self.lineEditReceive.setEnabled(False)

    @Slot()
    def on_buttonLogin_clicked(self):
        portfolio = self.portfolios[self.comboBoxPortfolio.currentIndex()]
        if portfolio.password == hash_string(self.lineEditPw.text()):
            self.portfolio = portfolio
            self.portfolio.load_currencies(self.db)
            self.portfolio_chart.set_portfolio(self.portfolio,
                                               title="Cryptomonaies possédées")
            self.init_tab_transaction()
            self.init_comboBox_currency()
            self.init_list_currencies()
            self.stackedWidget.setCurrentIndex(0)
            print("Login Succesfull")

    @Slot()
    def on_buttonNewPortfolio_clicked(self):
        self.stackedWidget.setCurrentIndex(2)
        print("New Portfolio Created !")

    @Slot(int)  
    def on_stackedWidget_currentChanged(self, index):
        print("Curent Page", index)

    @Slot()
    def on_buttonOkNp_clicked(self):
        name = self.lineEditNewName.text().strip()
        password = hash_string(self.lineEditNewName.text().strip())
        Portfolio.new_portfolio(name, password, self.db)
        self.lineEditNewName.setText("")
        self.lineEditNewPw.setText("")
        self.stackedWidget.setCurrentIndex(1)
        self.init_login_page()

    @Slot()
    def on_buttonCancelNp_clicked(self):
        self.lineEditNewName.setText("")
        self.stackedWidget.setCurrentIndex(1)

    @Slot()
    def on_buttonDelPortfolio_clicked(self):
        result = QMessageBox.warning(self, "Delete Portfolio?",
                                     "Your portfolio is about to get deleted, do you want to continue?",
                                      buttons = QMessageBox.Ok | QMessageBox.Cancel,
                                      defaultButton = QMessageBox.Cancel)
        if result == QMessageBox.Ok:
            portfolio = self.portfolios[self.comboBoxPortfolio.currentIndex()]
            portfolio.delete(self.db)
            self.init_login_page()

    @Slot()
    def on_buttonAdd_clicked(self):
        self.init_spinBox_line_edit()
        if self.comboBoxSend.currentIndex() == 0:
            currency_send = Cryptocurrency.from_api(self.lineEditSend.text().strip().lower())
        else:
            currency_send = self.currencies[self.comboBoxSend.currentIndex() - 1]
        if self.comboBoxReceive.currentIndex() == 0:
            currency_receive = Cryptocurrency.from_api(self.lineEditReceive.text().strip().lower())
        else:
            currency_receive = self.currencies[self.comboBoxReceive.currentIndex() - 1]
        send_tuple = (currency_send, self.send_amount)
        receive_tuple = (currency_receive, self.receive_amount)
        self.portfolio.add_transaction(send=send_tuple,
                                       received=receive_tuple,
                                       database=self.db)
        self.comboBoxSend.setCurrentIndex(0)
        self.comboBoxReceive.setCurrentIndex(0)
        self.lineEditSend.setText("")
        self.lineEditReceive.setText("")
        self.spinBoxSpend.setValue(0)
        self.spinBoxReceive.setValue(0)
        self.init_model_transaction()

    def keyPressEvent(self, event):
        print(event.key() == Qt.Key_Space)
        if event.key() == Qt.Key_Space and self.stackedWidget.currentIndex() == 1:
            self.on_buttonLogin_clicked()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget
    import sys

    app = QApplication(sys.argv)
    w = MainWindowCrypto()
    w.show()
    app.exec()

from .ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import Slot
from crypto_core.objects import Portfolio, Cryptocurrency, Transaction
from .models import TransactionTableModel
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


    def init_tab_transaction(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        #Informations des transactions sur 30 jours
        self.model_transaction = TransactionTableModel(self.portfolio.get_transactions(self.db, start_date, end_date))
        self.treeView.setModel(self.model_transaction)

    def init_comboBox_currency(self):
        currencies = [currency.name for currency in Cryptocurrency.CRYPTOCURRENCIES.values()]
        self.comboBoxSend.addItems(currencies)
        self.comboBoxReceive.addItems(currencies)
        self.comboBoxSendFilter.addItems(currencies)
        self.comboBoxReceiveFilter.addItems(currencies)

    def init_spinBox_line_edit(self):
        self.send_amount = self.lineEditSend.text().strip()
        self.receive_amount = self.lineEditReceive.text().strip()


    @Slot()
    def on_buttonLogin_clicked(self):
        portfolio = self.portfolios[self.comboBoxPortfolio.currentIndex()]
        if portfolio.password == hash_string(self.lineEditPw.text()):
            self.portfolio = portfolio
            self.portfolio_chart.set_portfolio(self.portfolio)
            self.init_tab_transaction()
            self.init_comboBox_currency()
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
        send_tuple = tuple[self.comboBoxSend.currentText(), self.send_amount]
        receive_tuple = tuple[self.comboBoxReceive.currentText(), self.receive_amount]
        Transaction.new_transaction(send_tuple, receive_tuple, datetime.now(), 1, CryptoDatabase)

    




if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget
    import sys

    app = QApplication(sys.argv)
    w = MainWindowCrypto()
    w.show()
    app.exec()
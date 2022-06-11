from .ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot
from crypto_core.objects import Portfolio
from crypto_core.db import CryptoDatabase
from utils.hashstring import hash_string

class MainWindowCrypto(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = CryptoDatabase.create_connection()
        self.init_login_page()
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.portfolio = None

    def init_login_page(self):
        self.comboBoxPortfolio.clear()
        self.portfolios = Portfolio.get_all_portfolios(self.db)
        self.comboBoxPortfolio.addItems([portfolio.name for portfolio in self.portfolios])



    @Slot()
    def on_buttonLogin_clicked(self):
        portfolio = self.portfolios[self.comboBoxPortfolio.currentIndex()]
        if portfolio.password == hash_string(self.lineEditPw.text()):
            self.portfolio = portfolio
            self.portfolio_chart.set_portfolio(self.portfolio)
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


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget
    import sys

    app = QApplication(sys.argv)
    w = MainWindowCrypto()
    w.show()
    app.exec()
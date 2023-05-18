import logging
from .ui import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QIcon
from PySide6.QtCharts import QChart, QLineSeries, QDateTimeAxis, QValueAxis
from crypto_core.objects import Portfolio, Currency, Cryptocurrency, Transaction
from .models import TransactionTableModel
from .widgets import CryptoWidget
from crypto_core.db import CryptoDatabase
from crypto_core import errors, crypto_api
from utils.hashstring import hash_string
from utils import new_logger
from datetime import datetime, timedelta
from ressources import icons_rc


class MainWindowCrypto(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.logger = new_logger("Mainwindow", level=logging.DEBUG)
        self.logger.debug("Initialization of window...")
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/finance/bitcoin-black.svg"))
        try:
            crypto_api.ping()
        except errors.ApiConnectionError:
            self.logger.warning("ApiConnectionError raised")
            QMessageBox.critical(self,
                                 "Connection error",
                                 "Can't connect to the API, check your internet connection.")
        self.db = CryptoDatabase.create_connection()
        self.init_login_page()
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        self.portfolio = None
        self.send_amount = 0
        self.receive_amount = 0
        self.market_chart_days= 30
        try:
            self.market_chart_crypto = Cryptocurrency.from_db('bitcoin', self.db)
        except errors.CurrencyDbNotFound:
            self.market_chart_crypto = None
        self.market_chart_fiat = Currency.CURRENCIES['euro']
        self.logger.debug("Mainwindow initialized")

    def init_login_page(self):
        self.logger.debug("Initialization of login page...")
        self.comboBoxPortfolio.clear()
        self.portfolios = Portfolio.get_all_portfolios(self.db)
        self.comboBoxPortfolio.addItems([portfolio.name for portfolio in self.portfolios])
        self.buttonDelPortfolio.setEnabled(len(self.portfolios) > 0)
        self.buttonLogin.setEnabled(len(self.portfolios) > 0)

    def init_model_transaction(self):
        self.logger.debug("Initialization of model transaction")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        #Informations des transactions sur 30 jours
        self.model_transaction = TransactionTableModel(self.portfolio.get_transactions(self.db, start_date, end_date))
        self.treeView.setModel(self.model_transaction)

    def init_tab_transaction(self):
        self.logger.debug("Initialization of tab transaction")
        self.init_model_transaction()
        self.buttonAdd.setEnabled(False)
        self.buttonUpdateTransaction.setEnabled(False)

    def init_comboBox_currency(self):
        self.logger.debug("Initialization of comboBox_currency")
        self.currencies = list(Currency.CURRENCIES.values()) + list(Cryptocurrency.CRYPTOCURRENCIES.values())
        currencies_name = [currency.name for currency in self.currencies]
        self.comboBoxSend.addItems(["Other"] + currencies_name)
        self.comboBoxReceive.addItems(["Other"] + currencies_name)
        self.comboBoxSendFilter.addItems(currencies_name)
        self.comboBoxReceiveFilter.addItems(currencies_name)

    def init_spinBox_line_edit(self):
        self.send_amount = self.spinBoxSpend.value()
        self.receive_amount = self.spinBoxReceive.value()

    def init_list_currencies(self):
        self.logger.debug("Initialization of the listWidget with currencies of portfolio")
        for currency, amount in sorted(self.portfolio.cryptocurrencies.items(), key=lambda item: item[0].rank):
            item = QListWidgetItem(self.listWidget_fav)
            crypto_widget = CryptoWidget(currency, amount, self.listWidget_fav)
            item.setSizeHint(crypto_widget.sizeHint())
            self.listWidget_fav.setItemWidget(item, crypto_widget)

    def init_top10_crypto(self):
        currencies = Cryptocurrency.get_top_coins_market(Currency.CURRENCIES['dollar'])
        for currency in currencies:
            crypto_widget = CryptoWidget(currency, 0, self.listWidget_top10)
            item = QListWidgetItem(self.listWidget_top10)
            item.setSizeHint(crypto_widget.sizeHint())
            self.listWidget_top10.setItemWidget(item, crypto_widget)


    def init_tab_market_chart(self):
        self.logger.debug("Initialization of the tab market_chart")
        try:
            self.init_market_chart()
        except errors.ApiConnectionError:
            pass
        self.cryptocurrencies = list(Cryptocurrency.CRYPTOCURRENCIES.values())
        self.fiatcurrencies = list(Currency.CURRENCIES.values())
        self.comboBoxCrypto.clear()
        self.comboBoxFiat.clear()
        self.comboBoxCrypto.addItems(["Other"] + [c.name for c in self.cryptocurrencies])
        self.comboBoxFiat.addItems(["Other"] + [c.name for c in self.fiatcurrencies])
        self.buttonUpdateMarketChart.setEnabled(False)

    def init_market_chart(self):
        self.logger.debug("Initialization of the market chart")
        if self.market_chart_crypto:
            data = self.market_chart_crypto.get_market_chart(
                    self.market_chart_fiat, self.market_chart_days)
            series = QLineSeries(name=self.market_chart_crypto.name)
            for x, y in zip(data[:, 0], data[:, 1]):
                series.append(x, y)
            x_axis = QDateTimeAxis()
            x_axis.setFormat("dd/MM/yyyy h:mm")
            y_axis = QValueAxis()
            chart = QChart()
            chart.addSeries(series)
            chart.setAxisX(x_axis, series)
            chart.setAxisY(y_axis, series)
            self.graphicsView.setChart(chart)

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

    @Slot(str)
    def on_lineEditSend_textChanged(self, text: str):
        if text.strip() and self.lineEditReceive.text().strip():
            self.buttonAdd.setEnabled(True)
        else:
            self.buttonAdd.setEnabled(False)

    @Slot(str)
    def on_lineEditReceive_textChanged(self, text: str):
        if text.strip() and self.lineEditSend.text().strip():
            self.buttonAdd.setEnabled(True)
        else:
            self.buttonAdd.setEnabled(False)

    @Slot()
    def on_buttonLogin_clicked(self):
        self.logger.debug("Login button clicked")
        portfolio = self.portfolios[self.comboBoxPortfolio.currentIndex()]
        if portfolio.password == hash_string(self.lineEditPw.text()):
            self.logger.info("Login successfully")
            self.portfolio = portfolio
            self.portfolio.load_currencies(self.db)
            self.portfolio_chart.set_portfolio(self.portfolio,
                                               title="Cryptomonaies possédées")
            self.init_tab_market_chart()
            self.init_tab_transaction()
            self.init_comboBox_currency()
            self.init_list_currencies()
            self.init_top10_crypto()
            self.stackedWidget.setCurrentIndex(0)

        else:
            self.logger.info("Login failed")
            QMessageBox.critical(self, "Bad password", "This password does not correspond to this portfolio")

    @Slot()
    def on_buttonNewPortfolio_clicked(self):
        self.stackedWidget.setCurrentIndex(2)

    @Slot()
    def on_buttonOkNp_clicked(self):
        try:
            name = self.lineEditNewName.text().strip()
            password = hash_string(self.lineEditNewPw.text().strip())
            Portfolio.new_portfolio(name, password, self.db)
            self.stackedWidget.setCurrentIndex(1)
            self.init_login_page()
            self.logger.info("Portfolio created with success")
        except errors.PortfolioAlreadyExists:
            self.logger.warning("Try to create a portfolio with a portfolio name existing")
            QMessageBox.critical(self,
                                 "Portfolio ALready exist",
                                 "A portfolio with the same name already exists!")
        finally:
            self.lineEditNewName.setText("")
            self.lineEditNewPw.setText("")
    @Slot()
    def on_buttonCancelNp_clicked(self):
        self.logger.debug("Creation of portfolio cancelled")
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
            self.logger.info("Portfolio deleted")

    @Slot()
    def on_buttonUpdateMarketChart_clicked(self):
        self.logger.debug("Update market chart")
        if self.comboBoxFiat.currentIndex() == 0:
            fiat = self.lineEditFiat.text().strip().lower()
            self.market_chart_fiat = Currency(id_=fiat, name=fiat.capitalize(), ticker=fiat)
        else:
            self.market_chart_fiat = self.fiatcurrencies[self.comboBoxFiat.currentIndex() - 1]
        
        if self.comboBoxCrypto.currentIndex() == 0:
            try:
                self.market_chart_crypto = Cryptocurrency.from_api(
                        self.lineEditCrypto.text().strip().lower(),
                        self.market_chart_fiat
                )

            except errors.CurrencyApiNotFound:
                self.logger.info(f"CurrencyApiNotFound: {self.lineEditCrypto.text().strip().lower()}")
                QMessageBox.critical(self,
                                     "Currency not found",
                                     f"The cryptocurrency with id: '{self.lineEditCrypto.text().strip().lower()}' "
                                     "was not found in CoinGecko API.")
                self.lineEditCrypto.setText("")
                return
            except errors.ApiConnectionError:
                self.logger.info("ApiConnectionError")
                QMessageBox.critical(self,
                                     "Connection Error",
                                     "Can't connect to the API, please, check your intenet connection.")
                return
        else:
            self.market_chart_crypto = self.cryptocurrencies[self.comboBoxCrypto.currentIndex() - 1]


        self.market_chart_days = int(self.comboBoxDays.currentText().strip())
        try:
            self.init_market_chart()

        except errors.ApiCurrencyNotFound:
            self.logger.info(f"ApiCurrencyNotFound: {self.lineEditFiat.text().strip().lower()}")
            QMessageBox.critical(self,
                                 "Fiat Currency not found",
                                 f"The fiat currency with id: '{self.lineEditFiat.text().strip().lower()}' "
                                 "was not found in CoinGecko API.")
            self.lineEditFiat.setText("")
            return

        except errors.ApiConnectionError:
            self.logger.info("ApiConnectionError")
            QMessageBox.critical(self,
                                 "Connection Error",
                                 "Can't connect to the API, please, check your intenet connection.")

    @Slot(int)
    def on_comboBoxCrypto_currentIndexChanged(self, index: int):
        if index == 0:
            self.lineEditCrypto.setEnabled(True)
            self.lineEditCrypto.setText("")
            self.buttonUpdateMarketChart.setEnabled(False)
        else:
            self.lineEditCrypto.setEnabled(False)
            self.lineEditCrypto.setText(self.cryptocurrencies[index - 1].name)
    
    @Slot(int)
    def on_comboBoxFiat_currentIndexChanged(self, index: int):
        if index == 0:
            self.lineEditFiat.setEnabled(True)
            self.lineEditFiat.setText("")
            self.buttonUpdateMarketChart.setEnabled(False)
        else:
            self.lineEditFiat.setEnabled(False)
            self.lineEditFiat.setText(self.fiatcurrencies[index - 1].name)

    @Slot(str)
    def on_lineEditCrypto_textChanged(self, text: str):
        if text.strip() and self.lineEditFiat.text().strip():
            self.buttonUpdateMarketChart.setEnabled(True)
        else:
            self.buttonUpdateMarketChart.setEnabled(False)
 
    @Slot(str)
    def on_lineEditFiat_textChanged(self, text: str):
        if text.strip() and self.lineEditCrypto.text().strip():
            self.buttonUpdateMarketChart.setEnabled(True)
        else:
            self.buttonUpdateMarketChart.setEnabled(False)           

    @Slot()
    def on_buttonAdd_clicked(self):
        self.logger.debug("Add transaction button clicked")
        self.init_spinBox_line_edit()
        try:
            if self.comboBoxSend.currentIndex() == 0:
                try:
                    currency_send = Cryptocurrency.from_api(
                            self.lineEditSend.text().strip().lower(), Currency.CURRENCIES['euro'])
                except errors.CurrencyApiNotFound:
                    self.logger.info("CurrencyApiNotFound: {self.lineEditSend.text().strip().lower()}")
                    QMessageBox.critical(self,
                                         "Cryptocurrency not found",
                                         f"The cryptocurrency with id: '{self.lineEditSend.text().strip().lower()}' "
                                         "was not found in CoinGecko API.")
                    self.lineEditSend.setText("")
                    return
            else:
                currency_send = self.currencies[self.comboBoxSend.currentIndex() - 1]
            if self.comboBoxReceive.currentIndex() == 0:
                try:
                    currency_receive = Cryptocurrency.from_api(
                            self.lineEditReceive.text().strip().lower(), Currency.CURRENCIES['euro'])
                except errors.CurrencyApiNotFound:
                    self.logger.info("CurrencyApiNotFound: {self.lineEditReceive.text().strip().lower()}")
                    QMessageBox.critical(self,
                                       "Cryptocurrency not found",
                                       f"The cryptocurrency with id: '{self.lineEditReceive.text().strip().lower()}' "
                                       "was not found in CoinGecko API.")
                    self.lineEditReceive.setText("")
                    return
            else:
                currency_receive = self.currencies[self.comboBoxReceive.currentIndex() - 1]
        except errors.ApiConnectionError:
            self.logger.info("ApiConnectionError")
            QMessageBox.critical(self,
                                     "Connection Error",
                                     "Can't connect to the API, please, check your intenet connection.")
            return
        send_tuple = (currency_send, self.send_amount)
        receive_tuple = (currency_receive, self.receive_amount)
        self.portfolio.add_transaction(send=send_tuple,
                                       received=receive_tuple,
                                       database=self.db)
        self.logger.debug("Transaction added")
        self.comboBoxSend.setCurrentIndex(0)
        self.comboBoxReceive.setCurrentIndex(0)
        self.lineEditSend.setText("")
        self.lineEditReceive.setText("")
        self.spinBoxSpend.setValue(0)
        self.spinBoxReceive.setValue(0)
        self.init_model_transaction()
        self.portfolio_chart.init_chart()
    
    @Slot()
    def on_buttonUpdateTransaction_clicked(self):
        self.logger.info("Update the list of transactions with the filter")
        parameters = dict()
        if self.checkBoxSpentFilter.isChecked():
            parameters['currency_send'] = self.currencies[self.comboBoxSendFilter.currentIndex()]
        if self.checkBoxReceivedFilter.isChecked():
            parameters['currency_received'] = self.currencies[self.comboBoxReceiveFilter.currentIndex()]
        if self.checkBoxRangeDateFilter.isChecked():
            parameters['range_date'] = (
                self.dateEditFromFilter.date().toPython(),
                self.dateEditToFilter.date().toPython() 
            )
        self.logger.debug(f"filter used: {parameters}")
        self.model_transaction.transactions = self.portfolio.get_transactions_filtered(self.db, **parameters)
        self.logger.debug("List of transactions updated")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and self.stackedWidget.currentIndex() == 1:
            self.on_buttonLogin_clicked()

    def closeEvent(self, event):
        if self.portfolio is not None:
            self.logger.info("Upload currencies of portfolio in database...")
            self.portfolio.upload_currencies_in_db(self.db)
        event.accept()
        self.logger.info("Mainwindow closed")


    @Slot()
    def on_checkBoxSpentFilter_stateChanged(self):
        if self.checkBoxSpentFilter.isChecked() or self.checkBoxReceivedFilter.isChecked() or self.checkBoxRangeDateFilter.isChecked():
            self.buttonUpdateTransaction.setEnabled(True)
        else:
            self.buttonUpdateTransaction.setEnabled(False)

    @Slot()
    def on_checkBoxReceivedFilter_stateChanged(self):
        if self.checkBoxSpentFilter.isChecked() or self.checkBoxReceivedFilter.isChecked() or self.checkBoxRangeDateFilter.isChecked():
            self.buttonUpdateTransaction.setEnabled(True)
        else:
            self.buttonUpdateTransaction.setEnabled(False)

    @Slot()
    def on_checkBoxRangeDateFilter_stateChanged(self):
        if self.checkBoxSpentFilter.isChecked() or self.checkBoxReceivedFilter.isChecked() or self.checkBoxRangeDateFilter.isChecked():
            self.buttonUpdateTransaction.setEnabled(True)
        else:
            self.buttonUpdateTransaction.setEnabled(False)

    @Slot()
    def on_groupBoxFilter_stateChanged(self):
        if self.groupBoxFilter.isChecked == False:
            self.checkBoxSpentFilter.setEnabled(False)
            self.checkBoxReceivedFilter.setEnabled(False)
            self.checkBoxRangeDateFilter.setEnabled(False)

    
    

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QWidget
    import sys

    app = QApplication(sys.argv)
    w = MainWindowCrypto()
    w.show()
    app.exec()

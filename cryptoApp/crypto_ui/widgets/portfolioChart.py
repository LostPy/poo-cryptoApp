from PySide6.QtCharts import QChartView, QChart, QPieSeries, QPieSlice
from PySide6.QtGui import QPainter

from crypto_core.objects import Portofolio


class PortfolioChart(QChartView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.portfolio = None
      

    def init_chart(self):
        chart = QChart()
        serie = QPieSeries()
        serie.append([
            QPieSlice(currency.name, amount * currency.price)
            for currency, amount in self.portfolio.currencies.items()
        ])  # Create slices with currency's name as label and total value as value

        for pieslice in serie.slices():
            # must be executed after add all slices to compute the good percent value
            pieslice.setLabel(f"{pieslice.label()} {pieslice.percentage():.2%}")
        serie.setLabelsPosition(QPieSlice.LabelOutside)
        serie.setLabelsVisible(True)
        chart.addSeries(serie)
        chart.legend().hide()
        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)  # to don't have pixelized curves

    def set_portfolio(self, portfolio: Portofolio, /,
                 title: str = "",
                 theme=QChart.ChartThemeLight):
        self.portfolio = portfolio
        self.init_chart()
        self.chart().setTitle(title)
        self.chart().setTheme(theme)

from crypto_common.crypto_api import *
import matplotlib.pyplot as plt
from datetime import datetime

market_chart = get_market_chart('bitcoin', 'usd', '3')
market_chart_by_range = get_market_chart_by_range('bitcoin', 'usd', '1651356000', '1652345026') # du 1er mai à mnt (12/05)
plt.subplot(2, 1, 1)
plt.plot(market_chart['date'], market_chart['price'])
plt.grid()
plt.subplot(2, 1, 2)
plt.plot(market_chart_by_range['date'], market_chart_by_range['price'])
plt.grid()
plt.show()

#print(get_trending())
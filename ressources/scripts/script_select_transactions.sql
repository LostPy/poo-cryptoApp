SELECT idTransaction, date, amountSend, amountReceived,
CurrencySend.idCurrency as idCurrencySend,
CurrencySend.name as nameSend,
CurrencySend.ticker as tickerSend,
CurrencySend.price as priceSend,
CurrencySend.circulatingSupply as circulatingSupplySend,
CurrencySend.last_update as lastUpdateSend,
CurrencySend.rank as rankSend,
CurrencySend.isCrypto as isCryptoSend,
CurrencyReceived.idCurrency as idCurrencyReceived,
CurrencyReceived.name as nameReceived,
CurrencyReceived.ticker as tickerReceived,
CurrencyReceived.price as priceReceived,
CurrencyReceived.circulatingSupply as circulatingSupplyReceived,
CurrencyReceived.last_update as lastUpdateReceived,
CurrencyReceived.rank as rankReceived,
currencyReceived.isCrypto as isCryptoReceived
FROM CryptoTransaction
INNER JOIN Currency as CurrencySend ON CryptoTransaction.currencySend=CurrencySend.idCurrency
INNER JOIN Currency as CurrencyReceived ON CryptoTransaction.currencyReceived=CurrencyReceived.idCurrency
{where}
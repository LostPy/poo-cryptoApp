CREATE TABLE Portofolio (
	idPortofolio integer PRIMARY KEY,
	name varchar(20) NOT NULL UNIQUE,
	password varchar(255) NOT NULL
);

CREATE TABLE Currency (
	idCurrency varchar(10) PRIMARY KEY,
	name varchar(10) NOT NULL,
	ticker varchar(3) NOT NULL,
	price real,
	circulatingSupply integer,
	rank integer,
	last_update timestamp,
	isCrypto boolean NOT NULL CHECK (isCrypto IN (0, 1))
);

CREATE TABLE PortofoliosCurrencies (
	portofolio integer NOT NULL,
	currency varchar(10) NOT NULL,
	amount real DEFAULT 0,
	PRIMARY KEY(portofolio, currency),
	FOREIGN KEY (portofolio) REFERENCES Portofolio(idPortofolio),
	FOREIGN KEY (currency) REFERENCES Currency(idCurrency)
);

CREATE TABLE CryptoTransaction (
	idTransaction integer PRIMARY KEY,
	date timestamp,
	amountSend real,
	amountReceived real,
	currencySend varchar(10) NOT NULL,
	currencyReceived varchar(10) NOT NULL,
	portofolio integer NOT NULL,
	FOREIGN KEY (currencySend) REFERENCES Currency(idCurrency),
	FOREIGN KEY (currencyReceived) REFERENCES Currency(idCurrency),
	FOREIGN KEY (portofolio) REFERENCES Portofolio(idPortofolio)
);


INSERT INTO Currency (idCurrency, name, ticker, isCrypto)
VALUES ('dollar', 'Dollar', 'usd', 0);

INSERT INTO Currency (idCurrency, name, ticker, isCrypto)
VALUES ('euro', 'Euro', 'eur', 0);

# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.3.0
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x05\x06\
C\
REATE TABLE Port\
ofolio (\x0a\x09idPort\
ofolio integer P\
RIMARY KEY,\x0a\x09nam\
e varchar(20) NO\
T NULL UNIQUE,\x0a\x09\
password varchar\
(255) NOT NULL\x0a)\
;\x0a\x0aCREATE TABLE \
Currency (\x0a\x09idCu\
rrency varchar(1\
0) PRIMARY KEY,\x0a\
\x09name varchar(10\
) NOT NULL,\x0a\x09tic\
ker varchar(3) N\
OT NULL,\x0a\x09price \
real,\x0a\x09circulati\
ngSupply integer\
,\x0a\x09rank integer,\
\x0a\x09last_update ti\
mestamp,\x0a\x09isCryp\
to boolean NOT N\
ULL CHECK (isCry\
pto IN (0, 1))\x0a)\
;\x0a\x0aCREATE TABLE \
PortofoliosCurre\
ncies (\x0a\x09portofo\
lio integer NOT \
NULL,\x0a\x09currency \
varchar(10) NOT \
NULL,\x0a\x09amount re\
al DEFAULT 0,\x0a\x09P\
RIMARY KEY(porto\
folio, currency)\
,\x0a\x09FOREIGN KEY (\
portofolio) REFE\
RENCES Portofoli\
o(idPortofolio),\
\x0a\x09FOREIGN KEY (c\
urrency) REFEREN\
CES Currency(idC\
urrency)\x0a);\x0a\x0aCRE\
ATE TABLE Crypto\
Transaction (\x0a\x09i\
dTransaction int\
eger PRIMARY KEY\
,\x0a\x09date timestam\
p,\x0a\x09amountSend r\
eal,\x0a\x09amountRece\
ived real,\x0a\x09curr\
encySend varchar\
(10) NOT NULL,\x0a\x09\
currencyReceived\
 varchar(10) NOT\
 NULL,\x0a\x09portofol\
io integer NOT N\
ULL,\x0a\x09FOREIGN KE\
Y (currencySend)\
 REFERENCES Curr\
ency(idCurrency)\
,\x0a\x09FOREIGN KEY (\
currencyReceived\
) REFERENCES Cur\
rency(idCurrency\
),\x0a\x09FOREIGN KEY \
(portofolio) REF\
ERENCES Portofol\
io(idPortofolio)\
\x0a);\x0a\x0a\x0aINSERT INT\
O Currency (idCu\
rrency, name, ti\
cker, isCrypto)\x0a\
VALUES ('dollar'\
, 'Dollar', 'USD\
', 0);\x0a\x0aINSERT I\
NTO Currency (id\
Currency, name, \
ticker, isCrypto\
)\x0aVALUES ('euro'\
, 'Euro', 'EUR',\
 0);\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00z|\
\x00s\
\x00q\x00l\
\x00\x07\
\x00P\xa5B\
\x00i\
\x00n\x00i\x00t\x00_\x00d\x00b\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x81-\xa2\xb1\x9b\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

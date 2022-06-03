# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.3.0
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x04\xfa\
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
real,\x0a\x09logo text\
,\x0a\x09circulatingSu\
pply integer,\x0a\x09r\
ank integer,\x0a\x09is\
Crypto boolean N\
OT NULL CHECK (i\
sCrypto IN (0, 1\
))\x0a);\x0a\x0aCREATE TA\
BLE PortofoliosC\
urrencies (\x0a\x09por\
tofolio integer \
NOT NULL,\x0a\x09curre\
ncy varchar(10) \
NOT NULL,\x0a\x09amoun\
t real DEFAULT 0\
,\x0a\x09PRIMARY KEY(p\
ortofolio, curre\
ncy),\x0a\x09FOREIGN K\
EY (portofolio) \
REFERENCES Porto\
folio(idPortofol\
io),\x0a\x09FOREIGN KE\
Y (currency) REF\
ERENCES Currency\
(idCurrency)\x0a);\x0a\
\x0aCREATE TABLE Cr\
yptoTransaction \
(\x0a\x09idTransaction\
 integer PRIMARY\
 KEY,\x0a\x09date time\
stamp,\x0a\x09amountSe\
nd real,\x0a\x09amount\
Received real,\x0a\x09\
currencySend var\
char(10) NOT NUL\
L,\x0a\x09currencyRece\
ived varchar(10)\
 NOT NULL,\x0a\x09port\
ofolio integer N\
OT NULL,\x0a\x09FOREIG\
N KEY (currencyS\
end) REFERENCES \
Currency(idCurre\
ncy),\x0a\x09FOREIGN K\
EY (currencyRece\
ived) REFERENCES\
 Currency(idCurr\
ency),\x0a\x09FOREIGN \
KEY (portofolio)\
 REFERENCES Port\
ofolio(idPortofo\
lio)\x0a);\x0a\x0a\x0aINSERT\
 INTO Currency (\
idCurrency, name\
, ticker, isCryp\
to)\x0aVALUES ('dol\
lar', 'Dollar', \
'USD', 0);\x0a\x0aINSE\
RT INTO Currency\
 (idCurrency, na\
me, ticker, isCr\
ypto)\x0aVALUES ('e\
uro', 'Euro', 'E\
UR', 0);\x0a\
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
\x00\x00\x01\x81*\xb0\x22b\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

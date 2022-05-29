# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.3.0
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x04\xf3\
C\
REATE TABLE Port\
ofolio (\x0a\x09idPort\
ofolio integer P\
RIMARY KEY,\x0a\x09nam\
e varchar(20) NO\
T NULL,\x0a\x09passwor\
d varchar(255) N\
OT NULL\x0a);\x0a\x0aCREA\
TE TABLE Currenc\
y (\x0a\x09idCurrency \
varchar(10) PRIM\
ARY KEY,\x0a\x09name v\
archar(10) NOT N\
ULL,\x0a\x09ticker var\
char(3) NOT NULL\
,\x0a\x09price real,\x0a\x09\
logo text,\x0a\x09circ\
ulatingSupply in\
teger,\x0a\x09rank int\
eger,\x0a\x09isCrypto \
boolean NOT NULL\
 CHECK (isCrypto\
 IN (0, 1))\x0a);\x0a\x0a\
CREATE TABLE Por\
tofoliosCurrenci\
es (\x0a\x09portofolio\
 integer NOT NUL\
L,\x0a\x09currency var\
char(10) NOT NUL\
L,\x0a\x09amount real \
DEFAULT 0,\x0a\x09PRIM\
ARY KEY(portofol\
io, currency),\x0a\x09\
FOREIGN KEY (por\
tofolio) REFEREN\
CES Portofolio(i\
dPortofolio),\x0a\x09F\
OREIGN KEY (curr\
ency) REFERENCES\
 Currency(idCurr\
ency)\x0a);\x0a\x0aCREATE\
 TABLE CryptoTra\
nsaction (\x0a\x09idTr\
ansaction intege\
r PRIMARY KEY,\x0a\x09\
date timestamp,\x0a\
\x09amountSend real\
,\x0a\x09amountReceive\
d real,\x0a\x09currenc\
ySend varchar(10\
) NOT NULL,\x0a\x09cur\
rencyReceived va\
rchar(10) NOT NU\
LL,\x0a\x09portofolio \
integer NOT NULL\
,\x0a\x09FOREIGN KEY (\
currencySend) RE\
FERENCES Currenc\
y(idCurrency),\x0a\x09\
FOREIGN KEY (cur\
rencyReceived) R\
EFERENCES Curren\
cy(idCurrency),\x0a\
\x09FOREIGN KEY (po\
rtofolio) REFERE\
NCES Portofolio(\
idPortofolio)\x0a);\
\x0a\x0a\x0aINSERT INTO C\
urrency (idCurre\
ncy, name, ticke\
r, isCrypto)\x0aVAL\
UES ('dollar', '\
Dollar', 'USD', \
0);\x0a\x0aINSERT INTO\
 Currency (idCur\
rency, name, tic\
ker, isCrypto)\x0aV\
ALUES ('euro', '\
Euro', 'EUR', 0)\
;\x0a\
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
\x00\x00\x01\x81\x0f\xb2&\x82\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

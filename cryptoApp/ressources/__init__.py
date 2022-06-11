"""Package with all module ressources generate by pyside6-rcc program.
These modules are generated from a QRC file (ressources folder).

To create a ressource file:

 1. Create a QRC file in `ressources` folder:

```
touch ressources/my_ressources.qrc
```

 2. Complete this ressource file with a similar code:

```xml
<!DOCTYPE RCC>
<RCC version="1.0">
    <qresource prefix="sql">
        <file alias="init_db">scripts/script_init_db.sql</file>
    </qresource>
</RCC>
```

 3. Compile this file in a Python module to use ressources in the application

```
pyside6-rcc ressources/my_ressources.qrc > cryptoApp/ressources/my_ressources_rc.py
```
"""

from . import scripts_rc

# Ressources Qt

Les ressources Qt permettent d'ajouter des ressources qui sont compilés avec le programme afin de limité les erreurs dû au système de fichier (notamment d'accès aux fichiers, et d'emplacement des fichiers).

Les ressources utilisés par l'application sont placés dans ce dossier (dans des sous dossier où non).

## Icons

Les icons proviennent de [RemixIcon](https://remixicon.com/) et sont sous la license Apache V2.

## Déclarer les ressources pour Qt

Pour déclarer les ressources utilisées par l'application Qt, il est nécessaire d'utiliser un fichier QRC (Qt Ressource) qui aura ce format :

```xml
<!DOCTYPE RCC>
<RCC version="1.0">
    <qresource prefix="icons">
        <file alias="logo-32.png">icons/logo-32.png</file>
        <file alias="logo-64.png">icons/logo-64.png</file>
        <file alias="other.png">icons/other.png</file>
    </qresource>
</RCC>
```

## Compiler les ressources

Pour compiler les ressources pour les utiliser avec PySide6, il faut utiliser le programme `pyside6-rcc` fournit avec le package.

En admettant que le fichier QRC a pour path relatif à la racine du projet `ressources/icons.qrc` 
et qu'on souhaite mettre le fichier python généré dans `src/ressources/icons_rc.py`

```
pyside6-rcc ressources/icons.qrc > src/ressources/icons_rc.py
```

## Utiliser les ressources dans l'application

Pour utiliser ces ressources il faut importer le module avec les ressources dans celui où l'on souhaite utiliser une ressource et utiliser le prefix et l'alias de la ressource spécifié dans le fichier QRC comme ceci : `:/{prefix}/{alias}`.

Par exemple :

```python
from PySide6.QtGui import QIcon
from ressources import icons_rc

QIcon(":/icons/logo-32.png")
```

# Boggler
Generate a 4x4 board of letters, then find all English words within sequences of adjacent letters like the game Boggle.

Example Generated Board:

```
U E F P 
D H W X 
L O U Y 
V L O L 
```

Words Found for Generated Board:

```
DEF
DEW
DEWY
DOLL
DOW
DUE
DUH
FED
FEUD
FEW
HEW
HOD
HOLD
HOV
HOW
HOWE
HUD
HUE
HUED
HULL
LODE
LOLL
LOO
LOU
LOW
LOWE
LOWED
LULL
LUX
ODE
OLD
OOH
OOHED
OWE
OWED
UHF
VOL
VOW
VOWED
WED
WHO
WOLD
WOO
WOOL
YOU
```


## Run 

Requires PyEnchant, which contains the English dictionary used to determine words: https://pyenchant.github.io/pyenchant/install.html

Once PyEnchant is installed, simply run the script without arguments

```python3 boggler.py```

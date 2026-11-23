## Before and After Table

|**Measure**|**Before (legacy\_fees.py)**|**After (fees.py)**|
|-|-|-|
|Ruff issues (total)|16|0|
|Highest cyclomatic complexity|9 (calc)|4 (tuition\_fee)|
|Arguments of the main function|6|5|
|Pylint score (/10)|4.86|10|
|Tests passing|0 (no tests)|6|

## 

## Pairing Reflection

Switching between driver and navigator helped us catch small mistakes early before they turned into bigger bugs. As the navigator, it was much easier to spot unclear names, edge cases, and missing tests while my partner focused on typing. Refactoring in small steps and running pytest after each change felt a bit slower at first, but it made the changes much safer because we knew right away if anything broke.


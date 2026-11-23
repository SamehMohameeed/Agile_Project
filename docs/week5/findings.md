## Findings Table



|Rule|Count|Smell|Refactoring|
|-|-|-|-|
|F401|2|Dead code (unused imports)|Delete the imports|
|PLR2004|6|Magic numbers|Replace with named constants or an enum|
|C901|1|Complex structure|Replace the if/elif chain with a rate table|
|PLR0913|1|Too many arguments|Remove the unused argument y and clean up the parameters|
|ARG001|1|Dead code (unused argument)|Delete y|
|B006|1|Mutable default argument|Use an immutable default like extras=() or None|
|E711/E712|2|Bad None / True comparisons|Use if summer: and default disc to `0`|
|F841|1|Dead code (unused variable)|Delete tmp|
|N802|1|Invalid function name|Rename ProcessAll to process\_all|

## 

## Extra Smells Ruff Missed

* Unclear names: single-letter parameters like d, t, y, and s don't explain what they hold, and calc is too vague.
* Duplicated code: ProcessAll repeats almost the exact same calc call for type 1 and type 2 instead of just passing st\["type"].
* Mixed responsibilities: report handles both calculating the fee and printing it instead of returning the text.

## 

## Hidden Bug in ProcessAll

A scholarship student (type 3) is supposed to pay 0, but ProcessAll only has if checks for type 1 and type 2. Since neither if runs for Omar, fee never changes and just keeps Sara's fee (1050) from the previous loop, so it prints `Omar 1050`. If Omar were first in the list, fee wouldn't exist yet and Python would crash with an UnboundLocalError.


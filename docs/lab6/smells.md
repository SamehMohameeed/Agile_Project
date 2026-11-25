# Code Smells — `legacy_invoice.py` (Task C1)

| Smell | Where | Principle it breaks |
| --- | --- | --- |
| Long `if/elif` chain on `kind` | Loop body (`if kind == ...`) and after loop (`if kind == "international"`) | **OCP**: adding a new student type requires editing `make_invoice` in two places |
| Mixed responsibilities (calculation, formatting, disk I/O, and printing) | Entire `make_invoice` function (`open`, `write`, `print`, and fee calculation) | **SRP & DIP**: multiple reasons to change (SRP), and the function depends directly on concrete disk/stdout I/O instead of an injected writer abstraction (DIP) |
| Magic numbers (`1200`, `0.5`, `2000`, `5000`) and duplicated base rate | Inside the `if/elif` branches and service-fee check | **Readability / DRY**: unnamed constants hide intent and duplicate `1200` across regular and scholarship branches |
| Feature Envy / unnecessary per-course loop | `for code in student.courses: h = student.courses[code]` | **Information Expert / Encapsulation**: `make_invoice` accesses `student.courses` directly instead of using `student.total_hours` |
| File opened manually without `with` | `f = open(...); f.write(text); f.close()` | **Resource safety**: if `f.write(text)` raises an exception, `f.close()` is skipped and the file handle leaks |

## How They Were Addressed in `invoice.py`

- **OCP (`if/elif` chain on `kind`)**: Replaced with the `FeePolicy` strategy hierarchy (`RegularPolicy`, `DiscountedPolicy`, `ScholarshipPolicy`, `SiblingPolicy`, `InternationalPolicy`) and the `POLICIES` lookup dictionary, so adding `"sibling"` required only adding `SiblingPolicy` and registering `"sibling"` in `POLICIES` without modifying `make_invoice`.
- **SRP & DIP (mixed responsibilities and concrete I/O)**: Separated fee calculation (`FeePolicy.fee`), formatting/orchestration (`make_invoice`), and file persistence (`FileWriter`), with an optional `writer` parameter on `make_invoice` for dependency injection (e.g., `FakeWriter` in `tests/test_invoice_characterization.py`).
- **Readability / DRY (magic numbers and duplicated base rate)**: Extracted named constants (`FEE_PER_HOUR`, `RATE`, `DISCOUNT`, `SERVICE_FEE`) and shared regular-rate calculation via `DiscountedPolicy(RegularPolicy)`.
- **Information Expert / Encapsulation (per-course loop)**: `make_invoice` reads `student.total_hours` directly instead of iterating over `student.courses`.
- **Resource safety (`open`/`close`)**: `FileWriter.write` opens the file with `with open(...)` so the file handle closes automatically even if writing raises an exception.

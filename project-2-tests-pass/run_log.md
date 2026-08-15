# Run log — Project 2 (tests-pass)

Checker command: `python3 -m unittest test_calc -v`
Cap: 6 tries. Stop rule: checker exit code == 0 (not agent opinion).

## Try 1/6 — FAIL (exit 1)
3 failures:
- `test_add`: `add(2, 3)` returned `-1`, expected `5` → bug: `a - b` instead of `a + b`
- `test_is_even`: `is_even(4)` returned `False` → bug: inverted condition (`% 2 == 1`)
- `test_factorial`: `factorial(5)` returned `24`, expected `120` → bug: `range(1, n)` off-by-one

Maker action: fixed all three functions in `calc.py` based on the failure
output above.

## Try 2/6 — PASS (exit 0)
```
test_add ... ok
test_is_even ... ok
test_factorial ... ok
Ran 3 tests in 0.000s
OK
```

## Result
Loop stopped at **try 2 of 6** because the checker (`unittest`'s own exit
code) reported success — not because the agent decided it looked done, and
not because it hit the 6-try cap. This satisfies the "Done when" criteria.

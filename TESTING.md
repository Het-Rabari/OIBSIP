# Test Evidence

Checks were run locally on 2026-11-11 with Python 3.12.14.

## Automated checks

Command:

    python -m unittest discover -s . -p "test_*.py" -v

Result: 16 tests ran and passed.

- BMI Calculator: 5 tests passed, covering the calculation, adult category boundaries, and invalid values.
- Random Password Generator: 6 tests passed, covering length, enabled character groups, and invalid options.
- Basic Weather App: 5 tests passed, covering a simulated successful response, an empty place, no matching place, a network failure, and invalid JSON.

The weather tests use simulated responses; they do not contact the live service. No password value is printed or stored by the tests.

## Command-line smoke checks

- The BMI command was run with sample inputs of 70 kg and 175 cm. It displayed BMI 22.9 and the “Normal weight” adult category.
- The password generator help command displayed the available options. A generated password was not captured as test evidence.

No screenshots, demo videos, peer evaluations, or internship completion claims are included.

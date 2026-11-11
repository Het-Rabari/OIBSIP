# Random Password Generator

A command-line password generator that uses Python's cryptographic random source. It includes at least one character from every selected character group, then securely shuffles the result.

## Run

From this folder, run:

    python password_generator.py

The default length is 16 characters. Use **python password_generator.py --help** to see options. You can choose a different length or disable lowercase letters, uppercase letters, digits, or symbols. The requested length must be at least the number of enabled groups.

The generated password is printed once and is not written to a file. Avoid sharing it or saving it in an unsecured location.

## Check

Run:

    python -m unittest -v

The tests check length, selected character groups, and invalid options. They do not print or preserve generated passwords.

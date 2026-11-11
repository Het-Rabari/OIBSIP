# Oasis Infobyte Python Projects

This repository contains three small Python command-line projects:

1. BMI Calculator
2. Random Password Generator
3. Basic Weather App

Each project has its own source file, instructions, and automated checks. The projects use only the Python standard library; the weather app needs an internet connection to query Open-Meteo.

## Run a project

Open a terminal in the project folder and use Python 3:

- BMI Calculator: **python bmi_calculator.py**
- Random Password Generator: **python password_generator.py --help**
- Basic Weather App: **python weather_app.py**

Read each project README for options and limitations. The BMI ranges are for adults and are a screening reference only, not a diagnosis. The weather app sends the entered place name to Open-Meteo to find its coordinates and current conditions.

## Check the projects

From this folder, run:

    python -m unittest discover -s . -p "test_*.py" -v

The observed test run is recorded in TESTING.md. No screenshots, demo videos, peer evaluations, or internship submissions are included.

## Review before submission

The account owner should run the projects, review the code, and be able to explain how each one works before using this material for an internship submission.

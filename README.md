# DevOps Lab Mid - Assignment Submission Portal

## Description

This project is an Assignment Submission Portal developed for DevOps Lab Mid.

Students can submit:
- Name
- Registration Number
- Assignment Title
- Submission URL


## Installation

Create virtual environment:

python -m venv venv


Activate environment:

venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


## Run Application

Start Flask application:

python app/main.py


Open browser:

http://127.0.0.1:5000


## Run Tests

Execute automated tests:

pytest


## Project Structure

app/
tests/
receiver/
reports/
.github/workflows/


## Run Receiver

Start local report receiver:

python receiver/receiver.py
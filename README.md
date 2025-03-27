# Credit Rating for Residential Mortgage-Backed Securities (RMBS)

## Overview
This project provides a robust system for calculating credit ratings for residential mortgage-backed securities (RMBS) by analyzing individual mortgage characteristics and portfolio risk.

## Features
- Calculate individual mortgage risk scores
- Assess overall credit rating for mortgage portfolios
- Validate mortgage data with comprehensive checks
- Flexible risk assessment using multiple financial parameters

## Prerequisites
- Python 3.8+
- No external dependencies required

## Installation

### Clone the Repository
```sh
git clone https://github.com/rushikesh-shinde-pyd/credit-rating-agency.git
cd credit_rating_mock
```

### Optional: Create Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

## Running the Code
```sh
python credit_rating_mock.py
```

## Running Unit Tests
```sh
python -m unittest test_credit_rating.py
```

## Key Components
- `credit_rating_mock.py`: Main script for credit rating calculation
- `test_credit_rating.py`: Comprehensive unit test suite

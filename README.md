# tekmoney
[![Build Status](https://travis-ci.org/tek-shinobi/tekmoney.svg?branch=master)](https://travis-ci.org/tek-shinobi/tekmoney)
Tek money. Handles money.

- Handles mathematical and comparison operations on product prices
- Implements exception handling
- Allows specifying tax on a product price
- Allows specifying a range for product price
- Allows for applying discount on product prices

## Installation
- Using pip: pip install tekmoney
- using pipenv: pipenv install tekmoney

## Usage
Use Currency class to specify amount and currency denomination.
- Currency(10, 'USD') indicates 10 us dollars
- Currency(Decimal('13.20'), 'USD') indicates 13 US dollars and 20 cents. Use Decimal class to specify non int values 

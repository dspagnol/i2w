# i2w

Integer to words. Given an integer, i2w outputs it as words.

As of today, the following languages are supported:

- English
- French
- Portuguese
- Spanish

## Install i2w from source

```bash
# clone the repo, go to the project root directory and run the command below
pip3 install .
```

## Usage

Basic usage:

```bash
$ i2w 123
one hundred twenty-three

$ i2w 0 1 -32 1000000
zero
one
minus thirty-two
one million

$ echo "0 1" | i2w
zero
one
```

Specific locale:

```bash
$ i2w -l C 1000000000
one billion

$ i2w -l en_US 1000000000
one billion

$ i2w -l en_GB 1000000000
one thousand million

$ i2w -l fr_CA 1000000000
un milliard

$ i2w -l fr_FR 1000000000
un-milliard

$ i2w -l pt_BR 1000000000
um bilhão
```

Print help:

```bash
$ i2w -h
usage: i2w [-h] [--locale LOCALE] [--verbose] [numbers ...]

positional arguments:
  numbers

options:
  -h, --help           show this help message and exit
  --locale, -l LOCALE
  --verbose, -v
```

## Uninstall i2w

```bash
pip3 uninstall i2w
```

## Useful Commands for i2w Developers

```bash
# run all unit tests and semantics checks (requirements: mypy and ruff)
python3 -m unittest && mypy tests && mypy src && ruff check

# usage without installation
python3 -m src.i2w 123

# sample script (assuming i2w package is installed)
python3 sample/i2w2.py

# extract numbers from a file
grep -Eo -- '-?[0-9]+' README.md | python3 -m src.i2w

# largest positive 999-illion in short scale
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=1000 ; n=999 ; print(a*10**(3*n+3)-1)" | python3 -m src.i2w -l en_US

# largest negative 999-illion in short scale
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=-1000 ; n=999 ; print(a*10**(3*n+3)+1)" | python3 -m src.i2w -l en_US

# largest positive 999-illion in long scale
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=1000000 ; n=999 ; print(a*10**(6*n)-1)" | python3 -m src.i2w -l en_GB
python3 -m src.i2w -l en_GB $(PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=1000000 ; n=999 ; print(a*10**(6*n)-1)")

# largest negative 999-illion in long scale
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=-1000000 ; n=999 ; print(a*10**(6*n)+1)" | python3 -m src.i2w -l en_GB

# googol and googolplex
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**100)" | python3 -m src.i2w -l C
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**10**100)" | python3 -m src.i2w -l C # the command before the pipe never finished in my machine

# performance comparison on an old mac mid-2015
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*1000+3))" | time python3 -m src.i2w -l C # ~0.1 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*10000+3))" | time python3 -m src.i2w -l C # ~0.1 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*100000+3))" | time python3 -m src.i2w -l C # ~0.4 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*1000000+3))" | time python3 -m src.i2w -l C # ~7.5 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*10000000+3))" | time python3 -m src.i2w -l C # ~192.6 s
```

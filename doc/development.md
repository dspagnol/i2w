# Development Guide for i2w

This guide contains information for developers who want to contribute to or work with the i2w codebase.

## Running Tests and Checks

Run all unit tests and semantic checks (requires: pytest, mypy, and ruff):

```bash
pytest && mypy tests && mypy src && ruff check
```

## Usage Without Installation

Test the package without installing it:

```bash
python3 -m src.i2w 123
```

## Sample Script

Run the sample script (requires i2w package to be installed):

```bash
python3 sample/i2w2.py
```

## Advanced Examples

### Extract Numbers from Files

Extract all numbers from a file and convert them to words:

```bash
grep -Eo -- '-?[0-9]+' README.md | python3 -m src.i2w
```

### Large Number Examples

These examples demonstrate i2w's ability to handle very large numbers:

**Largest positive 999-illion in short scale:**
```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=1000 ; n=999 ; print(a*10**(3*n+3)-1)" | python3 -m src.i2w -l en_US
```

**Largest negative 999-illion in short scale:**
```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=-1000 ; n=999 ; print(a*10**(3*n+3)+1)" | python3 -m src.i2w -l en_US
```

**Largest positive 999-illion in long scale:**
```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=1000000 ; n=999 ; print(a*10**(6*n)-1)" | python3 -m src.i2w -l en_GB
```

**Largest negative 999-illion in long scale:**
```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=-1000000 ; n=999 ; print(a*10**(6*n)+1)" | python3 -m src.i2w -l en_GB
```

**Googol and Googolplex:**
```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**100)" | python3 -m src.i2w -l C
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**10**100)" | python3 -m src.i2w -l C  # may take a very long time
```

### Performance Benchmarks

Performance comparison on an old Mac mid-2015:

```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*1000+3))" | time python3 -m src.i2w -l C          # ~0.1 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*10000+3))" | time python3 -m src.i2w -l C         # ~0.1 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*100000+3))" | time python3 -m src.i2w -l C        # ~0.4 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*1000000+3))" | time python3 -m src.i2w -l C       # ~7.5 s
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*10000000+3))" | time python3 -m src.i2w -l C      # ~192.6 s
```

## Building and Distribution

Refer to `pyproject.toml` for package configuration and build instructions.

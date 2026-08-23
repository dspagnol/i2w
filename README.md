# i2w

Convert integers to their word representations in multiple languages.

## Features

- **Multi-language support**: English, French, Portuguese, and Spanish
- **Multiple number systems**: Supports both short scale (US/modern) and long scale (UK/traditional) for large numbers
- **Large number support**: Handles arbitrarily large integers
- **Locale-aware**: Automatically adapts formatting based on system or specified locale

## Installation

### From PyPI

```bash
pip install i2w
```

### From Source

```bash
git clone https://github.com/dspagnol/i2w.git
cd i2w
pip install .
```

## Quick Start

Basic usage:

```bash
$ i2w 123
one hundred twenty-three

$ i2w 0 1 -32 1000000
zero
one
minus thirty-two
one million

$ i2w 100000000000000000000000000000000000
one hundred decillion
```

Read from stdin:

```bash
$ echo "0 1" | i2w
zero
one
```

## Usage

### Command-Line Interface

Print help and available options:

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

### Locale-Specific Conversion

By default, i2w uses your system locale. You can specify a different locale:

```bash
$ i2w -l en_US 1000000000
one billion

$ i2w -l en_GB 1000000000
one thousand million

$ i2w -l fr_FR 1000000000
un-milliard

$ i2w -l pt_BR 1000000000
um bilhão
```

**Note**: On Linux, run `locale -a` to see all available locales on your system.

### Advanced Usage

Extract numbers from a file:

```bash
grep -Eo -- '-?[0-9]+' README.md | i2w
```

## Uninstallation

```bash
pip uninstall i2w
```

## Contributing

For development information, testing, and advanced examples, see [doc/development.md](doc/development.md).

## License

See LICENSE file for details.

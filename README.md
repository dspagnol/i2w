# i2w

A Python library to convert integers to their word representations in multiple languages.

## Overview

**i2w** is primarily a **library for programmers** that provides robust, locale-aware integer-to-words conversion. It comes with a command-line interface for convenience and testing.

## Features

- **Multi-language support**: English, French, Portuguese, and Spanish
- **Multiple number systems**: Supports both short scale (US/modern) and long scale (UK/traditional) for large numbers
- **Large number support**: Handles arbitrarily large integers
- **Locale-aware**: Automatically adapts formatting based on system or specified locale
- **Programmer-friendly API**: Simple, intuitive interface for integration into Python applications

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

## Library Usage

The primary use case is as a library in Python applications:

```python
from i2w import Converter

# Use system locale
converter = Converter()
print(converter.to_words(123))  # "one hundred twenty-three"

# Use specific locale
converter_fr = Converter(locale_name="fr_FR")
print(converter_fr.to_words(123))  # "cent-vingt-trois"

# Override with a different locale
converter_pt = Converter(locale_name="pt_BR")
print(converter_pt.to_words(1000000))  # "um milhão"
```

### Locale Parameter

The `locale_name` parameter accepts POSIX locale strings (e.g., `"en_US"`, `"fr_FR"`, `"pt_BR"`):

- **Default behavior**: If `locale_name` is not specified or is an empty string, the library automatically uses the system's environment locale
- **Override locale**: Explicitly pass a locale string to override the system locale

Supported locales include:

- **English**: `en_US`, `en_GB`
- **French**: `fr_FR`, `fr_BE`, `fr_CH`, `fr_CA`
- **Spanish**: `es_ES`
- **Portuguese**: `pt_PT`, `pt_BR`

## Command-Line Interface

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

### Usage

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

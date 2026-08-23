# Development Guide for i2w

This guide contains information for developers who want to contribute to or work with the i2w codebase.

## Initial Setup: Create a Virtual Environment

### Option 1: Using the provided script (Recommended)

The project includes a convenience script to set up everything:

```bash
bash scripts/venv_create
```

This script:

- Creates a Python virtual environment (`venv/`)
- Upgrades pip
- Installs pip-tools (for managing locked dependencies)
- Compiles and installs all dev requirements

### Option 2: Manual setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Upgrade pip
pip install --upgrade pip

# Install pip-tools
pip install pip-tools

# Install dev requirements
pip install -r scripts/requirements-dev.txt
```

## Activating the Virtual Environment

Always activate the venv before working:

```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

Your prompt should show `(venv)` prefix when activated.

## Managing Dev Dependencies

### Adding a new dev dependency

1. Add the package to `scripts/requirements-dev.in`:

   ```ini
   black
   bump2version
   mypy
   pytest
   ruff
   your-new-package  # Add here
   ```

2. Regenerate the locked requirements:

   ```bash
   pip-compile scripts/requirements-dev.in --output-file=scripts/requirements-dev.txt
   ```

3. Install the updated dependencies:

   ```bash
   pip-sync scripts/requirements-dev.txt
   ```

Or combine in one command:

```bash
pip-compile scripts/requirements-dev.in --output-file=scripts/requirements-dev.txt && pip-sync scripts/requirements-dev.txt
```

### Updating all dev dependencies to latest versions

```bash
pip-compile --upgrade scripts/requirements-dev.in --output-file=scripts/requirements-dev.txt
pip-sync scripts/requirements-dev.txt
```

### What are `.in` and `.txt` files?

- **`requirements-dev.in`**: Specifies loose version constraints (human-readable, maintainer-friendly)
  - Example: `pytest` (gets latest), `black>=20.0` (minimum version)
  
- **`requirements-dev.txt`**: Auto-generated locked file with pinned versions (reproducible builds)
  - Example: `pytest==9.1.1` (exact version)
  - Never edit this manually; always regenerate with `pip-compile`

## Version Bumping

This project uses `bump2version` to automate version bumping.

### Bump version

```bash
# Bump patch version (0.0.2 → 0.0.3)
bump2version patch

# Bump minor version (0.0.2 → 0.1.0)
bump2version minor

# Bump major version (0.0.2 → 1.0.0)
bump2version major
```

This automatically:

1. Updates `src/i2w/__init__.py` with new version
2. Creates a git commit with the version bump
3. Creates a git tag (e.g., `v0.0.3`)

### Push and release

After bumping:

```bash
# Push commit and tag
git push origin main
git push origin --tags

# Go to GitHub and create a release from the tag
# The release.yml workflow will automatically publish to PyPI
```

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

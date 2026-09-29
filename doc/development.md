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
- Compiles `scripts/requirements-dev.txt` for Python 3.12 compatibility
- Syncs dependencies from the lockfile
- Installs the project in editable mode

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

# Install project in editable mode
pip install -e .
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

For best compatibility, regenerate lockfiles using Python 3.12 (the minimum
supported runtime). The `scripts/venv_create` helper prefers `python3.12`
automatically when available.

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
   pip-compile --strip-extras scripts/requirements-dev.in --output-file=scripts/requirements-dev.txt
   ```

3. Install the updated dependencies:

   ```bash
   pip-sync scripts/requirements-dev.txt
   ```

Or combine in one command:

```bash
pip-compile --strip-extras scripts/requirements-dev.in --output-file=scripts/requirements-dev.txt && pip-sync scripts/requirements-dev.txt
```

### Updating all dev dependencies to latest versions

```bash
pip-compile --strip-extras --upgrade scripts/requirements-dev.in --output-file=scripts/requirements-dev.txt
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

```

Create the release on GitHub (web):

- Open your repository on GitHub → "Releases" → "Draft a new release".
- Choose the tag you pushed (for example `v0.0.3`) or create it from the form.
- Use a concise release title and paste the release notes using the template below.
- Publish the release when ready — the `release.yml` workflow will automatically
   publish to PyPI once the release exists and CI verification passes.

Example release notes template (copy into the GitHub Release description):

```markdown
v0.0.3 — Patch release

*Summary*
Short, one-line summary of the release purpose.

*Changes*
- Fix: Short description of the security hardening for CLI integer parsing.
- Chore: Minor tooling and documentation updates.

*Notes*
- No user-facing API changes. Consumers can upgrade safely.
```

Create the release using the `gh` CLI (alternative):

```bash
# Prepare a file with the release notes
cat > release-notes.md <<'EOF'
v0.0.3 — Patch release

*Summary*
Short, one-line summary of the release purpose.

*Changes*
- Fix: Short description of the security hardening for CLI integer parsing.
- Chore: Minor tooling and documentation updates.

*Notes*
- No user-facing API changes. Consumers can upgrade safely.
EOF

# Create the release (replace v0.0.3 with your tag)
gh release create v0.0.3 --title "v0.0.3 — Patch release" --notes-file release-notes.md
```

## Running Tests and Checks

Run all unit tests and semantic checks (requires: pytest, mypy, and ruff):

```bash
pytest && ruff check src tests && mypy tests && mypy src
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
grep -Eo -- '-?[0-9]+' README.md | i2w
```

### Large Named Numbers

These examples demonstrate i2w's ability to handle very large numbers with conventional names (up to 999-illion):

**Largest positive 999-illion in short scale:**

```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=1000 ; n=999 ; print(a*10**(3*n+3)-1)" | i2w --max-str-digits 0 -l en_US
```

**Largest negative 999-illion in short scale:**

```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=-1000 ; n=999 ; print(a*10**(3*n+3)+1)" | i2w --max-str-digits 0 -l en_US
```

**Largest positive 999-illion in long scale:**

```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=1000000 ; n=999 ; print(a*10**(6*n)-1)" | i2w --max-str-digits 0 -l en_GB
```

**Largest negative 999-illion in long scale:**

```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "a=-1000000 ; n=999 ; print(a*10**(6*n)+1)" | i2w --max-str-digits 0 -l en_GB
```

**Googol and Googolplex:**

```bash
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**100)" | i2w --max-str-digits 0 -l C
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**10**100)" | i2w --max-str-digits 0 -l C  # may take a very long time
```

### Beyond Named Numbers

The program can handle numbers far beyond the conventional 999-illion limit. The performance benchmarks below demonstrate this capability with arbitrarily large numbers:

### Performance Benchmarks

**Note:** To measure i2w processing time accurately, generate the number to a file first, then time only the conversion (the piping approach includes number generation time).

Performance comparison on an old Intel(R) Core(TM) i5-5257U CPU @ 2.70GHz:

```bash
# Generate each number once
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*1000+3))" > /tmp/n1000.txt
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*10000+3))" > /tmp/n10000.txt
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*100000+3))" > /tmp/n100000.txt
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*1000000+3))" > /tmp/n1000000.txt
PYTHONINTMAXSTRDIGITS=0 python3 <<< "print(10**(3*10000000+3))" > /tmp/n10000000.txt

# Then time only i2w processing
time -p i2w --max-str-digits 0 -l C < /tmp/n1000.txt      #  ~ 0.1 s
time -p i2w --max-str-digits 0 -l C < /tmp/n10000.txt     #  ~ 0.1 s
time -p i2w --max-str-digits 0 -l C < /tmp/n100000.txt    #  ~ 0.5 s
time -p i2w --max-str-digits 0 -l C < /tmp/n1000000.txt   #  ~ 5.2 s
time -p i2w --max-str-digits 0 -l C < /tmp/n10000000.txt  # ~ 71.8 s
```

## Building and Distribution

Refer to `pyproject.toml` for package configuration and build instructions.

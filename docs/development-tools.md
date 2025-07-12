# Development Tools and Commands

## Overview
This document provides a comprehensive guide to development tools, commands, and utilities for the napari-flicker plugin development.

## Essential Development Tools

### Required Tools
These tools are essential for napari-flicker development:

| Tool | Purpose | Installation |
|------|---------|--------------|
| **pixi** | Package and environment management | `curl -fsSL https://pixi.sh/install.sh | bash` |
| **git** | Version control | System package manager |
| **python** | Programming language | Included in pixi environment |
| **napari** | Core napari application | Managed by pixi |
| **pytest** | Testing framework | Managed by pixi |
| **pre-commit** | Code quality hooks | Managed by pixi |

### Recommended Tools
These tools enhance the development experience:

| Tool | Purpose | Installation |
|------|---------|--------------|
| **GitHub CLI** | GitHub operations | `gh auth login` |
| **ruff** | Fast Python linter/formatter | Managed by pixi |
| **pyright** | Type checking | Managed by pixi |
| **tox** | Testing across environments | Managed by pixi |

## Environment Setup

### Initial Setup
```bash
# Clone the repository
git clone https://github.com/amano-takahisa/napari-flicker.git
cd napari-flicker

# Verify pixi installation
pixi --version

# Install project dependencies
pixi install

# Set up development environment
pixi shell --environment development

# Install pre-commit hooks
pre-commit install
```

### Environment Management
```bash
# Activate development environment
pixi shell --environment development

# Activate test environment
pixi shell --environment test

# List available environments
pixi info

# Update dependencies
pixi update

# Clean environment
pixi clean
```

## Development Commands

### Core Development
```bash
# Start napari with plugin
napari --with napari-flicker

# Install plugin in development mode
pip install -e .

# Run plugin-specific napari widget
napari --with napari-flicker 'Flicker Widget'
```

### Code Quality
```bash
# Run all pre-commit hooks
pre-commit run --all-files

# Run specific hooks
pre-commit run ruff              # Linting
pre-commit run ruff-format       # Formatting
pre-commit run pyright           # Type checking

# Format code manually
ruff check src/ --fix
ruff format src/

# Type checking
pyright src/
```

### Testing Commands
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=napari_flicker --cov-report=html

# Run specific test file
pytest src/napari_flicker/_tests/test_flicker.py

# Run specific test function
pytest src/napari_flicker/_tests/test_flicker.py::test_layer_selection

# Run tests in verbose mode
pytest -v -s

# Run tests with debugging
pytest --pdb

# Run failed tests only
pytest --lf

# Run tests in parallel
pytest -n auto
```

### Testing with Tox
```bash
# Run tests across multiple Python versions
pixi run --environment test tox

# Run specific tox environment
tox -e py310
tox -e py311
tox -e py312

# List available tox environments
tox -l

# Run tox with coverage
tox -e coverage
```

## Code Analysis Tools

### Linting and Formatting
```bash
# Check code style
ruff check src/

# Fix auto-fixable issues
ruff check src/ --fix

# Format code
ruff format src/

# Check specific file
ruff check src/napari_flicker/_widget.py
```

### Type Checking
```bash
# Run type checking
pyright src/

# Check specific file
pyright src/napari_flicker/_widget.py

# Generate type coverage report
pyright --stats src/
```

### Import Sorting
```bash
# Check import organization
isort --check-only src/

# Fix import organization
isort src/

# Show import differences
isort --diff src/
```

## Git Commands

### Branch Management
```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Switch branches
git checkout develop
git checkout main

# List branches
git branch -a

# Delete merged branch
git branch -d feature/completed-feature

# Update from remote
git pull origin develop
```

### Commit Operations
```bash
# Stage changes
git add .
git add src/napari_flicker/_widget.py

# Commit with message
git commit -m "feat: implement layer selection UI"

# Amend last commit
git commit --amend

# Interactive rebase
git rebase -i HEAD~3
```

### Remote Operations
```bash
# Push branch
git push origin feature/new-feature

# Create PR with GitHub CLI
gh pr create --title "feat: implement new feature" --body "Description"

# Check PR status
gh pr status

# Merge PR
gh pr merge --squash
```

## Debugging Commands

### napari Debugging
```bash
# Start napari with debug logging
NAPARI_LOG_LEVEL=DEBUG napari --with napari-flicker

# Start napari with console
napari --with napari-flicker --console

# Start napari with specific plugin only
napari --with napari-flicker --plugin napari-flicker

# Check plugin loading
napari --info
```

### Python Debugging
```bash
# Run with Python debugger
python -m pdb -c continue -m napari --with napari-flicker

# Run pytest with debugger
pytest --pdb

# Run specific test with debugging
pytest --pdb src/napari_flicker/_tests/test_flicker.py::test_layer_selection
```

### Performance Profiling
```bash
# Profile napari startup
python -m cProfile -o startup.prof -m napari --with napari-flicker

# Profile specific test
python -m cProfile -o test.prof -m pytest src/napari_flicker/_tests/test_flicker.py

# Analyze profile
python -m snakeviz startup.prof
```

## Build and Distribution

### Package Building
```bash
# Build package
python -m build

# Check package
twine check dist/*

# Install from built package
pip install dist/napari_flicker-*.whl
```

### Documentation Generation
```bash
# Generate API documentation
sphinx-apidoc -o docs/api src/napari_flicker

# Build documentation
sphinx-build -b html docs/ docs/_build/html

# Serve documentation locally
python -m http.server 8000 -d docs/_build/html
```

## Continuous Integration

### Local CI Testing
```bash
# Run same tests as CI
pytest --cov=napari_flicker --cov-report=xml

# Test multiple Python versions (with tox)
tox

# Check pre-commit hooks
pre-commit run --all-files
```

### GitHub Actions
```bash
# Check workflow syntax
gh workflow view

# Run workflow locally (with act)
act push

# Check workflow status
gh run list
```

## Development Utilities

### File and Directory Operations
```bash
# Find Python files
find src/ -name "*.py" -type f

# Count lines of code
find src/ -name "*.py" -exec wc -l {} + | sort -n

# Search for patterns
grep -r "QWidget" src/

# Find TODO comments
grep -r "TODO\|FIXME" src/
```

### Code Metrics
```bash
# Count lines of code
cloc src/

# Check cyclomatic complexity
radon cc src/

# Check maintainability index
radon mi src/

# Generate complexity report
radon cc src/ --show-complexity
```

## IDE Integration

### VS Code
```bash
# Install Python extension
code --install-extension ms-python.python

# Open workspace
code .

# Run task
code --task test
```

### PyCharm
```bash
# Create configuration for pytest
# Run -> Edit Configurations -> + -> Python tests -> pytest

# Configure interpreter
# File -> Settings -> Project -> Python Interpreter
```

## Troubleshooting Commands

### Environment Issues
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check napari installation
napari --version

# Verify plugin installation
napari --info | grep napari-flicker
```

### Common Fixes
```bash
# Clear pytest cache
pytest --cache-clear

# Reset pip cache
pip cache purge

# Reinstall development dependencies
pip install -e .[dev]

# Reset git to clean state
git clean -fd
git reset --hard HEAD
```

### Performance Debugging
```bash
# Monitor memory usage
python -m memory_profiler script.py

# Check import times
python -X importtime -m napari --with napari-flicker

# Profile specific function
python -m cProfile -s cumulative script.py
```

## Quick Reference

### Daily Development Workflow
```bash
# Start development session
pixi shell --environment development
git pull origin develop

# Make changes
# ... edit code ...

# Check code quality
pre-commit run --all-files

# Run tests
pytest

# Commit changes
git add .
git commit -m "feat: implement new feature"

# Push changes
git push origin feature/my-feature
```

### Testing Workflow
```bash
# Run quick tests
pytest src/napari_flicker/_tests/test_flicker.py

# Run with coverage
pytest --cov=napari_flicker --cov-report=term-missing

# Run specific test with output
pytest -v -s src/napari_flicker/_tests/test_flicker.py::test_specific_function
```

### Release Preparation
```bash
# Check version
python -c "import napari_flicker; print(napari_flicker.__version__)"

# Run full test suite
tox

# Check code quality
pre-commit run --all-files

# Build package
python -m build
```

## Tool Configuration Files

### Key Configuration Files
- **pyproject.toml**: Project configuration, dependencies, tool settings
- **.pre-commit-config.yaml**: Pre-commit hooks configuration
- **tox.ini**: Testing environment configuration
- **.github/workflows/**: CI/CD pipeline configuration

### Important Settings
- **ruff**: Line length, quote style, linting rules
- **pyright**: Type checking strictness, Python version
- **pytest**: Test discovery, coverage settings
- **isort**: Import sorting preferences

## Performance Optimization

### Development Performance
```bash
# Use parallel testing
pytest -n auto

# Skip slow tests during development
pytest -m "not slow"

# Use test markers
pytest -m "unit and not integration"
```

### Code Performance
```bash
# Profile specific functions
python -m cProfile -o profile.prof script.py

# Memory profiling
python -m memory_profiler script.py

# Line-by-line profiling
kernprof -l -v script.py
```

This comprehensive toolkit provides all the necessary commands and tools for efficient napari-flicker plugin development.

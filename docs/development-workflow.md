# napari-flicker Development Workflow

## Overview
This document outlines the development workflow, branching strategy, and processes for the napari-flicker plugin development. The project follows Test Driven Development (TDD) methodology and uses GitHub Flow for simple branch management.

## Git Workflow

### Branching Strategy
We use GitHub Flow - a simple workflow with only the main branch and feature branches:

```
main (production-ready, always deployable)
├── feature/flicker-widget
├── feature/ui-improvements
├── hotfix/layer-selection-bug
└── feature/timer-implementation
```

### Branch Types

#### Main Branch
- **Purpose**: Production-ready code that is always deployable
- **Protection**: Protected, requires PR approval and status checks
- **Direct commits**: Not allowed
- **Deployment**: Continuous deployment from main
- **Quality**: All merged code must be tested and reviewed

#### Feature Branches
- **Naming**: `feature/description` or `hotfix/description`
- **Base**: Always created from latest `main`
- **Lifecycle**: Merge directly back to `main` when complete
- **Examples**:
  - `feature/flicker-widget`
  - `feature/layer-selection-ui`
  - `hotfix/timer-precision-bug`
- **Scope**: Keep changes focused and small for faster review

## TDD Development Process

### 1. Starting New Work (TDD Approach)

```bash
# Update local repository
git checkout main
git pull origin main

# Create new feature branch
git checkout -b feature/your-feature-name

# TDD Red-Green-Refactor Cycle:

# RED: Write failing test first
# Create test file if not exists
touch src/napari_flicker/_tests/test_your_feature.py

# Write failing test that defines expected behavior
# Run test to ensure it fails for the right reason
pytest src/napari_flicker/_tests/test_your_feature.py::test_specific_feature

# GREEN: Write minimal code to make test pass
# Implement feature in main code
# Run test again to ensure it passes
pytest src/napari_flicker/_tests/test_your_feature.py::test_specific_feature

# REFACTOR: Improve code quality
# Refactor implementation while keeping tests green
# Run all tests to ensure no regressions
pytest

# Commit with test and implementation
git add .
git commit -m "feat: implement layer selection UI (TDD)

RED: Write test for QCheckBox layer selection
GREEN: Implement minimal layer filtering for Image/Labels
REFACTOR: Improve code organization and performance

- Add failing test for layer selection behavior
- Implement QCheckBox list for layer selection
- Add layer filtering for Image/Labels
- Refactor UI component organization
- Add automatic layer list updates

Test-driven implementation ensures 100% coverage for this feature.

Closes #123"
```

### 2. Commit Message Convention

We use conventional commits for clear commit history:

```
<type>(<scope>): <description>

<body>
```

#### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or modifying tests
- **chore**: Maintenance tasks

#### TDD-Enhanced Examples
```bash
feat(widget): implement flicker toggle functionality (TDD)
fix(timer): resolve timing precision issues (test-first)
docs(readme): add usage instructions
test(flicker): add comprehensive unit tests for layer selection
style(widget): apply consistent formatting
refactor(ui): reorganize widget layout code (TDD refactor)
chore(deps): update development dependencies

# TDD-specific commit patterns
test(widget): add failing test for layer visibility toggle
feat(widget): implement layer visibility toggle (make test pass)
refactor(widget): improve toggle performance (maintain test coverage)
```

### 3. Pull Request Process

#### Creating a Pull Request

```bash
# Push feature branch to origin
git push origin feature/your-feature-name

# Create PR using GitHub CLI
gh pr create --title "feat: implement layer selection UI" --body "
## Summary
- Implement QCheckBox list for layer selection
- Add layer filtering for Image/Labels only
- Add automatic layer list updates when layers change

## Testing
- [ ] Unit tests pass
- [ ] Manual testing with multiple layers
- [ ] Edge case testing (no layers, unsupported types)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests added for new functionality
- [ ] Documentation updated if needed
- [ ] No breaking changes

Closes #123
"
```

#### TDD-Enhanced PR Requirements
- [ ] **Title**: Follows conventional commit format with TDD indicators
- [ ] **Description**: Clear summary of changes including TDD cycle
- [ ] **Tests**: All automated tests pass (written before implementation)
- [ ] **Test Coverage**: Maintains or improves coverage (target >95%)
- [ ] **TDD Evidence**: Shows Red-Green-Refactor cycle was followed
- [ ] **Code Review**: At least one approval required
- [ ] **Conflicts**: No merge conflicts with target branch
- [ ] **Documentation**: Updated if functionality changes

#### TDD-Enhanced PR Review Checklist
- [ ] **TDD Compliance**: Evidence of Red-Green-Refactor cycle
- [ ] **Test Quality**: Tests written before implementation
- [ ] **Functionality**: Features work as specified by tests
- [ ] **Code Quality**: Clean, readable, well-organized
- [ ] **Test Coverage**: >95% coverage maintained or improved
- [ ] **Test Design**: Tests are isolated, fast, and descriptive
- [ ] **Documentation**: Docstrings and comments where needed
- [ ] **Performance**: No performance regressions
- [ ] **Compatibility**: Works with supported napari versions
- [ ] **Refactoring Safety**: Changes don't break existing tests

### 4. Merging Strategy

#### Feature to Main
- **Method**: Merge commit (preserve commit history)
- **Reason**: Maintain full development history and individual commits
- **Process**:
  1. Create PR from feature branch to main
  2. Code review and approval required
  3. All status checks must pass
  4. Merge with merge commit (no squashing)
  5. Delete feature branch after merge

## Release Process

### 1. Prepare Release

```bash
# Work directly on main branch
git checkout main
git pull origin main

# Update version in _version.py if needed
# Update CHANGELOG.md
# Create release commit

git add .
git commit -m "chore: prepare release v1.0.0"
git push origin main
```

### 2. Tag and Deploy

```bash
# Create and push tag from main
git tag -a v1.0.0 -m "Release v1.0.0: Initial napari-flicker plugin"
git push origin v1.0.0

# GitHub Actions will handle deployment from the tag
```

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11, 3.12]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[test]

    - name: Run tests
      run: pytest --cov=napari_flicker --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pixi shell --environment development
pre-commit install

# Manual run
pre-commit run --all-files
```

## Quality Assurance

### Code Quality Checks
- **Linting**: ruff for Python linting
- **Formatting**: ruff for code formatting
- **Type Checking**: pyright for type checking
- **Import Sorting**: isort for import organization

### TDD Testing Requirements
- **Unit Tests**: >95% coverage target (achieved through TDD)
- **Test-First Development**: All features start with failing tests
- **Integration Tests**: Key user workflows tested first
- **Performance Tests**: Layer handling performance with test benchmarks
- **Manual Testing**: User experience validation
- **Test Quality**: Tests serve as living documentation
- **Regression Prevention**: Comprehensive test suite prevents breaking changes

### Documentation Standards
- **Docstrings**: All public methods documented
- **Type Hints**: All function signatures typed
- **Comments**: Complex logic explained
- **README**: Usage instructions updated

## Issue Management

### Issue Templates

#### Bug Report
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Load napari with plugin
2. Add image layers
3. Select layers and start flicker
4. Observe issue

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- napari version:
- Python version:
- Operating System:
```

#### Feature Request
```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Implementation**
How should this feature work?

**Acceptance Criteria**
- [ ] Requirement 1
- [ ] Requirement 2
```

### Issue Labels
- **Type**: `bug`, `enhancement`, `documentation`, `question`
- **Priority**: `high`, `medium`, `low`
- **Status**: `ready`, `in-progress`, `blocked`, `needs-review`
- **Component**: `widget`, `ui`, `timer`, `testing`

## Environment Setup

### Development Environment

```bash
# Clone repository
git clone https://github.com/amano-takahisa/napari-flicker.git
cd napari-flicker

# Load the Nix tools (when using Nix/direnv)
direnv allow

# Set up development environment
pixi shell --environment development

# Install pre-commit hooks
pre-commit install

# Run tests
pixi run --environment test test
```

On NixOS, the Nix shell exposes the running system's GPU drivers through
`/run/opengl-driver/lib`. Pixi supplies Qt and its native libraries from
conda-forge; on Linux, `VISPY_GL_LIB` points to Pixi's `libGL.so.1`.
Run pre-commit from the Pixi development environment as well.
Headless Qt settings apply only to the test task.

Start the GUI with:

```bash
pixi run -e development napari --with napari-flicker 'Flicker Widget'
```

The locked Qt build can use XWayland (`xcb`) on a Wayland desktop.
It may warn that the native Wayland platform plugin is unavailable.

When migrating an existing environment from PyPI Qt to conda-forge Qt,
recreate it if Qt reports missing platform plugins. For example, move
`.pixi/envs/development` outside `.pixi/envs`, then run
`pixi install --locked -e development`.

After changing `flake.nix`, run `direnv reload`. If the current terminal was
started inside the old environment, open a fresh desktop terminal and enter
the repository again. The environment inherits `WAYLAND_DISPLAY` and `DISPLAY`
from the desktop session; it does not choose or hard-code a display socket.

### Local Testing

```bash
# Run unit tests
pytest src/napari_flicker/_tests/

# Run tests with coverage
pytest --cov=napari_flicker --cov-report=html

# Run specific test
pytest src/napari_flicker/_tests/test_flicker.py::test_layer_selection

# Run linting
pixi run --environment development pre-commit run --all-files
```

## Troubleshooting

### Common Issues

#### Git Issues
```bash
# Reset to clean state
git checkout develop
git reset --hard origin/develop

# Resolve merge conflicts
git status
# Edit conflicting files
git add .
git commit -m "resolve merge conflicts"
```

#### Development Environment
```bash
# Clean environment
pixi clean
pixi shell --environment development

# Reinstall dependencies
pixi install

# Check environment
pixi info
```

#### Testing Issues
```bash
# Clear pytest cache
pytest --cache-clear

# Run tests in verbose mode
pytest -v -s

# Run only failed tests
pytest --lf
```

## Best Practices

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all functions
- Write descriptive docstrings
- Keep functions small and focused
- Use meaningful variable names

### Git Practices
- Write clear commit messages
- Make atomic commits
- Test before committing
- Keep branches focused
- Regular updates from develop

### TDD Testing Practices
- **Red Phase**: Write failing tests that define expected behavior
- **Green Phase**: Write minimal code to make tests pass
- **Refactor Phase**: Improve code while maintaining test coverage
- **Test First**: Always write tests before implementing features
- **Edge Cases**: Test boundary conditions and error scenarios
- **Descriptive Names**: Test names clearly describe expected behavior
- **Test Isolation**: Each test is independent and focused
- **Mock Strategy**: Mock external dependencies appropriately
- **Fast Feedback**: Unit tests run quickly (<1s per test)
- **Living Documentation**: Tests document expected system behavior

### Documentation Practices
- Update documentation with code changes
- Write clear, concise explanations
- Include code examples
- Keep documentation up to date
- Review documentation regularly

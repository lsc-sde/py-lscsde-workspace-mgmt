# Contributing to lscsde-workspace-mgmt

We welcome contributions to the `lscsde-workspace-mgmt` library. This guide outlines the process for contributing.

## Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/lsc-sde/py-lscsde-workspace-mgmt.git
   cd py-lscsde-workspace-mgmt
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

- We use [ruff](https://github.com/astral-sh/ruff) for code formatting and linting
- Run linting with:
  ```bash
  ruff check .
  ```

## Testing

- Write tests for new functionality
- Ensure all tests pass before submitting:
  ```bash
  pytest
  ```

## Documentation

- Update documentation for any new features or changes
- Generate documentation with:
  ```bash
  mkdocs build
  ```
- Preview documentation locally:
  ```bash
  mkdocs serve
  ```

## Submitting Changes

1. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make and commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```

3. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a pull request on GitHub

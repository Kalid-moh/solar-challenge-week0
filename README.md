# solar-challenge-week0

solar-challenge-week0 repo
#Test again

# Solar Challenge – Week 0

[![Python Version](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)
[![CI](https://github.com/Kalid-moh/solar-challenge-week0/actions/workflows/unittests.yml/badge.svg)](https://github.com/Kalid-moh/solar-challenge-week0/actions/workflows/unittests.yml)

## 1. Repository Overview

This repository contains the initial setup for the Solar Challenge project, including:

- Git repository setup with branching workflow
- Python virtual environment configuration
- Continuous integration workflow
- Folder structure for source code, notebooks, tests, and scripts

## 2. Prerequisites

Before running the project, make sure you have:

- Python 3.x installed
- Git installed
- (Optional) VS Code for development

## 3. Clone the Repository

```bash
git clone https://github.com/Kalid-moh/solar-challenge-week0.git
cd solar-challenge-week0
```

## 4. Create & Activate Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python -m venv venv
source venv/bin/activate
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## 6. Project Structure

```
.vscode/
│   └── settings.json
.github/
│   └── workflows/
│       └── unittests.yml
.gitignore
requirements.txt
README.md
src/
notebooks/
│   ├── __init__.py
│   └── README.md
tests/
│   ├── __init__.py
scripts/
│   ├── __init__.py
│   └── README.md
```

- `src/` → Main source code
- `notebooks/` → Jupyter notebooks and documentation
- `tests/` → Unit tests
- `scripts/` → Helper scripts

## 7. Branching Workflow

- Development branch: `setup-task`
- Commit messages example:

  - `init: add .gitignore`
  - `chore: venv setup`
  - `ci: add GitHub Actions workflow`

## 8. Continuous Integration

- Workflow file: `.github/workflows/unittests.yml`
- Runs on push or pull requests:

  - Installs dependencies: `pip install -r requirements.txt`
  - Checks Python version: `python --version`
  - Can be extended to run tests later

## 9. Notes

- `data/` folder is ignored (add to `.gitignore`)
- Do **not commit CSV files**
- Always create a branch for new features or EDA tasks

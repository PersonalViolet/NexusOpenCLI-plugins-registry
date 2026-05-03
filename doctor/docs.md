# ncli-open-cli-doctor

Project health doctor plugin for [nexus-open-cli](https://github.com/nexus-cli/nexus-open-cli).

## Overview

`ncli-open-cli-doctor` is a CLI plugin that performs comprehensive health checks on your project. It analyzes various aspects of your project structure and provides actionable insights to improve project quality.

## Features

- ✅ **Git Repository Check**: Verifies if the project is initialized with Git
- 📄 **README Detection**: Checks for the presence of README.md
- 📜 **License Check**: Validates LICENSE file existence
- 🚫 **.gitignore Validation**: Ensures .gitignore file is present
- 📁 **Project Structure Analysis**: Evaluates file count and organization
- 📦 **Large File Detection**: Identifies files larger than 10MB
- 🔗 **Dependency File Check**: Detects dependency management files (requirements.txt, pyproject.toml, package.json, pom.xml)
- 🧪 **Test Coverage**: Checks for tests directory

## Installation

```bash
pip install ncli-open-cli-doctor
```

Or install from source:

```bash
git clone https://github.com/your-repo/ncli-open-cli-doctor.git
cd ncli-open-cli-doctor
pip install -e .
```

## Requirements

- Python >= 3.10
- nexus-open-cli
- typer >= 0.12, < 1.0
- rich >= 13, < 14
- babel >= 2.12, < 3.0

## Usage

Once installed as a plugin for `nexus-open-cli`, you can run:

```bash
ncli doctor --path /path/to/project
```

### Options

- `--path`: Target project path (default: current directory)
- `--verbose`: Show detailed report output

### Examples

Check the current directory:

```bash
ncli doctor
```

Check a specific project:

```bash
ncli doctor --path ./my-project
```

Show verbose output:

```bash
ncli doctor --path ./my-project --verbose
```

## Output

The plugin generates a health report with:

- Pass/Fail/Warning status for each check
- Overall health score (out of 100)
- Top 3 largest files in the project
- Detailed information in verbose mode

### Sample Output

```
Project Health Report
✓ Git repo initialized
✓ README.md present
✗ No LICENSE
✓ .gitignore present
✓ Project structure reasonable
✓ No large files detected
✓ Dependency file detected
✗ No tests folder
Score: 75/100

Top 3 largest files
File                  Size
─────────────────────────────
src/main.py          15.2 KB
README.md             5.8 KB
pyproject.toml        1.2 KB
```

## Scoring System

Each rule contributes to the overall score:

| Rule              | Weight    | Description                          |
| ----------------- | --------- | ------------------------------------ |
| Git Repository    | 20 points | Project should be version controlled |
| README.md         | 15 points | Documentation is essential           |
| LICENSE           | 10 points | Legal clarity for users              |
| .gitignore        | 10 points | Proper git configuration             |
| Project Structure | 15 points | Reasonable file count (< 1000)       |
| Large Files       | 10 points | No files > 10MB                      |
| Dependencies      | 10 points | Dependency management present        |
| Tests             | 10 points | Test suite availability              |

## Development

### Setup Development Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
pytest
```

### Building Package

```bash
pip install build
python -m build
```

## Project Structure

```
ncli-open-cli-doctor/
├── src/
│   └── ncli_doctor/
│       ├── __init__.py
│       └── plugin.py
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/)
- Rich terminal output powered by [Rich](https://rich.readthedocs.io/)
- Internationalization support via [Babel](https://babel.pocoo.org/)
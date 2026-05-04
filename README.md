# NexusOpenCLI Plugins Registry

English | [中文文档](README.zh-CN.md)

Welcome to the **NexusOpenCLI Plugins Registry**! This repository serves as the official plugin registry for [NexusOpenCLI](https://github.com/nexus-cli/nexus-open-cli), where developers can submit, discover, and manage plugins to extend the functionality of NexusOpenCLI.

## 📋 Table of Contents

- [Overview](#overview)
- [Plugin Submission Guidelines](#plugin-submission-guidelines)
- [Directory Structure](#directory-structure)
- [Submission Process](#submission-process)
- [Plugin Configuration](#plugin-configuration)
- [Review Process](#review-process)
- [Example: Doctor Plugin](#example-doctor-plugin)
- [Contributing](#contributing)
- [FAQ](#faq)

## 🌟 Overview

This registry allows community developers to contribute plugins that enhance NexusOpenCLI's capabilities. Each plugin is carefully reviewed to ensure quality, security, and compatibility before being added to the official registry.

## 📝 Plugin Submission Guidelines

### Prerequisites

Before submitting your plugin, please ensure:

1. ✅ **Published on PyPI**: Your plugin package must be published and available on [PyPI](https://pypi.org/)
2. ✅ **Source Code Available**: Include source code in the `plugins/{plugin-name}` directory (highly recommended)
3. ✅ **Documentation**: Provide a README.md or docs.md file explaining your plugin
4. ✅ **GitHub Account**: The author field in `plugins.json` will default to your GitHub username

### Requirements

- Plugin must be compatible with NexusOpenCLI
- Must follow Python packaging standards
- Should include proper documentation
- Must pass security review

## 📁 Directory Structure

```
NexusOpenCLI-plugins-registry/
├── plugins.json              # Plugin registry configuration
├── README.md                 # This file (English)
├── README.zh-CN.md          # Chinese documentation
└── plugins/                  # Plugin directories
    └── {plugin-name}/       # Individual plugin folder
        ├── README.md        # Plugin documentation (optional but recommended)
        ├── docs.md          # Alternative documentation file
        ├── src/             # Source code package (recommended)
        │   └── ...
        ├── pyproject.toml   # Build configuration (if including source)
        └── ...              # Other relevant files
```

### Example Structure

```
doctor/
├── docs.md                  # Plugin documentation
├── README.md                # Detailed usage guide
├── src/                     # Source code (optional but recommended)
│   └── ncli_doctor/
│       ├── __init__.py
│       └── plugin.py
└── pyproject.toml           # Package configuration
```

## 🚀 Submission Process

Follow these steps to submit your plugin:

### Step 1: Publish to PyPI

First, ensure your plugin is published on PyPI:

```bash
# Build your package
pip install build
python -m build

# Upload to PyPI
pip install twine
twine upload dist/*
```

Verify your package is available:
```bash
pip install your-plugin-name
```

### Step 2: Prepare Plugin Directory

Create a new directory under `plugins/` with your plugin name:

```bash
mkdir plugins/your-plugin-name
```

### Step 3: Add Documentation

Include at least one documentation file:
- `README.md` - Comprehensive plugin documentation
- `docs.md` - Alternative documentation format

Your documentation should include:
- Plugin overview and features
- Installation instructions
- Usage examples
- Configuration options
- API reference (if applicable)

### Step 4: Include Source Code (Recommended)

While optional, including source code is **highly recommended** because it:

- 🔒 Helps reviewers verify security and code quality
- 👥 Allows users to inspect the code before installation
- 🛠️ Enables users to install from source if needed
- 📚 Serves as reference implementation for other developers

You can include:
- Complete source code in `src/` directory
- `pyproject.toml` or `setup.py` for building
- Test files and examples

### Step 5: Update plugins.json

Add your plugin entry to [`plugins.json`](plugins.json):

```json
{
  "your-plugin-name": {
    "package": "nexus-open-cli-your-plugin",
    "version": "0.1.0",
    "description": "Brief description of your plugin",
    "author": "YourGitHubUsername"
  }
}
```

**Note**: The `author` field will be set to your GitHub username after review approval.

### Step 6: Submit Pull Request

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/add-your-plugin`
3. Commit your changes: `git commit -m 'Add your-plugin-name'`
4. Push to your fork: `git push origin feature/add-your-plugin`
5. Open a Pull Request with:
   - Clear description of your plugin
   - Link to PyPI package
   - Any special considerations

## ⚙️ Plugin Configuration

### plugins.json Schema

Each plugin entry in `plugins.json` should include:

| Field         | Type   | Required | Description                                    |
|---------------|--------|----------|------------------------------------------------|
| `package`     | string | Yes      | PyPI package name                              |
| `version`     | string | Yes      | Current version (semver format)               |
| `description` | string | Yes      | Brief description (max 200 characters)        |
| `author`      | string | Auto     | GitHub username (set during review)           |

### Example Entry

```json
{
  "doctor": {
    "package": "nexus-open-cli-doctor",
    "version": "0.1.0",
    "description": "Project health doctor",
    "author": "PersonalViolet"
  }
}
```

## 🔍 Review Process

Our review team will evaluate your submission based on:

### Security Check
- ✅ No malicious code or backdoors
- ✅ No hardcoded secrets or credentials
- ✅ Safe dependencies
- ✅ Proper error handling

### Quality Check
- ✅ Code follows Python best practices
- ✅ Adequate documentation
- ✅ Proper version management
- ✅ Clear plugin purpose and functionality

### Compatibility Check
- ✅ Compatible with current NexusOpenCLI version
- ✅ No conflicting dependencies
- ✅ Proper plugin interface implementation

## 📖 Example: Doctor Plugin

The [`doctor`](plugins/doctor/) plugin serves as a reference implementation:

### Features
- ✅ Git repository check
- 📄 README detection
- 📜 License validation
- 🚫 .gitignore verification
- 📁 Project structure analysis
- 📦 Large file detection
- 🔗 Dependency file check
- 🧪 Test coverage assessment

### Documentation
- See [`plugins/doctor/README.md`](plugins/doctor/README.md) for complete documentation
- Includes installation, usage, and development guides

### Source Code
- Source code can be included in the plugin directory
- Helps users understand implementation details

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Submit Plugins
Follow the [Submission Process](#-submission-process) above.

### Improve Documentation
- Fix typos or unclear explanations
- Add translations
- Improve examples

### Review Plugins
Help review submissions from other developers.

### Report Issues
Found a problem? Open an issue!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/nexus-cli/NexusOpenCLI-plugins-registry.git
cd NexusOpenCLI-plugins-registry

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## ❓ FAQ

### Q: Do I need to include source code?
**A**: While not required, it's **strongly recommended**. Including source code helps reviewers verify security and allows users to inspect the code before installation.

### Q: How long does review take?
**A**: Typically 1-3 business days for initial review, up to 1 week for complete approval.

### Q: Can I update my plugin after submission?
**A**: Yes! Simply submit a new PR with updated version information in `plugins.json` and any code changes.

### Q: What license should my plugin use?
**A**: We recommend MIT or Apache 2.0, but you can choose any open-source license.

### Q: My plugin isn't approved. What should I do?
**A**: Reviewers will provide feedback. Address the concerns and resubmit. Common issues include missing documentation or security concerns.

### Q: Can I submit multiple plugins?
**A**: Yes! Each plugin should have its own directory and entry in `plugins.json`.

### Q: How do I test my plugin locally?
**A**: Before development and testing, ensure the `nexus-open-cli` package is installed in your environment. If not, use `pip install nexus-open-cli`.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/PersonalViolet/NexusOpenCLI-plugins-registry/issues)
- **Email**: Contact the maintainers

## 📄 License

This registry is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Individual plugins may use different licenses - check each plugin's documentation.

---

**Happy Plugining!** 🎉

For more information about NexusOpenCLI, visit the [main repository](https://github.com/PersonalViolet/nexus-open-cli).

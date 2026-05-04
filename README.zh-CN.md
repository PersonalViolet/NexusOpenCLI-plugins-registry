# NexusOpenCLI 插件注册中心

[English](README.md) | 中文文档

欢迎来到 **NexusOpenCLI 插件注册中心**！本仓库是 [NexusOpenCLI](https://github.com/nexus-cli/nexus-open-cli) 的官方插件注册中心，开发者可以在此提交、发现和管理插件，以扩展 NexusOpenCLI 的功能。

## 📋 目录

- [概述](#概述)
- [插件提交指南](#插件提交指南)
- [目录结构](#目录结构)
- [提交流程](#提交流程)
- [插件配置](#插件配置)
- [审核流程](#审核流程)
- [示例：Doctor 插件](#示例doctor-插件)
- [贡献指南](#贡献指南)
- [常见问题](#常见问题)

## 🌟 概述

本注册中心允许社区开发者贡献插件，以增强 NexusOpenCLI 的功能。每个插件在添加到官方注册中心之前，都会经过仔细审核，以确保其质量、安全性和兼容性。

## 📝 插件提交指南

### 前置条件

在提交插件之前，请确保：

1. ✅ **已发布到 PyPI**：您的插件包必须已在 [PyPI](https://pypi.org/) 上发布并可用
2. ✅ **提供源代码**：在 `plugins/{plugin-name}` 目录中包含源代码（强烈推荐）
3. ✅ **完整文档**：提供 README.md 或 docs.md 文件说明您的插件
4. ✅ **GitHub 账号**：`plugins.json` 中的 author 字段将默认为您的 GitHub 用户名

### 基本要求

- 插件必须与 NexusOpenCLI 兼容
- 必须遵循 Python 打包标准
- 应包含适当的文档
- 必须通过安全审核

## 📁 目录结构

```
NexusOpenCLI-plugins-registry/
├── plugins.json              # 插件注册配置文件
├── README.md                 # 英文文档
├── README.zh-CN.md          # 中文文档（本文件）
└── plugins/                  # 插件目录
    └── {plugin-name}/       # 单个插件文件夹
        ├── README.md        # 插件文档（可选但推荐）
        ├── docs.md          # 替代文档文件
        ├── src/             # 源代码包（推荐）
        │   └── ...
        ├── pyproject.toml   # 构建配置（如果包含源码）
        └── ...              # 其他相关文件
```

### 结构示例

```
doctor/
├── docs.md                  # 插件文档
├── README.md                # 详细使用指南
├── src/                     # 源代码（可选但推荐）
│   └── ncli_doctor/
│       ├── __init__.py
│       └── plugin.py
└── pyproject.toml           # 包配置文件
```

## 🚀 提交流程

按照以下步骤提交您的插件：

### 步骤 1：发布到 PyPI

首先，确保您的插件已发布到 PyPI：

```bash
# 构建您的包
pip install build
python -m build

# 上传到 PyPI
pip install twine
twine upload dist/*
```

验证您的包是否可用：
```bash
pip install your-plugin-name
```

### 步骤 2：准备插件目录

在 `plugins/` 下创建一个以您插件命名的新目录：

```bash
mkdir plugins/your-plugin-name
```

### 步骤 3：添加文档

至少包含一个文档文件：
- `README.md` - 全面的插件文档
- `docs.md` - 替代文档格式

您的文档应包括：
- 插件概述和功能
- 安装说明
- 使用示例
- 配置选项
- API 参考（如适用）

### 步骤 4：包含源代码（推荐）

虽然不是必需的，但**强烈推荐**包含源代码，因为这样可以：

- 🔒 帮助审核员验证安全性和代码质量
- 👥 允许用户在安装前检查代码
- 🛠️ 使用户能够从源码安装（如果需要）
- 📚 为其他开发者提供参考实现

您可以包含：
- `src/` 目录中的完整源代码
- 用于构建的 `pyproject.toml` 或 `setup.py`
- 测试文件和示例

### 步骤 5：更新 plugins.json

将您的插件条目添加到 [`plugins.json`](plugins.json)：

```json
{
  "your-plugin-name": {
    "package": "nexus-open-cli-your-plugin",
    "version": "0.1.0",
    "description": "插件的简要描述",
    "author": "YourGitHubUsername"
  }
}
```

**注意**：`author` 字段将在审核批准后设置为您的 GitHub 用户名。

### 步骤 6：提交 Pull Request

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/add-your-plugin`
3. 提交您的更改：`git commit -m 'Add your-plugin-name'`
4. 推送到您的 fork：`git push origin feature/add-your-plugin`
5. 打开 Pull Request，包括：
   - 清晰的插件描述
   - PyPI 包链接
   - 任何特殊注意事项

## ⚙️ 插件配置

### plugins.json 架构

`plugins.json` 中的每个插件条目应包括：

| 字段          | 类型   | 必需 | 描述                                    |
|---------------|--------|------|-----------------------------------------|
| `package`     | string | 是   | PyPI 包名                              |
| `version`     | string | 是   | 当前版本（语义化版本格式）               |
| `description` | string | 是   | 简要描述（最多 200 个字符）              |
| `author`      | string | 自动 | GitHub 用户名（审核期间设置）            |

### 配置示例

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

## 🔍 审核流程

我们的审核团队将根据以下标准评估您的提交：

### 安全检查
- ✅ 无恶意代码或后门
- ✅ 无硬编码的秘密或凭证
- ✅ 依赖项安全
- ✅ 适当的错误处理

### 质量检查
- ✅ 代码遵循 Python 最佳实践
- ✅ 文档充分
- ✅ 正确的版本管理
- ✅ 清晰的插件目的和功能

### 兼容性检查
- ✅ 与当前 NexusOpenCLI 版本兼容
- ✅ 无冲突的依赖项
- ✅ 正确的插件接口实现

## 📖 示例：Doctor 插件

[`doctor`](plugins/doctor/) 插件作为参考实现：

### 功能特性
- ✅ Git 仓库检查
- 📄 README 检测
- 📜 License 验证
- 🚫 .gitignore 验证
- 📁 项目结构分析
- 📦 大文件检测
- 🔗 依赖文件检查
- 🧪 测试覆盖率评估

### 文档
- 查看 [`plugins/doctor/README.md`](plugins/doctor/README.md) 获取完整文档
- 包括安装、使用和开发指南

### 源代码
- 源代码可以包含在插件目录中
- 帮助用户了解实现细节

## 🤝 贡献指南

我们欢迎贡献！以下是您可以提供帮助的方式：

### 提交插件
按照上面的 [提交流程](#-提交流程) 操作。

### 改进文档
- 修复拼写错误或不清楚的解释
- 添加翻译
- 改进示例

### 审核插件
帮助审核其他开发者的提交。

### 报告问题
发现问题？创建一个 issue！

## ❓ 常见问题

### Q：我需要包含源代码吗？
**A**：虽然不是必需的，但**强烈建议**。包含源代码有助于审核员验证安全性，并允许用户在安装前检查代码。

### Q：审核需要多长时间？
**A**：通常初步审核需要 1-3 个工作日，完全批准最多需要 1 周时间。

### Q：提交后可以更新我的插件吗？
**A**：可以！只需提交一个新的 PR，在 `plugins.json` 中更新版本信息以及任何代码更改。

### Q：我的插件应该使用什么许可证？
**A**：我们推荐 MIT 或 Apache 2.0，但您可以选择任何开源许可证。

### Q：我的插件未获批准怎么办？
**A**：审核员会提供反馈。解决问题后重新提交。常见问题包括缺少文档或安全问题。

### Q：我可以提交多个插件吗？
**A**：可以！每个插件应该有自己的目录和 `plugins.json` 中的条目。

### Q：如何在本地测试我的插件？
**A**：开发和测试前确保当前环境有`nexus-open-cli`包，若没有，使用`pip install nexus-open-cli`。

## 📞 支持

- **Issues**：[GitHub Issues](https://github.com/PersonalViolet/NexusOpenCLI-plugins-registry/issues)
- **电子邮件**：联系维护者

## 📄 许可证

本注册中心采用 MIT 许可证。详情请见 [LICENSE](LICENSE)。

单个插件可能使用不同的许可证 - 请查看每个插件的文档。

---

**祝您插件开发愉快！** 🎉

有关 NexusOpenCLI 的更多信息，请访问 [主仓库](https://github.com/PersonalViolet/nexus-open-cli)。

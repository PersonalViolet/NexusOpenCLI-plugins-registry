from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Sequence

import typer
from babel.core import Locale
from babel.support import Translations
from rich.console import Console
from rich.table import Table
from rich.text import Text

from nexuscli.core.plugin_contract import CliPluginBase, CommandMetadata

Status = Literal["pass", "fail", "warn"]


@dataclass(frozen=True)
class RuleResult:
    id: str
    description: str
    status: Status
    score: int
    message: str


@dataclass(frozen=True)
class FileInfo:
    path: Path
    size_bytes: int


@dataclass(frozen=True)
class ProjectContext:
    root: Path
    file_count: int
    large_files: tuple[FileInfo, ...]
    top_files: tuple[FileInfo, ...]
    project_types: tuple[str, ...]
    dependency_files: tuple[str, ...]
    has_tests: bool


class DoctorPlugin(CliPluginBase):
    def __init__(self) -> None:
        self._: Callable[[str], str] = lambda message: message
        self._app: typer.Typer | None = None
        self.loaded_context: dict[str, Any] | None = None
        self.last_error: str | None = None

    @property
    def metadata(self) -> CommandMetadata:
        return CommandMetadata(
            plugin_id="byteknight.doctor",
            command_name="doctor",
            command_group=None,
            help_text=self._("Project health check report."),
            version="0.1.0",
            min_cli_version=">=0.1.0",
            dependencies=(
                "typer>=0.12,<1.0",
                "rich>=13,<14",
                "babel>=2.12,<3.0",
            ),
        )

    @property
    def typer_app(self) -> typer.Typer:
        return self._app

    def on_configure(self, context: dict[str, Any]) -> None:
        language = context.get("language", "en")
        locale = Locale.parse(language.replace("-", "_"))
        locales_dir = Path(__file__).resolve().parent / "locales"
        try:
            translations = Translations.load(
                str(locales_dir), locales=[str(locale)], domain="messages"
            )
        except OSError:
            return
        self._ = translations.gettext

    def build_app(self) -> typer.Typer:
        _ = self._
        self._app = typer.Typer(help=_("Project health doctor commands."))

        @self._app.command("doctor", help=_("Generate a project health report."))
        def doctor(
            path: Path = typer.Option(
                Path("."),
                "--path",
                exists=True,
                file_okay=False,
                dir_okay=True,
                readable=True,
                help=_("Target project path."),
            ),
            verbose: bool = typer.Option(
                False, "--verbose", help=_("Show detailed report output.")
            ),
        ) -> None:
            context = analyze_project(path)
            results = evaluate_rules(context, _)
            render_report(context, results, verbose, _)

        return self._app

    def on_load(self, context: dict[str, Any]) -> None:
        self.loaded_context = context

    def on_error(self, error: Exception) -> None:
        self.last_error = str(error)


def analyze_project(root: Path) -> ProjectContext:
    resolved_root = root.resolve()
    files = list(iter_project_files(resolved_root))
    file_count = len(files)
    file_infos = [FileInfo(path=item, size_bytes=item.stat().st_size) for item in files]
    file_infos.sort(key=lambda info: info.size_bytes, reverse=True)
    top_files = tuple(file_infos[:3])
    large_files = tuple(
        info for info in file_infos if info.size_bytes > 10 * 1024 * 1024
    )
    project_types, dependency_files = detect_project_types(resolved_root)
    has_tests = (resolved_root / "tests").is_dir()
    return ProjectContext(
        root=resolved_root,
        file_count=file_count,
        large_files=large_files,
        top_files=top_files,
        project_types=project_types,
        dependency_files=dependency_files,
        has_tests=has_tests,
    )


def iter_project_files(root: Path) -> Iterable[Path]:
    ignore_dirs = {".git", ".venv", "__pycache__"}
    for current, dirs, files in os.walk(root):
        dirs[:] = [item for item in dirs if item not in ignore_dirs]
        for file_name in files:
            yield Path(current) / file_name


def detect_project_types(root: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    mapping = {
        "Python": ("requirements.txt", "pyproject.toml"),
        "Node": ("package.json",),
        "Java": ("pom.xml",),
    }
    types: list[str] = []
    dependency_files: list[str] = []
    for project_type, markers in mapping.items():
        for marker in markers:
            if (root / marker).is_file():
                types.append(project_type)
                dependency_files.append(marker)
                break
    return tuple(types), tuple(dependency_files)


def evaluate_rules(context: ProjectContext, translate: Callable[[str], str]) -> list[RuleResult]:
    return [
        rule_git(context, translate),
        rule_readme(context, translate),
        rule_license(context, translate),
        rule_gitignore(context, translate),
        rule_structure(context, translate),
        rule_large_files(context, translate),
        rule_dependency_files(context, translate),
        rule_tests(context, translate),
    ]


def rule_git(context: ProjectContext, translate: Callable[[str], str]) -> RuleResult:
    has_git = (context.root / ".git").is_dir()
    return build_result(
        "git",
        translate("Git repo initialized"),
        has_git,
        20,
        translate("Git repo initialized"),
        translate("No .git directory"),
    )


def rule_readme(context: ProjectContext, translate: Callable[[str], str]) -> RuleResult:
    has_readme = (context.root / "README.md").is_file()
    return build_result(
        "readme",
        translate("README.md present"),
        has_readme,
        15,
        translate("README.md present"),
        translate("No README.md"),
    )


def rule_license(context: ProjectContext, translate: Callable[[str], str]) -> RuleResult:
    has_license = (context.root / "LICENSE").is_file()
    return build_result(
        "license",
        translate("LICENSE present"),
        has_license,
        10,
        translate("LICENSE present"),
        translate("No LICENSE"),
    )


def rule_gitignore(context: ProjectContext, translate: Callable[[str], str]) -> RuleResult:
    has_gitignore = (context.root / ".gitignore").is_file()
    return build_result(
        "gitignore",
        translate(".gitignore present"),
        has_gitignore,
        10,
        translate(".gitignore present"),
        translate("No .gitignore"),
    )


def rule_structure(context: ProjectContext, translate: Callable[[str], str]) -> RuleResult:
    is_reasonable = context.file_count < 1000
    return build_result(
        "structure",
        translate("Project structure reasonable"),
        is_reasonable,
        15,
        translate("File count within 1000"),
        translate("Too many files"),
        fail_status="warn",
    )


def rule_large_files(context: ProjectContext, translate: Callable[[str], str]) -> RuleResult:
    no_large_files = len(context.large_files) == 0
    return build_result(
        "large_files",
        translate("No large files"),
        no_large_files,
        10,
        translate("No large files detected"),
        translate("Large files detected"),
        fail_status="warn",
    )


def rule_dependency_files(
    context: ProjectContext, translate: Callable[[str], str]
) -> RuleResult:
    has_dependency = len(context.dependency_files) > 0
    return build_result(
        "dependencies",
        translate("Dependency file detected"),
        has_dependency,
        10,
        translate("Dependency file detected"),
        translate("No dependency file found"),
    )


def rule_tests(context: ProjectContext, translate: Callable[[str], str]) -> RuleResult:
    return build_result(
        "tests",
        translate("Tests folder present"),
        context.has_tests,
        10,
        translate("Tests folder present"),
        translate("No tests folder"),
    )


def build_result(
    rule_id: str,
    description: str,
    passed: bool,
    score: int,
    pass_message: str,
    fail_message: str,
    *,
    fail_status: Status = "fail",
) -> RuleResult:
    if passed:
        return RuleResult(
            id=rule_id,
            description=description,
            status="pass",
            score=score,
            message=pass_message,
        )
    return RuleResult(
        id=rule_id,
        description=description,
        status=fail_status,
        score=0,
        message=fail_message,
    )


def render_report(
    context: ProjectContext,
    results: Sequence[RuleResult],
    verbose: bool,
    translate: Callable[[str], str],
) -> None:
    console = Console()
    console.print(Text(translate("Project Health Report"), style="bold"))

    for result in results:
        console.print(format_result(result))

    score = sum(result.score for result in results)
    console.print(Text(f"{translate('Score')}: {score}/100", style="bold"))

    if context.top_files:
        console.print(Text(translate("Top 3 largest files"), style="bold"))
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column(translate("File"))
        table.add_column(translate("Size"), justify="right")
        for info in context.top_files:
            table.add_row(str(info.path.relative_to(context.root)), human_size(info.size_bytes))
        console.print(table)

    if verbose:
        console.print(Text(translate("Details"), style="bold"))
        console.print(f"{translate('Root')}: {context.root}")
        console.print(f"{translate('File count')}: {context.file_count}")
        if context.project_types:
            console.print(
                f"{translate('Project types')}: {', '.join(context.project_types)}"
            )
        if context.dependency_files:
            console.print(
                f"{translate('Dependency files')}: {', '.join(context.dependency_files)}"
            )
        if context.large_files:
            console.print(translate("Large files"))
            for info in context.large_files:
                console.print(
                    f"- {info.path.relative_to(context.root)} ({human_size(info.size_bytes)})"
                )


def format_result(result: RuleResult) -> Text:
    symbol_map: dict[Status, str] = {"pass": "✓", "fail": "✗", "warn": "⚠"}
    style_map: dict[Status, str] = {"pass": "green", "fail": "red", "warn": "yellow"}
    symbol = symbol_map[result.status]
    style = style_map[result.status]
    return Text(f"{symbol} {result.message}", style=style)


def human_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    units = ["KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    for unit in units:
        size /= 1024.0
        if size < 1024.0:
            return f"{size:.1f} {unit}"
    return f"{size:.1f} PB"

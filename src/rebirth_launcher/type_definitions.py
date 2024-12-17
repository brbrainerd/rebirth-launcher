"""Type stubs for external libraries."""
from typing import Any, Protocol

# Rich types
class RichConsole(Protocol):
    """Protocol for Rich console interface."""
    def print(self, *args: Any, **kwargs: Any) -> None: ...

class ProgressColumn(Protocol):
    """Protocol for Rich progress column."""

class SpinnerColumn(ProgressColumn):
    """Protocol for Rich spinner column."""

class TextColumn(ProgressColumn):
    """Protocol for Rich text column."""

class BarColumn(ProgressColumn):
    """Protocol for Rich progress bar column."""

class TaskProgressColumn(ProgressColumn):
    """Protocol for Rich task progress column."""

class Progress(Protocol):
    """Protocol for Rich progress interface."""
    def add_task(self, description: str, total: float | None = None) -> int: ...
    def update(self, task_id: int, completed: float | None = None) -> None: ...
    def __enter__(self) -> "Progress": ...
    def __exit__(self, *args: Any) -> None: ...

class Confirm(Protocol):
    """Protocol for Rich confirm interface."""
    @staticmethod
    def ask(prompt: str) -> bool: ...

# Typer types
class Option(Protocol):
    """Protocol for Typer option interface."""
    def __call__(self, default: Any, *args: Any, **kwargs: Any) -> Any: ...

class Command(Protocol):
    """Protocol for Typer command interface."""
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

class Typer(Protocol):
    """Protocol for Typer interface."""
    def command(self) -> Command: ...
    Option: Option
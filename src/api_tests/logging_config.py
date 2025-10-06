import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(level: int = logging.INFO, console: Optional[Console] = None) -> None:
	console = console or Console(force_terminal=True)
	handler = RichHandler(console=console, rich_tracebacks=True, markup=True, show_path=False)
	logging.basicConfig(
		level=level,
		format="%(message)s",
		handlers=[handler],
	)

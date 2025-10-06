.PHONY: venv install test lint clean report open

PYTHON ?= python3
VENV ?= .venv
ACTIVATE = . $(VENV)/bin/activate

venv:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE); pip install --upgrade pip

install: venv
	$(ACTIVATE); pip install -r requirements.txt

test:
	$(ACTIVATE); pytest

report:
	@echo "Report generated at reports/report.html"

open:
	@python -c "import webbrowser, os; p=os.path.abspath('reports/report.html'); print('Opening', p); webbrowser.open('file://' + p)"

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache .mypy_cache reports

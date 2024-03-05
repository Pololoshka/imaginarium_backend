fix:
	ruff format game src user tests
	ruff check --fix --show-fixes game src user tests

check:
	ruff format --check game src user tests
	ruff check game src user tests
	mypy game src user tests
	pytest tests

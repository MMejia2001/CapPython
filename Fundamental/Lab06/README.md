## Setup
- Python 3.12
- Poetry

## Install
poetry install

## Quality tools
poetry run isort .
poetry run black .
poetry run ruff check . --fix
poetry run pre-commit run --all-files --config .pre-commit-config.yaml

## Ejecutar solo este lab
Desde la raíz del repositorio:

poetry -C Fundamental/Lab06 run pre-commit run --all-files --config Fundamental/Lab06/.pre-commit-config.yaml

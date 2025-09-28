
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install poetry pytest pytest-cov

poetry config virtualenvs.create false
poetry install --no-interaction --no-ansi --with dev

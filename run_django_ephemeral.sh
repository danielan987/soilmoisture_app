#!/usr/bin/env bash
set -euo pipefail

# Config: adjust if your project path changes
PROJECT_DIR="/Users/daniel/Desktop/Python/Projects/ML/soilmoisture_site"
HOST="127.0.0.1"

# 1) Go to project directory
cd "$PROJECT_DIR"

# 2) Ensure expected files/dirs exist
if [[ ! -f "manage.py" ]]; then
  echo "Error: manage.py not found in $PROJECT_DIR"
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Error: .venv not found in $PROJECT_DIR"
  echo "Create it first, e.g.: python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

# 3) Activate virtual environment (works in bash/zsh/sh)
# shellcheck disable=SC1091
. ".venv/bin/activate"

# Deactivate venv on exit
trap 'deactivate >/dev/null 2>&1 || true' EXIT

# 4) Find a free ephemeral port using Python stdlib
PORT="$(python - <<'PY'
import socket
s = socket.socket()
s.bind(('', 0))
print(s.getsockname()[1])
s.close()
PY
)"

echo "Using port ${PORT}"

# 5) Run Django development server on that port
exec python manage.py runserver "${HOST}:${PORT}"


# chmod +x /Users/daniel/Desktop/Python/Projects/ML/soilmoisture_site/run_django_ephemeral.sh

# /Users/daniel/Desktop/Python/Projects/ML/soilmoisture_site/run_django_ephemeral.sh
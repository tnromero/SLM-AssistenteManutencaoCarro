
#!/usr/bin/env bash

{
  echo "===== PROJECT STRUCTURE ====="
  tree -a -I '.git|.venv|__pycache__|.pytest_cache|.ruff_cache|*.pyc|uv.lock'
  echo
  echo "===== FILE CONTENT ====="

  find . \
    -type f \
    \( -name "*.py" -o -name "*.toml" -o -name "*.csv" -o -name "*.json" -o -name "*.md" \) \
    ! -path "./.venv/*" \
    ! -path "./.git/*" \
    ! -path "*/__pycache__/*" \
    ! -path "*/.pytest_cache/*" \
    ! -path "*/.ruff_cache/*" \
    -print0 |
  while IFS= read -r -d '' file; do
    echo
    echo "============================================================"
    echo "FILE: $file"
    echo "============================================================"
    cat "$file"
  done
} > project_context.txt

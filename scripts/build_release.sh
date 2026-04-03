#!/usr/bin/env bash
# build_release.sh — Build e verifica release do GuruDev®
set -euo pipefail

VERSION=$(python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); print(d['project']['version'])" 2>/dev/null || \
          python -c "import tomli; d=tomli.load(open('pyproject.toml','rb')); print(d['project']['version'])" 2>/dev/null || \
          grep '^version' pyproject.toml | head -1 | sed 's/.*= *"\(.*\)"/\1/')

echo "╔══════════════════════════════════════════╗"
echo "║   GuruDev® Release Build                 ║"
echo "╚══════════════════════════════════════════╝"
echo "  Version: $VERSION"
echo ""

# 1. Run full test suite
echo "▶ Running tests..."
pytest tests/ -v --tb=short
echo "  ✓ All tests passed"
echo ""

# 2. Lint (if ruff is available)
if command -v ruff &>/dev/null; then
    echo "▶ Linting..."
    ruff check src/ tests/
    echo "  ✓ Lint passed"
    echo ""
fi

# 3. Build distribution
echo "▶ Building distribution..."
pip install build -q
python -m build --wheel --sdist
echo "  ✓ Built dist/"
ls dist/
echo ""

echo "✅ Release build complete: gurudev-lang $VERSION"
echo ""
echo "To upload to PyPI (requires credentials):"
echo "  twine upload dist/*"

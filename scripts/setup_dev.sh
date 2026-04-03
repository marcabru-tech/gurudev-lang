#!/usr/bin/env bash
# setup_dev.sh — Configura o ambiente de desenvolvimento GuruDev®
set -euo pipefail

echo "╔══════════════════════════════════════════╗"
echo "║   GuruDev® Dev Setup                     ║"
echo "╚══════════════════════════════════════════╝"

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python $PYTHON_VERSION detected"

# Install in editable mode with dev dependencies
echo ""
echo "▶ Installing gurudev-lang[dev]..."
pip install -e ".[dev]"

# Verify installation
echo ""
echo "▶ Verifying installation..."
python -c "from compiler.lexer import Lexer; print('  ✓ compiler.lexer')"
python -c "from runtime.gurudvm import GuruDVM; print('  ✓ runtime.gurudvm')"
python -c "from gurumatrix.core import GuruMatrix; print('  ✓ gurumatrix.core')"
python -c "from gurudev.exceptions import GuruDevError; print('  ✓ gurudev.exceptions')"

# Run tests
echo ""
echo "▶ Running test suite..."
pytest tests/ -v --tb=short

echo ""
echo "✅ Dev environment ready!"
echo ""
echo "Quick start:"
echo "  gurudev build examples/mvp_demo.guru"
echo "  gurudev run examples/mvp_demo.guru --hermeneutica 4"
echo "  gurudev examples/mvp_demo.guru --demo"

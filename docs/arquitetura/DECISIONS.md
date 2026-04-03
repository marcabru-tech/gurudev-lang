# Architecture Decisions — GuruDev®

This document records architecture decisions made during the development of GuruDev®. When faced with ambiguity, the simplest viable option is chosen and documented here.

---

## ADR-001: src/ Layout

**Date:** April 2026  
**Status:** Accepted

**Context:** Source packages could be at the root level or under `src/`.

**Decision:** Use `src/` layout with hatchling as build backend.

**Rationale:**
- Standard Python project practice (PEP 517 + PEP 660)
- Prevents accidental imports of uninstalled code during testing
- Aligns with the project specification

**Consequence:** All packages are under `src/`. Tests use `pythonpath = ["src"]` in pytest config.

---

## ADR-002: CLI naming — Option A (rename with underscore)

**Date:** April 2026  
**Status:** Accepted

**Context:** The original CLI file was `gurudev-cli.py` (hyphen), which is not importable as a Python module.

**Decision:** Rename to `gurudev_cli.py` (underscore) under `src/cli/`.

**Rationale:**
- Python module names cannot contain hyphens
- Option A (rename) is simpler and cleaner than a wrapper module
- The `gurudev.cli` entry point (from `src/gurudev/cli.py`) is preserved for `gurudev = "gurudev.cli:main"`

**Consequence:** Two CLI entry points exist:
- `gurudev` → `gurudev.cli:main` (Click + Rich interface)
- `gurudev-cli` → `cli.gurudev_cli:main` (argparse interface)

---

## ADR-003: GuruByte as JSON

**Date:** April 2026  
**Status:** Accepted (MVP only)

**Context:** The GuruByte format could be binary (compact) or JSON (readable).

**Decision:** Use JSON for MVP.

**Rationale:** Simplicity and debuggability for MVP. Binary encoding is planned for v0.2.

**Consequence:** `.gurub` files are human-readable JSON. Larger than binary but easier to inspect.

---

## ADR-004: Keep root-level packages as compatibility layer

**Date:** April 2026  
**Status:** Accepted (temporary)

**Context:** Existing code and tests used root-level packages (`compiler/`, `runtime/`, `gurumatrix/`).

**Decision:** Move canonical code to `src/`, keep root packages as compatibility shims (or remove them once all imports are updated).

**Rationale:** Gradual migration reduces breakage risk.

**Consequence:** Tests use `pythonpath = ["src"]`; imports resolve to `src/` packages.

---

## ADR-005: No heavy dependencies in core

**Date:** April 2026  
**Status:** Accepted

**Context:** Several ML/NLP libraries could enhance GuruMatrix (numpy, sentence-transformers, etc.).

**Decision:** Core dependencies are only `click`, `pydantic`, `rich`. Numpy is optional.

**Rationale:** Keep the core installable in any Python environment without heavy prerequisites.

# GuruCompiler Specification

**Status:** Draft  
**Date:** April 2026

---

## Overview

The **GuruCompiler** transforms `.guru` source files into **GuruByte** (`.gurub`) artifacts through a pipeline:

```
Source (.guru) → Lexer → Tokens → Parser → AST → ContextAnalyzer → BytecodeGenerator → GuruByte (.gurub)
```

---

## Pipeline Stages

### 1. Lexer (`src/compiler/lexer.py`)

Transforms raw source text into a flat list of `Token` objects.

**Input:** `str`  
**Output:** `List[Token]`

Supported token types: identifiers, numbers, strings, keywords, operators, delimiters, comments (skipped), newlines.

### 2. Parser (`src/compiler/parser.py`)

Transforms the token stream into a **GuruAST** (Abstract Syntax Tree).

**Input:** `List[Token]`  
**Output:** `Programa` (root AST node)

Key AST node types:
- `Programa` — root
- `BindClave` — `bind clave = X`
- `TagHermeneutica` — `tag hermeneutica = N`
- `Instrucao` — `load`, `display`, `evaluate`, etc.
- `DispatchHermeneutica` — `dispatch hermeneutica X { ... }`
- `FuncaoDecl` — function definition

### 3. Context Analyzer (`src/compiler/context_analyzer.py`)

Propagates semantic context (clave, hermeneutica, ontologia) through the AST. Annotates each node with its resolved context. Generates a **dry-run report** with gap analysis.

**Input:** `Programa`  
**Output:** annotated AST (in-place); `relatorio_dry_run()` dict

### 4. Bytecode Generator (`src/compiler/bytecode_gen.py`)

Transforms the annotated AST into a **GuruByte** dict structure.

**Input:** `Programa`  
**Output:** `dict` (GuruByte format)

---

## GuruByte Format

See [GURUBYTE_SPEC.md](GURUBYTE_SPEC.md) for the full specification.

---

## Error Handling

- `LexerError` — unexpected character during tokenization
- `ParserError` — unexpected token during parsing
- `SemanticError` — semantic analysis failure

All errors extend `GuruDevError` from `src/gurudev/exceptions.py`.

---

## Future Work

- Optimization passes (constant folding, dead-code elimination)
- Type inference
- Source maps for debugging
- Incremental compilation

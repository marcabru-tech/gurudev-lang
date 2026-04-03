# GuruByte Specification

**Status:** Draft  
**Date:** April 2026

---

## Overview

**GuruByte** (`.gurub`) is the intermediate representation produced by the GuruCompiler. It is a JSON-serializable dict that the **GuruDVM** executes.

---

## Format

```json
{
  "HEADER": {
    "version": "0.1",
    "source": "<filename>",
    "timestamp": "<ISO 8601>",
    "checksum": "<sha256-hex>"
  },
  "CONTEXT_DEFAULT": {
    "clave": "geral",
    "hermeneutics": 1,
    "ontologia": "SUBSTANCIA"
  },
  "CODEBLOCKS": [
    {
      "type": "INSTRUCOES",
      "CONTEXT": {},
      "instructions": [
        {
          "opcode": "LOAD",
          "operandos": ["formula_energia"],
          "modificadores": {},
          "contexto_hermeneutica": 1,
          "contexto_clave": "ciencia",
          "linha": 3
        }
      ]
    },
    {
      "type": "DISPATCH_ON_HERMENEUTICS",
      "recurso": "formula_energia",
      "CONTEXT": {},
      "casos": {
        "1": [ { "opcode": "DISPLAY", "modificadores": {"in_context": true}, ... } ],
        "4": [ { "opcode": "DISPLAY", ... } ],
        "7": [ { "opcode": "DISPLAY", ... } ]
      },
      "default": [ { "opcode": "DISPLAY", ... } ]
    }
  ]
}
```

---

## HEADER

| Field       | Type   | Description                          |
|-------------|--------|--------------------------------------|
| `version`   | string | GuruByte format version              |
| `source`    | string | Source file path                     |
| `timestamp` | string | Compilation timestamp (ISO 8601)     |
| `checksum`  | string | SHA-256 of source code (hex)         |

---

## CONTEXT_DEFAULT

Provides the execution context defaults. Can be overridden at the codeblock level.

---

## CODEBLOCKS

An ordered list of code blocks. Each block has a `type`:

| Type                     | Description                                      |
|--------------------------|--------------------------------------------------|
| `INSTRUCOES`             | Sequential instruction block                     |
| `DISPATCH_ON_HERMENEUTICS` | Hermeneutic dispatch block                     |
| `FUNCTION`               | Function definition block                        |

---

## Instruction Format

Each instruction is a dict with:

| Field                    | Type   | Description                              |
|--------------------------|--------|------------------------------------------|
| `opcode`                 | string | Instruction opcode (see instruction set) |
| `operandos`              | list   | Positional operands                      |
| `modificadores`          | dict   | Named modifiers/flags                    |
| `contexto_hermeneutica`  | int    | Hermeneutic level at compile time        |
| `contexto_clave`         | string | Clave at compile time                    |
| `linha`                  | int    | Source line number                       |

---

## File Extension

GuruByte files use the `.gurub` extension and are stored by default in `.gurudev/` next to the source file.

---

## Future Work

- Binary encoding (MessagePack / custom)
- Versioned format with migration support
- Digital signatures for artifact integrity

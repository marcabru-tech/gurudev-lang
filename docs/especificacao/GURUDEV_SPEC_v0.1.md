# GuruDev® Specification v0.1

**Status:** Draft  
**Date:** April 2026  
**Author:** Guilherme Gonçalves Machado / Hubstry

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Design Principles](#2-design-principles)
3. [Lexical Structure](#3-lexical-structure)
4. [Type System](#4-type-system)
5. [Semantic Context Model](#5-semantic-context-model)
6. [Hermeneutic Dispatch](#6-hermeneutic-dispatch)
7. [Standard Instructions](#7-standard-instructions)
8. [Modules and Loading](#8-modules-and-loading)
9. [Grammar Reference](#9-grammar-reference)
10. [Appendix](#10-appendix)

---

## 1. Introduction

GuruDev® is a **semantic programming language** designed to produce computationally distinct outputs from the same instruction, depending on the active *hermeneutic level* (1–7). This is not a decorative annotation system — the language guarantees that identical code executed at different hermeneutic levels produces structurally and computationally different outputs.

### 1.1 Objectives

- Represent knowledge across multiple epistemological registers simultaneously.
- Enable programs that adapt their behavior based on semantic context.
- Support multimodal computation: literal, contextual, and ontological.

### 1.2 Non-Objectives

- GuruDev® is not a general-purpose systems programming language.
- GuruDev® does not aim to replace existing languages but to complement them for semantic computing tasks.

---

## 2. Design Principles

1. **Semantic Distinctiveness**: The same instruction must produce computationally distinct outputs at different hermeneutic levels.
2. **Ontological Grounding**: All resources are grounded in the GuruMatrix coordinate system (Aristotle × Domains).
3. **Controlled Ambiguity**: Ambiguity is not an error — it is a feature exploited by the hermeneutic dispatch.
4. **Minimalism**: The core language is intentionally small; complexity lives in the semantic model.

---

## 3. Lexical Structure

### 3.1 Keywords

```
def  bind  tag  load  dispatch  case  default
display  evaluate  transcode  emote  in  context
hermeneutica  clave  map  on
```

### 3.2 Identifiers

Identifiers match the pattern `[a-zA-Z_][a-zA-Z0-9_]*`.

### 3.3 Literals

- **Numbers**: `42`, `3.14`
- **Strings**: `"hello world"` (double-quote delimited, with escape sequences)

### 3.4 Comments

- `# comment` — single-line comment
- `// comment` — single-line comment (C-style alias)

---

## 4. Type System

*TBD — GuruDev® v0.2*

---

## 5. Semantic Context Model

Every instruction executes within a **semantic context** consisting of:

- `clave` — the active knowledge domain (e.g., `ciencia`, `arte`, `filosofia`)
- `hermeneutics` — the active hermeneutic level (1–7)
- `ontologia` — the Aristotelian category (e.g., `SUBSTANCIA`, `RELACAO`)

---

## 6. Hermeneutic Dispatch

See [GURUMATRIX_SPEC.md](GURUMATRIX_SPEC.md) for the coordinate system.

The `dispatch hermeneutica` construct routes execution to a `case` body based on the current hermeneutic level:

```guru
dispatch hermeneutica <resource> {
    case 1: <instructions>
    case 4: <instructions>
    case 7: <instructions>
    default: <instructions>
}
```

Level semantics:

| Level | Mode        |
|-------|-------------|
| 1     | LITERAL     |
| 2     | ALEGÓRICO   |
| 3     | TÉCNICO     |
| 4     | CONTEXTUAL  |
| 5     | COMPARATIVO |
| 6     | ANALÓGICO   |
| 7     | ONTOLÓGICO  |

---

## 7. Standard Instructions

| Instruction          | Description                                          |
|----------------------|------------------------------------------------------|
| `bind clave = X`     | Set the semantic clave                               |
| `tag hermeneutica = N` | Set the hermeneutic level                          |
| `load <resource>`    | Load a resource into the execution context           |
| `display in context` | Display the top resource according to hermeneutic level |
| `evaluate <resource>` | Evaluate a resource (numeric, symbolic, or ontological) |
| `transcode <r> to X` | Transcode a resource to domain X                    |

---

## 8. Modules and Loading

*TBD — GuruDev® v0.2*

---

## 9. Grammar Reference

*TBD — Formal BNF grammar will be added in v0.2*

---

## 10. Appendix

### A. Reserved Words

All keywords listed in §3.1 are reserved.

### B. Version History

| Version | Date       | Notes              |
|---------|------------|--------------------|
| 0.1     | April 2026 | Initial draft      |

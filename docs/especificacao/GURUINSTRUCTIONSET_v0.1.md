# GuruDev® Instruction Set v0.1

**Status:** Draft  
**Date:** April 2026

---

## Overview

The GuruDev® instruction set defines the opcodes understood by the **GuruDVM** (GuruDev Virtual Machine). Instructions are encoded in **GuruByte** format and executed in a context-dependent manner.

---

## Core Instructions

### `BIND`

Sets the active semantic clave.

**Syntax:** `bind clave = <identifier>`  
**Effect:** Updates `context.clave`

---

### `TAG`

Sets the active hermeneutic level.

**Syntax:** `tag hermeneutica = <N>`  
**Effect:** Updates `context.hermeneutics` to N (1–7)

---

### `LOAD`

Loads a named resource onto the execution stack.

**Syntax:** `load <resource_name>`  
**Effect:** Pushes `{nome, valor}` onto the stack. If the resource is not registered, uses `<resource:name>` as placeholder.

---

### `DISPLAY`

Displays the top-of-stack resource according to the current hermeneutic level.

**Syntax:** `display in context`  
**Effect:** Calls `_render_por_hermeneutica(nome, valor, level, clave)` and records output.

Output per level:

| Level | Mode        | Output type               |
|-------|-------------|---------------------------|
| 1     | LITERAL     | `str`                     |
| 2     | ALEGÓRICO   | `dict` with type info     |
| 3     | TÉCNICO     | `dict` with analysis      |
| 4     | CONTEXTUAL  | `dict` with GuruMatrix coord |
| 5     | COMPARATIVO | `dict` with semantic relations |
| 6     | ANALÓGICO   | `dict` with cross-domain analogies |
| 7     | ONTOLÓGICO  | `dict` with full expansion |

---

### `EVALUATE`

Evaluates the top-of-stack resource.

**Syntax:** `evaluate <resource_name>`  
**Modes:** `numeric` (levels 1–2), `symbolic` (levels 3–4), `ontological` (levels 5–7)

---

### `TRANSCODE`

Transcodes a resource to a different domain.

**Syntax:** `transcode <resource> to <domain>`  
**Effect:** Produces a transcoded representation recorded in output.

---

### `DISPATCH_ON_HERMENEUTICS`

Routes execution to a case body matching the current hermeneutic level.

**Syntax:**
```guru
dispatch hermeneutica <resource> {
    case N: <instructions>
    default: <instructions>
}
```

---

### `EMOTE`

*(Reserved for level 6+ — not yet implemented)*  
Produces an aesthetic/emotional expression of a resource.

---

### `MAP_TO`

Maps the current context to a new clave.

**Syntax:** `map clave = <identifier>` *(internal opcode: MAP_TO)*

---

## Instruction Encoding

All instructions are encoded as dicts in GuruByte format. See [GURUBYTE_SPEC.md](GURUBYTE_SPEC.md).

---

## Future Instructions (v0.2+)

- `INFER` — semantic inference from GuruMatrix relations
- `COMPOSE` — combine resources across domains
- `REFLECT` — introspective output about the execution context
- `CITE` — attach provenance metadata to a resource

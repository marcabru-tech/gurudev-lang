# GuruMatrix Specification

**Status:** Draft  
**Date:** April 2026  
**Author:** Guilherme Gonçalves Machado / Hubstry

---

## Overview

The **GuruMatrix** is a 10×10 semantic coordinate system that grounds all GuruDev® computations. It is structured as a product of:

- **Rows (Ontologia):** Aristotle's 10 Categories
- **Columns (Dominio):** 10 Knowledge Domains

Each cell `(Ontologia × Dominio)` represents a semantic region where objects, relations, and preferred instructions reside.

---

## Ontological Axes

### Ontologia (Rows)

| Value | Name       | Description                          |
|-------|------------|--------------------------------------|
| 1     | SUBSTANCIA | Primary substance; what a thing is   |
| 2     | QUANTIDADE | Quantity; measurable properties      |
| 3     | QUALIDADE  | Quality; attributes and characteristics |
| 4     | RELACAO    | Relation; connections between things |
| 5     | LUGAR      | Place; spatial localization          |
| 6     | TEMPO      | Time; temporal properties            |
| 7     | SITUACAO   | Situation; state or condition        |
| 8     | CONDICAO   | Condition; prerequisite states       |
| 9     | ACAO       | Action; processes and activities     |
| 10    | PAIXAO     | Passion; receptive properties        |

### Dominio (Columns)

| Value | Name                  |
|-------|-----------------------|
| 1     | ARTE                  |
| 2     | CIENCIA               |
| 3     | FILOSOFIA             |
| 4     | TRADICAO_ESPIRITUAL   |
| 5     | TECNOLOGIA            |
| 6     | LINGUAGEM             |
| 7     | MATEMATICA            |
| 8     | MEDICINA_BIOLOGIA     |
| 9     | DIREITO_ETICA         |
| 10    | EDUCACAO              |

---

## Cell Structure

Each cell `CelulaGuruMatrix(x: Ontologia, y: Dominio)` contains:

- `objetos: List[str]` — Named objects/concepts inhabiting this cell
- `relacoes_ativas: List[RelacaoSemantica]` — Active semantic relations
- `instrucoes_preferenciais: List[str]` — Preferred GuruDev® instructions
- `embedding: Optional[List[float]]` — Vector embedding (future use)

---

## Semantic Relations

| Relation      | Meaning                                              |
|---------------|------------------------------------------------------|
| SIMILITUDE    | Surface similarity between objects                   |
| HOMOLOGIA     | Structural correspondence across domains             |
| EQUIVALENCIA  | Functional equivalence in different contexts         |
| SIMETRIA      | Symmetric structural relationship                    |
| EQUILIBRIO    | Dynamic equilibrium between opposing forces          |
| COMPENSACAO   | Compensatory relationship                            |

---

## Coordinate Inference

When a resource is loaded with clave `ciencia`, it is mapped to `(ACAO, CIENCIA)` by default. This mapping can be overridden by explicit `tag` and `bind` instructions.

---

## Special Values

### Inefável (Beyond the Matrix)

Values that cannot be grounded in any cell emit a semantic warning: `"Inefável: beyond GuruMatrix coordinates"`. This is by design — some concepts resist categorization.

---

## Python API

```python
from gurumatrix.core import GuruMatrix, Ontologia, Dominio

matrix = GuruMatrix()
matrix.popular_minimo()

celula = matrix.get(Ontologia.ACAO, Dominio.CIENCIA)
print(celula.objetos)  # ['E=mc²', ...]
```

---

## Future Work

- Cell embeddings (dense vector representations)
- Dynamic relation discovery via semantic similarity
- Cross-matrix traversal algorithms
- GuruMatrix v2: 3D extension with temporal axis

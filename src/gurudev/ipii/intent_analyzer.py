"""
GuruDev IPII – IntentAnalyzer v0.1-beta
Infers semantic intent from canonical adapted blocks produced by BytecodeAdapterReal.

Three intents are supported:
  - calculo_numerico   : numeric/math computations (factorial, sums, means …)
  - formula_cientifica : scientific formula evaluation (physics, chemistry …)
  - despacho_multiplo  : hermeneutic dispatch patterns
"""
from __future__ import annotations

from dataclasses import dataclass

# ── Vocabulary hints per intent ───────────────────────────────────────────────

_HINTS_CALCULO = {
    "fatorial", "factorial", "soma", "sum", "media", "mean",
    "calcular", "calculo", "compute", "numero", "number",
    "raiz", "sqrt", "potencia", "pow", "produto", "product",
}

_HINTS_FORMULA = {
    "formula", "energia", "massa", "velocidade", "euler",
    "constante", "constantes", "fisica", "quimica", "ciencia",
    "science", "mc2", "equacao", "equation",
}

_HINTS_DESPACHO = {
    "dispatch", "despacho", "hermeneutica", "hermeneutics",
    "case", "caso", "multimodal", "multi",
}


def _extract_text(blocks: list) -> str:
    """Collect all string tokens from a list of canonical blocks for matching."""
    parts: list[str] = []
    for b in blocks:
        parts.append(str(b.get("nome", "")))
        parts.append(str(b.get("recurso", "")))
        for instr in b.get("instructions", []):
            parts.append(str(instr.get("opcode", "")))
            parts.extend(str(op) for op in instr.get("operandos", []))
        for sub in b.get("corpo", []):
            parts.append(_extract_text([sub]))
    return " ".join(parts).lower()


def _count_hits(text: str, vocab: set) -> int:
    return sum(1 for word in vocab if word in text)


def _has_dispatch(blocks: list) -> bool:
    for b in blocks:
        if b.get("kind") == "dispatch":
            return True
        for sub in b.get("corpo", []):
            if _has_dispatch([sub]):
                return True
    return False


def _infer_hermeneutics(blocks: list) -> int:
    """Return the first hermeneutics level found, defaulting to 4."""
    for b in blocks:
        h = b.get("context", {}).get("hermeneutics")
        if isinstance(h, int):
            return h
        for sub in b.get("corpo", []):
            h2 = _infer_hermeneutics([sub])
            if h2 != 4:
                return h2
    return 4


# ── Result ───────────────────────────────────────────────────────────────────


@dataclass
class Intent:
    name: str
    tags: str
    hermeneutics: int


_INTENT_META: dict[str, dict] = {
    "calculo_numerico": {"tags": "[ACAO][CIENCIA]"},
    "formula_cientifica": {"tags": "[ACAO][CIENCIA][FORMULA]"},
    "despacho_multiplo": {"tags": "[DESPACHO][HERMENEUTICA]"},
}


# ── Analyzer ─────────────────────────────────────────────────────────────────


class IntentAnalyzer:
    """Infer the dominant intent from a list of canonical adapted blocks."""

    def analyze(self, adapted_blocks: list) -> Intent:
        text = _extract_text(adapted_blocks)
        hermeneutics = _infer_hermeneutics(adapted_blocks)

        # Dispatch takes priority when explicit dispatch blocks exist
        if _has_dispatch(adapted_blocks):
            intent_name = "despacho_multiplo"
        else:
            scores = {
                "calculo_numerico": _count_hits(text, _HINTS_CALCULO),
                "formula_cientifica": _count_hits(text, _HINTS_FORMULA),
            }
            # Prefer 'calculo_numerico' on tie (including zero scores)
            intent_name = max(
                scores,
                key=lambda k: (scores[k], k == "calculo_numerico"),
            )

        meta = _INTENT_META[intent_name]
        return Intent(
            name=intent_name,
            tags=meta["tags"],
            hermeneutics=hermeneutics,
        )

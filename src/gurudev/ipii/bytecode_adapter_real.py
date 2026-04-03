"""
GuruDev IPII – BytecodeAdapterReal v0.1-beta
Adapts the real GuruByte CODEBLOCKS format produced by src/compiler/bytecode_gen.py
into a canonical representation that IPIIEngine can transpile.

Block types recognised:
  - FUNCTION          (nome, parametros, corpo)
  - DISPATCH_ON_HERMENEUTICS (recurso, casos, default)
  - plain instruction block   (instructions)
"""
from __future__ import annotations

from typing import Any


# ── Canonical data-classes (plain dicts with typed constructors) ─────────────


def _make_function(nome: str, parametros: list, corpo: list, context: dict) -> dict:
    return {
        "kind": "function",
        "nome": nome,
        "parametros": parametros,
        "corpo": corpo,
        "context": context,
    }


def _make_dispatch(recurso: str, casos: dict, default: Any, context: dict) -> dict:
    return {
        "kind": "dispatch",
        "recurso": recurso,
        "casos": casos,
        "default": default,
        "context": context,
    }


def _make_instruction_block(instructions: list, context: dict) -> dict:
    return {
        "kind": "instructions",
        "instructions": instructions,
        "context": context,
    }


# ── Adapter ─────────────────────────────────────────────────────────────────


class BytecodeAdapterReal:
    """Convert a raw GuruByte dict (from BytecodeGenerator) into canonical blocks."""

    def adapt(self, gurubyte: dict) -> list:
        """Return a list of canonical block dicts."""
        codeblocks = gurubyte.get("CODEBLOCKS", [])
        return [self._adapt_block(b) for b in codeblocks]

    def _adapt_block(self, block: dict) -> dict:
        btype = block.get("type", "")
        ctx = block.get("CONTEXT", {})

        if btype == "FUNCTION":
            corpo_raw = block.get("corpo", [])
            corpo = [self._adapt_block(c) for c in corpo_raw]
            return _make_function(
                nome=block.get("nome", "anonymous"),
                parametros=block.get("parametros", []),
                corpo=corpo,
                context=ctx,
            )

        if btype == "DISPATCH_ON_HERMENEUTICS":
            casos_raw = block.get("casos", {})
            casos = {k: v for k, v in casos_raw.items()}
            return _make_dispatch(
                recurso=block.get("recurso", ""),
                casos=casos,
                default=block.get("default"),
                context=ctx,
            )

        # Plain instruction block
        instructions = block.get("instructions", [])
        return _make_instruction_block(instructions=instructions, context=ctx)

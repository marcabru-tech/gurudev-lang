"""
tests/test_turing_completeness.py — Controle de fluxo hermenêutico (PR 1).

Verifica:
  - Turing-completude prática: if/else, while, for + variáveis
  - fatorial(5) em nível 1 = 120
  - nível 7 retorna DecisionTrace com graph não vazio e kind coerente
  - loops aninhados
  - contrato único DecisionTrace (chaves obrigatórias)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from compiler.bytecode_gen import BytecodeGenerator
from compiler.context_analyzer import ContextAnalyzer
from compiler.lexer import Lexer
from compiler.parser import Parser
from gurumatrix.core import GuruMatrix
from runtime.gurudvm import GuruDVM


# ── Helpers ───────────────────────────────────────────────────────────────────

def _compilar(codigo: str) -> dict:
    tokens = Lexer(codigo).tokenizar()
    ast = Parser(tokens).parse()
    ContextAnalyzer().analisar(ast)
    return BytecodeGenerator().gerar(ast)


def _executar(codigo: str, hermeneutica: int = 1) -> tuple[list, dict]:
    """Retorna (saidas, env) após execução no nível hermenêutico dado."""
    gurubyte = _compilar(codigo)
    gurubyte["CONTEXT_DEFAULT"]["hermeneutics"] = hermeneutica
    # Override top-level block contexts for hermeneutics level
    for bloco in gurubyte.get("CODEBLOCKS", []):
        bloco.setdefault("CONTEXT", {})["hermeneutics"] = hermeneutica
    matrix = GuruMatrix()
    matrix.popular_minimo()
    dvm = GuruDVM(matrix)
    saidas = dvm.executar(gurubyte)
    return saidas, dvm.env


def _display_outputs(saidas: list) -> list[Any]:
    return [s["dados"].get("output") for s in saidas if s["opcode"] == "DISPLAY"]


def _decision_traces(saidas: list) -> list[dict]:
    return [s["dados"] for s in saidas if s["opcode"] == "DECISION_TRACE"]


# ── Fatorial (nível 1) ────────────────────────────────────────────────────────

FATORIAL_WHILE = """
x = 5
acc = 1
while x > 1 {
  acc = acc * x
  x = x - 1
}
display acc
"""

FATORIAL_FOR = """
acc = 1
for i in range(1, 6) {
  acc = acc * i
}
display acc
"""


class TestFatorialNivel1:
    def test_fatorial_while_retorna_120(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=1)
        outputs = _display_outputs(saidas)
        assert len(outputs) >= 1
        assert outputs[0] == "120"

    def test_fatorial_for_retorna_120(self):
        saidas, _ = _executar(FATORIAL_FOR, hermeneutica=1)
        outputs = _display_outputs(saidas)
        assert len(outputs) >= 1
        assert outputs[0] == "120"

    def test_fatorial_env_acc_igual_120_while(self):
        _, env = _executar(FATORIAL_WHILE, hermeneutica=1)
        assert env.get("acc") == 120

    def test_fatorial_env_acc_igual_120_for(self):
        _, env = _executar(FATORIAL_FOR, hermeneutica=1)
        assert env.get("acc") == 120

    def test_fatorial_arquivo_guru(self):
        """examples/fatorial.guru deve executar sem erros e retornar 120."""
        caminho = Path(__file__).parent.parent / "examples" / "fatorial.guru"
        if not caminho.exists():
            pytest.skip("examples/fatorial.guru não encontrado")
        saidas, env = _executar(caminho.read_text(), hermeneutica=1)
        outputs = _display_outputs(saidas)
        assert "120" in outputs


# ── DecisionTrace (níveis 4–7) ────────────────────────────────────────────────

DECISION_TRACE_KEYS = {"kind", "level", "condition", "condition_value",
                        "taken_branch", "iterations", "events", "graph"}


class TestDecisionTrace:
    def test_nivel_4_while_emite_trace(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=4)
        traces = _decision_traces(saidas)
        assert len(traces) >= 1

    def test_nivel_4_trace_tem_chaves_obrigatorias(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=4)
        trace = _decision_traces(saidas)[0]
        assert DECISION_TRACE_KEYS <= trace.keys(), f"Faltam chaves: {DECISION_TRACE_KEYS - trace.keys()}"

    def test_nivel_4_trace_kind_while(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=4)
        trace = _decision_traces(saidas)[0]
        assert trace["kind"] == "while"

    def test_nivel_4_trace_iterations_igual_4(self):
        # while x > 1 com x=5 → 4 iterações
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=4)
        trace = _decision_traces(saidas)[0]
        assert trace["iterations"] == 4

    def test_nivel_4_graph_nulo(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=4)
        trace = _decision_traces(saidas)[0]
        assert trace["graph"] is None

    def test_nivel_5_events_historico(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=5)
        trace = _decision_traces(saidas)[0]
        assert len(trace["events"]) == 4

    def test_nivel_6_graph_existe(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=6)
        trace = _decision_traces(saidas)[0]
        assert trace["graph"] is not None
        assert "nodes" in trace["graph"]
        assert "edges" in trace["graph"]

    def test_nivel_7_graph_nao_vazio(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=7)
        trace = _decision_traces(saidas)[0]
        assert trace["graph"] is not None
        assert len(trace["graph"]["nodes"]) > 0
        assert len(trace["graph"]["edges"]) > 0

    def test_nivel_7_kind_coerente_while(self):
        saidas, _ = _executar(FATORIAL_WHILE, hermeneutica=7)
        trace = _decision_traces(saidas)[0]
        assert trace["kind"] == "while"
        assert trace["level"] == 7

    def test_nivel_7_kind_coerente_for(self):
        saidas, _ = _executar(FATORIAL_FOR, hermeneutica=7)
        trace = _decision_traces(saidas)[0]
        assert trace["kind"] == "for"
        assert trace["level"] == 7

    def test_arquivo_guru_nivel_7_retorna_trace(self):
        """examples/fatorial.guru nível 7 deve ter traces com graph."""
        caminho = Path(__file__).parent.parent / "examples" / "fatorial.guru"
        if not caminho.exists():
            pytest.skip("examples/fatorial.guru não encontrado")
        saidas, _ = _executar(caminho.read_text(), hermeneutica=7)
        traces = _decision_traces(saidas)
        assert len(traces) > 0
        # Pelo menos um trace deve ter graph não vazio
        graphs_nao_vazios = [t for t in traces if t.get("graph") and t["graph"]["nodes"]]
        assert len(graphs_nao_vazios) > 0


# ── If/else ────────────────────────────────────────────────────────────────────

IF_CODE = """
x = 10
if x > 5 {
  resultado = 1
} else {
  resultado = 0
}
display resultado
"""

IF_FALSE_CODE = """
x = 3
if x > 5 {
  resultado = 1
} else {
  resultado = 0
}
display resultado
"""


class TestIfElse:
    def test_if_true_branch(self):
        _, env = _executar(IF_CODE, hermeneutica=1)
        assert env.get("resultado") == 1

    def test_if_false_branch(self):
        _, env = _executar(IF_FALSE_CODE, hermeneutica=1)
        assert env.get("resultado") == 0

    def test_if_display_output(self):
        saidas, _ = _executar(IF_CODE, hermeneutica=1)
        outputs = _display_outputs(saidas)
        assert outputs[0] == "1"

    def test_if_trace_taken_branch_then(self):
        saidas, _ = _executar(IF_CODE, hermeneutica=4)
        traces = [t for t in _decision_traces(saidas) if t["kind"] == "if"]
        assert len(traces) >= 1
        assert traces[0]["taken_branch"] == "then"

    def test_if_trace_taken_branch_else(self):
        saidas, _ = _executar(IF_FALSE_CODE, hermeneutica=4)
        traces = [t for t in _decision_traces(saidas) if t["kind"] == "if"]
        assert traces[0]["taken_branch"] == "else"

    def test_if_trace_condition_value(self):
        saidas, _ = _executar(IF_CODE, hermeneutica=4)
        traces = [t for t in _decision_traces(saidas) if t["kind"] == "if"]
        assert traces[0]["condition_value"] is True

    def test_if_level_7_graph_com_nos_then_else(self):
        saidas, _ = _executar(IF_CODE, hermeneutica=7)
        traces = [t for t in _decision_traces(saidas) if t["kind"] == "if"]
        assert len(traces) >= 1
        graph = traces[0]["graph"]
        assert graph is not None
        node_ids = [n["id"] for n in graph["nodes"]]
        assert "then" in node_ids
        assert "else" in node_ids


# ── Loop aninhado ─────────────────────────────────────────────────────────────

NESTED_LOOP = """
n = 0
for i in range(1, 4) {
  for j in range(1, 4) {
    n = n + 1
  }
}
display n
"""


class TestNestedLoop:
    def test_nested_loop_resultado(self):
        _, env = _executar(NESTED_LOOP, hermeneutica=1)
        assert env.get("n") == 9

    def test_nested_loop_display(self):
        saidas, _ = _executar(NESTED_LOOP, hermeneutica=1)
        outputs = _display_outputs(saidas)
        assert outputs[0] == "9"

    def test_nested_loop_nivel_7_emite_multiplos_traces(self):
        saidas, _ = _executar(NESTED_LOOP, hermeneutica=7)
        traces = _decision_traces(saidas)
        # Dois loops aninhados → pelo menos 2 traces
        assert len(traces) >= 2

    def test_nested_loop_traces_kind_for(self):
        saidas, _ = _executar(NESTED_LOOP, hermeneutica=5)
        traces = _decision_traces(saidas)
        kinds = {t["kind"] for t in traces}
        assert "for" in kinds

    def test_nested_loop_outer_iterations(self):
        saidas, _ = _executar(NESTED_LOOP, hermeneutica=5)
        traces = _decision_traces(saidas)
        # Esperamos pelo menos um trace com 3 iterações (outer loop range(1,4))
        iterations_values = [t["iterations"] for t in traces if t["iterations"] is not None]
        assert 3 in iterations_values


# ── Aritmética e operadores ───────────────────────────────────────────────────

class TestArithmeticOps:
    def test_addition(self):
        _, env = _executar("a = 3\nb = 4\nc = a + b", hermeneutica=1)
        assert env.get("c") == 7

    def test_subtraction(self):
        _, env = _executar("a = 10\nb = 3\nc = a - b", hermeneutica=1)
        assert env.get("c") == 7

    def test_multiplication(self):
        _, env = _executar("a = 6\nb = 7\nc = a * b", hermeneutica=1)
        assert env.get("c") == 42

    def test_comparison_gt(self):
        _, env = _executar(
            "x = 0\nif 5 > 3 {\n  x = 1\n}", hermeneutica=1
        )
        assert env.get("x") == 1

    def test_comparison_lte(self):
        _, env = _executar(
            "x = 0\nif 3 <= 3 {\n  x = 1\n}", hermeneutica=1
        )
        assert env.get("x") == 1

    def test_range_builtin(self):
        _, env = _executar(
            "s = 0\nfor k in range(1, 5) {\n  s = s + k\n}", hermeneutica=1
        )
        assert env.get("s") == 10  # 1+2+3+4

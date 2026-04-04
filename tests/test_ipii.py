"""
Tests for GuruDev IPII pipeline:
  - BytecodeAdapterReal: FUNCTION and DISPATCH_ON_HERMENEUTICS blocks
  - IntentAnalyzer: at least one intent case
  - IPIIEngine: fatorial -> math.factorial
"""
import pytest

from gurudev.ipii import BytecodeAdapterReal, IntentAnalyzer, IPIIEngine, MAPEAMENTOS_BETA
from gurudev.ipii.intent_analyzer import Intent


# ── Fixtures ──────────────────────────────────────────────────────────────────

GURUBYTE_FUNCTION = {
    "HEADER": {"signature": "GURU", "version": "0.1.0"},
    "CONTEXT_DEFAULT": {"hermeneutics": 4},
    "CODEBLOCKS": [
        {
            "id": "BLOCK_0001",
            "CONTEXT": {"hermeneutics": 4, "clave": "ciencia"},
            "type": "FUNCTION",
            "nome": "fatorial",
            "parametros": ["n"],
            "corpo": [
                {
                    "id": "BLOCK_0002",
                    "CONTEXT": {"hermeneutics": 4},
                    "instructions": [
                        {"opcode": "LOAD", "operandos": ["n"], "modificadores": [], "contexto_hermeneutica": 4, "contexto_clave": "ciencia"}
                    ],
                }
            ],
        }
    ],
    "FOOTER": {"checksum": "SHA256-abc123"},
}

GURUBYTE_DISPATCH = {
    "HEADER": {"signature": "GURU", "version": "0.1.0"},
    "CONTEXT_DEFAULT": {"hermeneutics": 1},
    "CODEBLOCKS": [
        {
            "id": "BLOCK_0001",
            "CONTEXT": {"hermeneutics": 1},
            "type": "DISPATCH_ON_HERMENEUTICS",
            "recurso": "formula_energia",
            "casos": {
                "1": [{"opcode": "DISPLAY", "operandos": [], "modificadores": [], "contexto_hermeneutica": 1, "contexto_clave": "ciencia"}],
                "4": [{"opcode": "DISPLAY", "operandos": [], "modificadores": [], "contexto_hermeneutica": 4, "contexto_clave": "ciencia"}],
            },
            "default": [{"opcode": "DISPLAY", "operandos": [], "modificadores": [], "contexto_hermeneutica": 1, "contexto_clave": "geral"}],
        }
    ],
    "FOOTER": {},
}


# ── BytecodeAdapterReal ───────────────────────────────────────────────────────

class TestBytecodeAdapterReal:

    def test_adapt_function_block(self):
        adapter = BytecodeAdapterReal()
        result = adapter.adapt(GURUBYTE_FUNCTION)
        assert len(result) == 1
        block = result[0]
        assert block["kind"] == "function"
        assert block["nome"] == "fatorial"
        assert block["parametros"] == ["n"]
        assert isinstance(block["corpo"], list)

    def test_adapt_function_corpo_contains_instruction_block(self):
        adapter = BytecodeAdapterReal()
        result = adapter.adapt(GURUBYTE_FUNCTION)
        corpo = result[0]["corpo"]
        assert len(corpo) == 1
        assert corpo[0]["kind"] == "instructions"

    def test_adapt_dispatch_block(self):
        adapter = BytecodeAdapterReal()
        result = adapter.adapt(GURUBYTE_DISPATCH)
        assert len(result) == 1
        block = result[0]
        assert block["kind"] == "dispatch"
        assert block["recurso"] == "formula_energia"
        assert "1" in block["casos"]
        assert "4" in block["casos"]
        assert block["default"] is not None

    def test_adapt_plain_instruction_block(self):
        gurubyte = {
            "CODEBLOCKS": [
                {
                    "id": "BLOCK_0001",
                    "CONTEXT": {"hermeneutics": 1},
                    "instructions": [
                        {"opcode": "LOAD", "operandos": ["x"], "modificadores": []}
                    ],
                }
            ]
        }
        adapter = BytecodeAdapterReal()
        result = adapter.adapt(gurubyte)
        assert result[0]["kind"] == "instructions"
        assert len(result[0]["instructions"]) == 1

    def test_adapt_empty_codeblocks(self):
        adapter = BytecodeAdapterReal()
        result = adapter.adapt({"CODEBLOCKS": []})
        assert result == []

    def test_adapt_preserves_context(self):
        adapter = BytecodeAdapterReal()
        result = adapter.adapt(GURUBYTE_FUNCTION)
        assert result[0]["context"]["hermeneutics"] == 4
        assert result[0]["context"]["clave"] == "ciencia"


# ── IntentAnalyzer ────────────────────────────────────────────────────────────

class TestIntentAnalyzer:

    def test_function_fatorial_is_calculo_numerico(self):
        adapter = BytecodeAdapterReal()
        adapted = adapter.adapt(GURUBYTE_FUNCTION)
        analyzer = IntentAnalyzer()
        intent = analyzer.analyze(adapted)
        assert intent.name == "calculo_numerico"

    def test_dispatch_block_is_despacho_multiplo(self):
        adapter = BytecodeAdapterReal()
        adapted = adapter.adapt(GURUBYTE_DISPATCH)
        analyzer = IntentAnalyzer()
        intent = analyzer.analyze(adapted)
        assert intent.name == "despacho_multiplo"

    def test_formula_cientifica_intent(self):
        gurubyte = {
            "CODEBLOCKS": [
                {
                    "id": "BLOCK_0001",
                    "CONTEXT": {"hermeneutics": 4},
                    "type": "FUNCTION",
                    "nome": "formula_energia",
                    "parametros": ["massa", "velocidade"],
                    "corpo": [],
                }
            ]
        }
        adapted = BytecodeAdapterReal().adapt(gurubyte)
        intent = IntentAnalyzer().analyze(adapted)
        assert intent.name == "formula_cientifica"

    def test_intent_has_required_fields(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_FUNCTION)
        intent = IntentAnalyzer().analyze(adapted)
        assert isinstance(intent.name, str)
        assert isinstance(intent.tags, str)
        assert isinstance(intent.hermeneutics, int)

    def test_hermeneutics_from_context(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_FUNCTION)
        intent = IntentAnalyzer().analyze(adapted)
        assert intent.hermeneutics == 4

    def test_default_hermeneutics_is_4(self):
        adapted = [{"kind": "instructions", "instructions": [], "context": {}}]
        intent = IntentAnalyzer().analyze(adapted)
        assert intent.hermeneutics == 4

    def test_calculo_numerico_tags(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_FUNCTION)
        intent = IntentAnalyzer().analyze(adapted)
        assert "[ACAO]" in intent.tags
        assert "[CIENCIA]" in intent.tags


# ── IPIIEngine ────────────────────────────────────────────────────────────────

class TestIPIIEngine:

    def test_fatorial_generates_math_factorial(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_FUNCTION)
        intent = IntentAnalyzer().analyze(adapted)
        engine = IPIIEngine()
        code = engine.generate(adapted, intent)
        assert "math.factorial" in code
        assert "import math" in code

    def test_output_has_header_comment(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_FUNCTION)
        intent = IntentAnalyzer().analyze(adapted)
        code = IPIIEngine().generate(adapted, intent)
        assert "# Generated by GuruDev IPII v0.1-beta" in code

    def test_output_has_intent_comment(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_FUNCTION)
        intent = IntentAnalyzer().analyze(adapted)
        code = IPIIEngine().generate(adapted, intent)
        assert "# Intent:" in code
        assert "calculo_numerico" in code
        assert "[ACAO][CIENCIA]" in code
        assert "herm=4" in code

    def test_output_is_valid_python(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_FUNCTION)
        intent = IntentAnalyzer().analyze(adapted)
        code = IPIIEngine().generate(adapted, intent)
        # Should not raise SyntaxError
        compile(code, "<test>", "exec")

    def test_dispatch_generates_function_with_dict(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_DISPATCH)
        intent = IntentAnalyzer().analyze(adapted)
        code = IPIIEngine().generate(adapted, intent)
        assert "def despachar_formula_energia" in code
        assert "dispatch" in code

    def test_dispatch_output_is_valid_python(self):
        adapted = BytecodeAdapterReal().adapt(GURUBYTE_DISPATCH)
        intent = IntentAnalyzer().analyze(adapted)
        code = IPIIEngine().generate(adapted, intent)
        compile(code, "<test>", "exec")

    def test_mapeamentos_beta_has_at_least_15_entries(self):
        assert len(MAPEAMENTOS_BETA) >= 15

    def test_mapeamentos_beta_contains_fatorial(self):
        assert "fatorial" in MAPEAMENTOS_BETA
        assert "math.factorial" in MAPEAMENTOS_BETA["fatorial"]["call"]

    def test_generic_fallback_for_empty_blocks(self):
        intent = Intent(name="calculo_numerico", tags="[ACAO][CIENCIA]", hermeneutics=4)
        code = IPIIEngine().generate([], intent)
        assert "# Generated by GuruDev IPII v0.1-beta" in code
        compile(code, "<test>", "exec")


# ── IPIITranspiler tests ───────────────────────────────────────────────────────

import subprocess
import sys
import tempfile
from pathlib import Path

from gurudev.ipii.transpiler import IPIITranspiler


FATORIAL_CODE = """
x = 5
acc = 1
while x > 1 {
  acc = acc * x
  x = x - 1
}
display acc
"""

FOR_CODE = """
acc = 1
for i in range(1, 6) {
  acc = acc * i
}
display acc
"""


def _run_python(code: str) -> tuple[str, str, int]:
    """Runs Python code string in a subprocess. Returns (stdout, stderr, returncode)."""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        fname = f.name
    result = subprocess.run([sys.executable, fname], capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


class TestIPIITranspiler:
    def test_transpile_while_nivel_1_gera_python_valido(self):
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(FATORIAL_CODE, nivel=1)
        compile(py, "<test>", "exec")

    def test_transpile_while_nivel_1_executavel_retorna_120(self):
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(FATORIAL_CODE, nivel=1)
        stdout, stderr, rc = _run_python(py)
        assert rc == 0, f"Erro na execução: {stderr}"
        assert "120" in stdout

    def test_transpile_for_nivel_4_gera_python_valido(self):
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(FOR_CODE, nivel=4)
        compile(py, "<test>", "exec")

    def test_transpile_for_nivel_4_executavel_retorna_120(self):
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(FOR_CODE, nivel=4)
        stdout, stderr, rc = _run_python(py)
        assert rc == 0, f"Erro na execução: {stderr}"
        assert "120" in stdout

    def test_transpile_nivel_4_tem_decision_trace_helper(self):
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(FATORIAL_CODE, nivel=4)
        assert "_make_decision_trace" in py
        assert "_decision_traces" in py

    def test_transpile_nivel_1_sem_decision_trace(self):
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(FATORIAL_CODE, nivel=1)
        assert "_make_decision_trace" not in py

    def test_transpile_header_presente(self):
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(FATORIAL_CODE, nivel=4)
        assert "# Generated by GuruDev IPII v0.1-beta" in py
        assert "# Hermeneutics level: 4" in py

    def test_transpile_arquivo_fatorial_guru(self):
        """examples/fatorial.guru --nivel 4 gera Python válido e executável."""
        caminho = Path(__file__).parent.parent / "examples" / "fatorial.guru"
        if not caminho.exists():
            pytest.skip("examples/fatorial.guru não encontrado")
        transpiler = IPIITranspiler()
        py = transpiler.transpile_source(caminho.read_text(), nivel=4)
        # Valida sintaxe Python
        compile(py, str(caminho), "exec")
        # Executa e verifica saída
        stdout, stderr, rc = _run_python(py)
        assert rc == 0, f"Erro na execução: {stderr}"
        assert "120" in stdout

    def test_transpile_if_nivel_4_trace_estruturado(self):
        """Código com if deve emitir DecisionTrace estruturado no nível 4."""
        transpiler = IPIITranspiler()
        code = "x = 10\nif x > 5 {\n  y = 1\n} else {\n  y = 0\n}\ndisplay y"
        py = transpiler.transpile_source(code, nivel=4)
        stdout, stderr, rc = _run_python(py + "\nprint(_decision_traces)")
        assert rc == 0, f"Erro: {stderr}"
        assert "if" in stdout

    def test_transpile_bytecode_delega_a_engine_classico(self):
        """Bytecode sem blocos imperativos deve usar o engine IPII clássico."""
        transpiler = IPIITranspiler()
        gurubyte = {
            "HEADER": {"signature": "GURU", "version": "0.1.0"},
            "CONTEXT_DEFAULT": {"hermeneutics": 4},
            "CODEBLOCKS": [
                {
                    "id": "BLOCK_0001",
                    "CONTEXT": {"hermeneutics": 4, "clave": "ciencia"},
                    "type": "FUNCTION",
                    "nome": "fatorial",
                    "parametros": ["n"],
                    "corpo": [],
                }
            ],
            "FOOTER": {},
        }
        py = transpiler.transpile_bytecode(gurubyte, nivel=4)
        assert "# Generated by GuruDev IPII v0.1-beta" in py
        compile(py, "<test>", "exec")


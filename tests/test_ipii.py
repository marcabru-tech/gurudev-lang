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

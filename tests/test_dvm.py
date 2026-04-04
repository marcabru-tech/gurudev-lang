"""
test_dvm.py — Testes focados no runtime GuruDVM e dispatch hermenêutico.
"""
import pytest
from gurumatrix.core import GuruMatrix
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.context_analyzer import ContextAnalyzer
from compiler.bytecode_gen import BytecodeGenerator
from runtime.gurudvm import GuruDVM


# ── Helpers ──────────────────────────────────────────────────────────────────

def compilar(codigo: str) -> dict:
    tokens = Lexer(codigo).tokenizar()
    ast = Parser(tokens).parse()
    ContextAnalyzer().analisar(ast)
    return BytecodeGenerator().gerar(ast)


def executar_com_nivel(codigo: str, hermeneutica: int, recursos: dict = None) -> list:
    gurubyte = compilar(codigo)
    gurubyte["CONTEXT_DEFAULT"]["hermeneutics"] = hermeneutica
    for bloco in gurubyte.get("CODEBLOCKS", []):
        bloco.setdefault("CONTEXT", {})["hermeneutics"] = hermeneutica
    matrix = GuruMatrix()
    dvm = GuruDVM(matrix)
    if recursos:
        for k, v in recursos.items():
            dvm.carregar_recurso(k, v)
    return dvm.executar(gurubyte)


def saida_display(saidas: list) -> dict:
    for s in saidas:
        if s["opcode"] == "DISPLAY":
            return s["dados"]
    return {}


CODIGO_DISPATCH = """
bind clave = ciencia
load formula_energia
dispatch hermeneutica formula_energia {
    case 1:
        display in context
    case 4:
        display in context
    case 7:
        display in context
    default:
        display in context
}
"""

RECURSOS = {"formula_energia": "E = mc^2"}


# ── Instanciação da DVM ───────────────────────────────────────────────────────

class TestGuruDVMInstancia:
    def test_cria_dvm(self):
        matrix = GuruMatrix()
        dvm = GuruDVM(matrix)
        assert dvm is not None

    def test_contexto_inicial(self):
        matrix = GuruMatrix()
        dvm = GuruDVM(matrix)
        assert dvm.contexto["hermeneutics"] == 1
        assert dvm.contexto["clave"] == "geral"

    def test_carregar_recurso(self):
        matrix = GuruMatrix()
        dvm = GuruDVM(matrix)
        dvm.carregar_recurso("teste", "valor")
        assert dvm.recursos["teste"] == "valor"


# ── Dispatch hermenêutico — outputs distintos ────────────────────────────────

class TestDispatchHermeneutico:
    def test_nivel_1_modo_literal(self):
        saidas = executar_com_nivel(CODIGO_DISPATCH, 1, RECURSOS)
        dados = saida_display(saidas)
        assert dados.get("modo") == "LITERAL"

    def test_nivel_1_output_string(self):
        saidas = executar_com_nivel(CODIGO_DISPATCH, 1, RECURSOS)
        dados = saida_display(saidas)
        assert dados["output"] == "E = mc^2"

    def test_nivel_4_modo_contextual(self):
        saidas = executar_com_nivel(CODIGO_DISPATCH, 4, RECURSOS)
        dados = saida_display(saidas)
        assert dados.get("modo") == "CONTEXTUAL"

    def test_nivel_4_output_e_dict(self):
        saidas = executar_com_nivel(CODIGO_DISPATCH, 4, RECURSOS)
        dados = saida_display(saidas)
        assert isinstance(dados["output"], dict)
        assert "coordenada_gurumatrix" in dados["output"]

    def test_nivel_7_modo_ontologico(self):
        saidas = executar_com_nivel(CODIGO_DISPATCH, 7, RECURSOS)
        dados = saida_display(saidas)
        assert dados.get("modo") == "ONTOLÓGICO"

    def test_nivel_7_output_e_dict(self):
        saidas = executar_com_nivel(CODIGO_DISPATCH, 7, RECURSOS)
        dados = saida_display(saidas)
        assert isinstance(dados["output"], dict)
        assert "celula_origem" in dados["output"]

    def test_outputs_distintos_1_4_7(self):
        """Prova central do MVP: 3 níveis → 3 outputs computacionalmente distintos."""
        saidas_1 = executar_com_nivel(CODIGO_DISPATCH, 1, RECURSOS)
        saidas_4 = executar_com_nivel(CODIGO_DISPATCH, 4, RECURSOS)
        saidas_7 = executar_com_nivel(CODIGO_DISPATCH, 7, RECURSOS)

        modo_1 = saida_display(saidas_1).get("modo")
        modo_4 = saida_display(saidas_4).get("modo")
        modo_7 = saida_display(saidas_7).get("modo")

        assert modo_1 != modo_4
        assert modo_4 != modo_7
        assert modo_1 != modo_7

    def test_todos_niveis_produzem_output(self):
        for nivel in [1, 2, 3, 4, 5, 6, 7]:
            saidas = executar_com_nivel(CODIGO_DISPATCH, nivel, RECURSOS)
            dados = saida_display(saidas)
            assert dados.get("modo") is not None, f"Nenhum modo para nível {nivel}"

    def test_mvp_provado(self):
        """Fluxo mvp_demo.guru deve provar o MVP."""
        codigo = """
bind clave = ciencia
load formula_energia
dispatch hermeneutica formula_energia {
    case 1: display in context
    case 4: display in context
    case 7: display in context
    default: display in context
}
"""
        saidas_1 = executar_com_nivel(codigo, 1, RECURSOS)
        saidas_4 = executar_com_nivel(codigo, 4, RECURSOS)
        saidas_7 = executar_com_nivel(codigo, 7, RECURSOS)

        modos = {
            saida_display(saidas_1).get("modo"),
            saida_display(saidas_4).get("modo"),
            saida_display(saidas_7).get("modo"),
        }
        assert len(modos) == 3, "MVP PROVADO: True — 3 modos distintos"


# ── Instrução LOAD ────────────────────────────────────────────────────────────

class TestLoad:
    def test_load_registra_recurso(self):
        codigo = "load formula_energia"
        saidas = executar_com_nivel(codigo, 1, RECURSOS)
        load_saidas = [s for s in saidas if s["opcode"] == "LOAD"]
        assert len(load_saidas) == 1
        assert load_saidas[0]["alvo"] == "formula_energia"

    def test_load_recurso_ausente(self):
        codigo = "load recurso_inexistente"
        saidas = executar_com_nivel(codigo, 1, {})
        load_saidas = [s for s in saidas if s["opcode"] == "LOAD"]
        assert len(load_saidas) == 1
        assert "recurso_inexistente" in load_saidas[0]["dados"]["valor_preview"]


# ── Case sem correspondência → default ───────────────────────────────────────

class TestDefault:
    def test_case_ausente_usa_default(self):
        codigo = """
load formula_energia
dispatch hermeneutica formula_energia {
    case 1:
        display in context
    default:
        display in context
}
"""
        saidas = executar_com_nivel(codigo, 6, RECURSOS)
        dados = saida_display(saidas)
        assert dados is not None and dados.get("modo") is not None


# ── Bytecode generation ───────────────────────────────────────────────────────

class TestBytecodeGen:
    def test_header_presente(self):
        gurubyte = compilar("bind clave = ciencia")
        assert "HEADER" in gurubyte

    def test_codeblocks_presente(self):
        gurubyte = compilar("bind clave = ciencia")
        assert "CODEBLOCKS" in gurubyte

    def test_context_default_presente(self):
        gurubyte = compilar("bind clave = ciencia")
        assert "CONTEXT_DEFAULT" in gurubyte

    def test_dispatch_gera_bloco_dispatch(self):
        codigo = """
dispatch hermeneutica x {
    case 1: display in context
}
"""
        gurubyte = compilar(codigo)
        tipos = [b.get("type") for b in gurubyte["CODEBLOCKS"]]
        assert "DISPATCH_ON_HERMENEUTICS" in tipos

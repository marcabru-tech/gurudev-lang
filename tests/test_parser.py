"""
test_parser.py — Testes focados no analisador sintático GuruDev.
"""
import pytest
from compiler.lexer import Lexer, TokenType
from compiler.parser import (
    Parser,
    Programa,
    BindClave,
    TagHermeneutica,
    Instrucao,
    DispatchHermeneutica,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def parse(codigo: str) -> Programa:
    tokens = Lexer(codigo).tokenizar()
    return Parser(tokens).parse()


def find_nodes(programa: Programa, tipo: str):
    """Busca todos os nós de um tipo específico na AST."""
    result = []
    def _walk(nodes):
        for node in nodes:
            if hasattr(node, "tipo") and node.tipo == tipo:
                result.append(node)
            if hasattr(node, "declaracoes"):
                _walk(node.declaracoes)
            if hasattr(node, "filhos"):
                _walk(node.filhos)
    _walk(programa.declaracoes)
    return result


# ── Programa raiz ─────────────────────────────────────────────────────────────

class TestProgramaRaiz:
    def test_programa_vazio(self):
        prog = parse("")
        assert isinstance(prog, Programa)

    def test_programa_retorna_programa(self):
        prog = parse("bind clave = ciencia")
        assert isinstance(prog, Programa)

    def test_programa_tem_declaracoes(self):
        prog = parse("bind clave = ciencia")
        assert len(prog.declaracoes) > 0


# ── BindClave ─────────────────────────────────────────────────────────────────

class TestBindClave:
    def test_bind_clave_simples(self):
        prog = parse("bind clave = ciencia")
        nodes = find_nodes(prog, "BIND_CLAVE")
        assert len(nodes) >= 1
        assert nodes[0].campo == "ciencia"

    def test_bind_clave_campo(self):
        prog = parse("bind clave = arte")
        nodes = find_nodes(prog, "BIND_CLAVE")
        assert nodes[0].campo == "arte"


# ── TagHermeneutica ───────────────────────────────────────────────────────────

class TestTagHermeneutica:
    def test_tag_hermeneutica_nivel(self):
        prog = parse("tag hermeneutica = 4")
        nodes = find_nodes(prog, "TAG_HERMENEUTICA")
        assert len(nodes) >= 1
        assert nodes[0].nivel == 4

    def test_tag_hermeneutica_nivel_7(self):
        prog = parse("tag hermeneutica = 7")
        nodes = find_nodes(prog, "TAG_HERMENEUTICA")
        assert nodes[0].nivel == 7


# ── LOAD ──────────────────────────────────────────────────────────────────────

class TestLoad:
    def test_load_simples(self):
        prog = parse("load formula_energia")
        nodes = find_nodes(prog, "INSTRUCAO")
        load_nodes = [n for n in nodes if n.opcode == "LOAD"]
        assert len(load_nodes) >= 1
        assert "formula_energia" in load_nodes[0].operandos

    def test_load_identifier(self):
        prog = parse("load nota_musical")
        nodes = find_nodes(prog, "INSTRUCAO")
        load_nodes = [n for n in nodes if n.opcode == "LOAD"]
        assert "nota_musical" in load_nodes[0].operandos


# ── DISPLAY ───────────────────────────────────────────────────────────────────

class TestDisplay:
    def test_display_in_context(self):
        prog = parse("display in context")
        nodes = find_nodes(prog, "INSTRUCAO")
        display_nodes = [n for n in nodes if n.opcode == "DISPLAY"]
        assert len(display_nodes) >= 1
        assert display_nodes[0].modificadores.get("in_context") is True


# ── DispatchHermeneutica ──────────────────────────────────────────────────────

class TestDispatchHermeneutica:
    def test_dispatch_simples(self):
        codigo = """
dispatch hermeneutica formula_energia {
    case 1:
        display in context
    case 4:
        display in context
}
"""
        prog = parse(codigo)
        nodes = find_nodes(prog, "DISPATCH_HERMENEUTICA")
        assert len(nodes) >= 1

    def test_dispatch_recurso(self):
        codigo = """
dispatch hermeneutica formula_energia {
    case 1:
        display in context
}
"""
        prog = parse(codigo)
        nodes = find_nodes(prog, "DISPATCH_HERMENEUTICA")
        assert nodes[0].recurso == "formula_energia"

    def test_dispatch_casos(self):
        codigo = """
dispatch hermeneutica x {
    case 1:
        display in context
    case 4:
        display in context
    case 7:
        display in context
}
"""
        prog = parse(codigo)
        nodes = find_nodes(prog, "DISPATCH_HERMENEUTICA")
        assert 1 in nodes[0].casos
        assert 4 in nodes[0].casos
        assert 7 in nodes[0].casos

    def test_dispatch_default(self):
        codigo = """
dispatch hermeneutica x {
    default:
        display in context
}
"""
        prog = parse(codigo)
        nodes = find_nodes(prog, "DISPATCH_HERMENEUTICA")
        assert nodes[0].padrao is not None


# ── Pipeline completo ────────────────────────────────────────────────────────

class TestPipelineParser:
    def test_mvp_demo_parse(self):
        """O arquivo mvp_demo.guru deve ser parseado sem exceções."""
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
        prog = parse(codigo)
        assert isinstance(prog, Programa)
        assert len(prog.declaracoes) > 0

    def test_multiplos_binds(self):
        codigo = "bind clave = ciencia\nbind clave = arte"
        prog = parse(codigo)
        nodes = find_nodes(prog, "BIND_CLAVE")
        assert len(nodes) == 2

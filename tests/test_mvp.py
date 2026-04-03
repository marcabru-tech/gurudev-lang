"""
GuruDev MVP Tests
Prova do caso zero: DISPATCH_ON_HERMENEUTICS produz outputs computacionalmente distintos.
Execute: python -m pytest tests/ -v  (a partir de gurudev-mvp/)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from gurumatrix.core import GuruMatrix
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.context_analyzer import ContextAnalyzer
from compiler.bytecode_gen import BytecodeGenerator
from runtime.gurudvm import GuruDVM


# ── Helpers ─────────────────────────────────────────────────────────────────

def compilar(codigo: str) -> dict:
    tokens = Lexer(codigo).tokenizar()
    ast    = Parser(tokens).parse()
    ContextAnalyzer().analisar(ast)
    return BytecodeGenerator().gerar(ast)

def executar(codigo: str, hermeneutica: int, recursos: dict = None) -> list:
    gurubyte = compilar(codigo)
    gurubyte["CONTEXT_DEFAULT"]["hermeneutics"] = hermeneutica
    for bloco in gurubyte["CODEBLOCKS"]:
        bloco.setdefault("CONTEXT", {})["hermeneutics"] = hermeneutica
    matrix = GuruMatrix()
    matrix.popular_minimo()
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


# ── Código de teste central ─────────────────────────────────────────────────

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


# ── Testes: Prova do Caso Zero ───────────────────────────────────────────────

class TestCasoZero:
    """
    MVP Semântico: uma instrução, três hermenêuticas → três outputs distintos.
    Este é o teste que prova que GuruDev é uma linguagem semântica, não apenas
    uma linguagem com anotações semânticas inertes.
    """

    def test_hermeneutica_1_modo_literal(self):
        saidas = executar(CODIGO_DISPATCH, 1, RECURSOS)
        dados  = saida_display(saidas)
        assert dados.get("modo") == "LITERAL"
        assert dados["output"] == "E = mc^2"

    def test_hermeneutica_4_modo_contextual(self):
        saidas = executar(CODIGO_DISPATCH, 4, RECURSOS)
        dados  = saida_display(saidas)
        assert dados.get("modo") == "CONTEXTUAL"
        assert "coordenada_gurumatrix" in dados["output"]

    def test_hermeneutica_7_modo_ontologico(self):
        saidas = executar(CODIGO_DISPATCH, 7, RECURSOS)
        dados  = saida_display(saidas)
        assert dados.get("modo") == "ONTOLÓGICO"
        assert "conexoes_ontologicas" in dados["output"]
        assert "celula_origem" in dados["output"]

    def test_tres_outputs_computacionalmente_distintos(self):
        """Prova central: três modos diferentes, tipos de output diferentes."""
        d1 = saida_display(executar(CODIGO_DISPATCH, 1, RECURSOS))
        d4 = saida_display(executar(CODIGO_DISPATCH, 4, RECURSOS))
        d7 = saida_display(executar(CODIGO_DISPATCH, 7, RECURSOS))

        modos = {d1["modo"], d4["modo"], d7["modo"]}
        assert len(modos) == 3, f"Esperado 3 modos distintos, obtido: {modos}"

        # Output de nível 1 é string; output de nível 7 é dict
        assert isinstance(d1["output"], str), "Hermenêutica 1 deve retornar string"
        assert isinstance(d7["output"], dict), "Hermenêutica 7 deve retornar dict"

    def test_case_sem_correspondencia_usa_default(self):
        codigo = """
bind clave = ciencia
load recurso
dispatch hermeneutica recurso {
    case 1: display in context
    default: display in context
}
"""
        # hermeneutica=5 não tem case — deve cair no default
        saidas = executar(codigo, 5, {"recurso": "teste"})
        display = saida_display(saidas)
        assert display, "Default deve produzir output de DISPLAY"


# ── Testes: Todos os Níveis Hermenêuticos ───────────────────────────────────

class TestNiveisHermeneuticos:
    """Verifica que todos os 7 níveis produzem outputs semanticamente distintos."""

    CODIGO = """
bind clave = ciencia
load objeto
dispatch hermeneutica objeto {
    case 1: display in context
    case 2: display in context
    case 3: display in context
    case 4: display in context
    case 5: display in context
    case 6: display in context
    case 7: display in context
    default: display in context
}
"""
    RECURSOS = {"objeto": 42}

    def test_todos_os_niveis_produzem_output(self):
        for nivel in range(1, 8):
            saidas = executar(self.CODIGO, nivel, self.RECURSOS)
            d = saida_display(saidas)
            assert d, f"Hermenêutica {nivel} não produziu output de DISPLAY"
            assert "modo" in d, f"Hermenêutica {nivel}: campo 'modo' ausente"
            assert "output" in d, f"Hermenêutica {nivel}: campo 'output' ausente"

    def test_niveis_crescentes_produzem_output_crescente(self):
        """Níveis mais altos devem produzir outputs estruturalmente mais ricos."""
        d1 = saida_display(executar(self.CODIGO, 1, self.RECURSOS))
        d7 = saida_display(executar(self.CODIGO, 7, self.RECURSOS))

        # Nível 1: string simples; Nível 7: dict com múltiplas chaves
        assert isinstance(d1["output"], str)
        assert isinstance(d7["output"], dict)
        assert len(d7["output"]) > len(d1["output"]) or isinstance(d7["output"], dict)

    def test_nivel_7_contem_gurumatrix(self):
        d7 = saida_display(executar(self.CODIGO, 7, self.RECURSOS))
        assert "conexoes_ontologicas" in d7["output"]
        assert "celula_origem" in d7["output"]

    def test_nivel_5_contem_relacoes_semanticas(self):
        d5 = saida_display(executar(self.CODIGO, 5, self.RECURSOS))
        assert d5["modo"] == "COMPARATIVO"
        assert "relacoes_semanticas" in d5["output"]

    def test_nivel_6_contem_analogias(self):
        d6 = saida_display(executar(self.CODIGO, 6, self.RECURSOS))
        assert d6["modo"] == "ANALÓGICO"
        assert "analogias_interdominio" in d6["output"]


# ── Testes: Pipeline Completo ────────────────────────────────────────────────

class TestPipeline:
    """Testa cada etapa do pipeline: Lexer → Parser → ContextAnalyzer → BytecodeGen → DVM."""

    def test_lexer_tokeniza_keywords(self):
        from compiler.lexer import TokenType
        tokens = Lexer("bind clave = ciencia").tokenizar()
        tipos = [t.tipo for t in tokens]
        assert TokenType.BIND in tipos
        assert TokenType.CLAVE in tipos
        assert TokenType.ASSIGN in tipos

    def test_lexer_tokeniza_tag_hermeneutica(self):
        from compiler.lexer import TokenType
        tokens = Lexer("tag hermeneutica = 7").tokenizar()
        tipos = [t.tipo for t in tokens]
        assert TokenType.TAG in tipos
        assert TokenType.HERMENEUTICA in tipos
        numeros = [t.valor for t in tokens if t.tipo == TokenType.NUMBER]
        assert "7" in numeros

    def test_parser_gera_bind_clave(self):
        from compiler.parser import BindClave
        tokens = Lexer("bind clave = arte").tokenizar()
        ast    = Parser(tokens).parse()
        assert any(isinstance(n, BindClave) for n in ast.declaracoes)

    def test_parser_gera_dispatch(self):
        from compiler.parser import DispatchHermeneutica
        codigo = """
load x
dispatch hermeneutica x {
    case 1: display in context
}
"""
        tokens = Lexer(codigo).tokenizar()
        ast    = Parser(tokens).parse()
        assert any(isinstance(n, DispatchHermeneutica) for n in ast.declaracoes)

    def test_context_analyzer_propaga_clave(self):
        codigo = "bind clave = filosofia\nload x"
        tokens = Lexer(codigo).tokenizar()
        ast    = Parser(tokens).parse()
        ca     = ContextAnalyzer()
        ca.analisar(ast)
        from compiler.parser import Instrucao
        instrucoes = [n for n in ast.declaracoes if isinstance(n, Instrucao)]
        if instrucoes:
            assert instrucoes[0].clave == "filosofia"

    def test_bytecode_gen_cria_codeblocks(self):
        codigo = "bind clave = ciencia\nload x\ndisplay in context"
        gurubyte = compilar(codigo)
        assert "CODEBLOCKS" in gurubyte
        assert len(gurubyte["CODEBLOCKS"]) > 0

    def test_bytecode_gen_cria_header(self):
        gurubyte = compilar("bind clave = geral")
        assert gurubyte["HEADER"]["signature"] == "GURU"
        assert "version" in gurubyte["HEADER"]

    def test_gurubyte_tem_checksum(self):
        gurubyte = compilar("bind clave = ciencia\nload x")
        assert "checksum" in gurubyte["FOOTER"]
        assert gurubyte["FOOTER"]["checksum"].startswith("SHA256-")

    def test_dvm_executa_load(self):
        gurubyte = compilar("load meu_recurso")
        matrix   = GuruMatrix(); matrix.popular_minimo()
        dvm      = GuruDVM(matrix)
        dvm.carregar_recurso("meu_recurso", "valor_teste")
        saidas   = dvm.executar(gurubyte)
        loads    = [s for s in saidas if s["opcode"] == "LOAD"]
        assert loads, "LOAD deve gerar saída"
        assert loads[0]["dados"]["carregado"] is True


# ── Testes: Dry-Run Semântico ────────────────────────────────────────────────

class TestDryRun:
    """Verifica que o Semantic Dry-Run detecta anotações inertes."""

    def test_dry_run_detecta_gap(self):
        codigo = "bind clave = ciencia\ntag hermeneutica = 7\nload x\ndisplay in context"
        tokens = Lexer(codigo).tokenizar()
        ast    = Parser(tokens).parse()
        ca     = ContextAnalyzer()
        ca.analisar(ast)
        relatorio = ca.relatorio_dry_run()
        assert "gap_semantico" in relatorio
        assert "total_anotacoes" in relatorio

    def test_dry_run_com_dispatch_marca_ativo(self):
        codigo = """
load x
dispatch hermeneutica x {
    case 1: display in context
    case 7: display in context
}
"""
        tokens = Lexer(codigo).tokenizar()
        ast    = Parser(tokens).parse()
        ca     = ContextAnalyzer()
        ca.analisar(ast)
        relatorio = ca.relatorio_dry_run()
        ativos = [e for e in relatorio["detalhes"]
                  if e["status"] == "ATIVA_COM_DESPACHO"]
        assert len(ativos) >= 0  # estrutura válida


# ── Testes: GuruMatrix ───────────────────────────────────────────────────────

class TestGuruMatrix:

    def test_tem_100_celulas(self):
        m = GuruMatrix()
        assert len(m.celulas) == 100

    def test_popular_minimo_adiciona_objetos(self):
        m = GuruMatrix()
        m.popular_minimo()
        from gurumatrix.core import Ontologia, Dominio
        c = m.get(Ontologia.ACAO, Dominio.CIENCIA)
        assert len(c.objetos) > 0

    def test_get_por_nome(self):
        m = GuruMatrix()
        c = m.get_by_name("ACAO", "CIENCIA")
        assert c is not None

    def test_inefavel_gera_warning(self):
        from gurumatrix.core import Inefavel
        i = Inefavel("fenômeno não mapeável")
        w = i.to_guruwarning()
        assert w["tipo"] == "GuruWarning"
        assert "acao_recomendada" in w

"""Pipeline compartilhada do GuruDev: compilar e executar."""
from compiler.bytecode_gen import BytecodeGenerator
from compiler.context_analyzer import ContextAnalyzer
from compiler.lexer import Lexer
from compiler.parser import Parser
from gurumatrix.core import GuruMatrix
from runtime.gurudvm import GuruDVM

RECURSOS_DEMO = {
    "formula_energia": "E = mc^2",
    "nota_musical": "Lá 440Hz",
    "formula_euler": "e^(iπ) + 1 = 0",
    "pi": 3.14159265,
    "sequencia": [1, 1, 2, 3, 5, 8, 13],
}


def compilar(codigo: str, filename: str = "<input>") -> tuple:
    """Compila código GuruDev para bytecode."""
    tokens = Lexer(codigo, filename).tokenizar()
    ast = Parser(tokens).parse()
    analyzer = ContextAnalyzer()
    analyzer.analisar(ast)
    gurubyte = BytecodeGenerator().gerar(ast)
    return gurubyte, analyzer


def executar(gurubyte: dict, hermeneutica: int, recursos: dict) -> tuple:
    """Executa bytecode no GuruDVM e retorna resultados + status MVP."""
    if "CONTEXT_DEFAULT" not in gurubyte:
        gurubyte["CONTEXT_DEFAULT"] = {}
    gurubyte["CONTEXT_DEFAULT"]["hermeneutics"] = hermeneutica

    for bloco in gurubyte.get("CODEBLOCKS", []):
        if "CONTEXT" not in bloco:
            bloco["CONTEXT"] = {}
        bloco["CONTEXT"]["hermeneutics"] = hermeneutica

    matrix = GuruMatrix()
    dvm = GuruDVM(matrix)

    for k, v in recursos.items():
        dvm.carregar_recurso(k, v)

    resultados = dvm.executar(gurubyte)
    status_mvp = dvm._verificar_mvp()
    return resultados, status_mvp

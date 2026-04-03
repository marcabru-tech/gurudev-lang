#!/usr/bin/env python3
"""
gurudev-cli.py — Interface de linha de comando GuruDev v0.1-MVP
Uso:
  python gurudev-cli.py <arquivo.guru> [--hermeneutica N] [--dry-run] [--json]
"""
import sys, os, json, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gurumatrix.core import GuruMatrix
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.context_analyzer import ContextAnalyzer
from compiler.bytecode_gen import BytecodeGenerator
from runtime.gurudvm import GuruDVM

BANNER = """
╔══════════════════════════════════════════╗
║   GuruDev® v0.1-MVP  ·  Semantic Runtime ║
╚══════════════════════════════════════════╝"""

RECURSOS_DEMO = {
    "formula_energia": "E = mc^2",
    "nota_musical":    "Lá 440Hz",
    "formula_euler":   "e^(iπ) + 1 = 0",
    "pi":              3.14159265,
    "sequencia":       [1, 1, 2, 3, 5, 8, 13],
}

def compilar(codigo: str) -> tuple:
    tokens   = Lexer(codigo).tokenizar()
    ast      = Parser(tokens).parse()
    analyzer = ContextAnalyzer()
    analyzer.analisar(ast)
    gurubyte = BytecodeGenerator().gerar(ast)
    return gurubyte, analyzer

def executar(gurubyte: dict, hermeneutica: int, recursos: dict) -> list:
    gurubyte["CONTEXT_DEFAULT"]["hermeneutics"] = hermeneutica
    for bloco in gurubyte["CODEBLOCKS"]:
        bloco.setdefault("CONTEXT", {})["hermeneutics"] = hermeneutica
    matrix = GuruMatrix()
    matrix.popular_minimo()
    dvm = GuruDVM(matrix)
    for k, v in recursos.items():
        dvm.carregar_recurso(k, v)
    return dvm.executar(gurubyte)

def formatar_saida(saidas: list, nivel: int, json_mode: bool) -> str:
    if json_mode:
        return json.dumps(saidas, ensure_ascii=False, indent=2)

    linhas = [f"\n── Execução com hermenêutica={nivel} " + "─" * 30]
    for s in saidas:
        opcode = s["opcode"]
        dados  = s["dados"]
        if opcode == "DISPLAY":
            modo   = dados.get("modo", "?")
            output = dados.get("output", "")
            desc   = dados.get("descricao", "")
            linhas.append(f"\n[DISPLAY] modo={modo}")
            linhas.append(f"  descricao: {desc}")
            if isinstance(output, dict):
                linhas.append(f"  output:")
                for k, v in output.items():
                    v_str = str(v)[:120] + ("…" if len(str(v)) > 120 else "")
                    linhas.append(f"    {k}: {v_str}")
            else:
                linhas.append(f"  output: {output}")
        elif opcode == "LOAD":
            linhas.append(f"[LOAD] {s['alvo']} — carregado")
        elif opcode == "EVALUATE":
            modo = dados.get("modo", "?")
            linhas.append(f"[EVALUATE] modo={modo}")
        elif opcode in ("BIND", "MAP_TO", "TAG"):
            linhas.append(f"[{opcode}] {s['alvo']}")
    return "\n".join(linhas)

def main():
    parser = argparse.ArgumentParser(
        description="GuruDev CLI v0.1-MVP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python gurudev-cli.py examples/mvp_demo.guru --hermeneutica 1
  python gurudev-cli.py examples/mvp_demo.guru --hermeneutica 7
  python gurudev-cli.py examples/mvp_demo.guru --demo
  python gurudev-cli.py examples/mvp_demo.guru --dry-run
""")
    parser.add_argument("arquivo", nargs="?", help="Arquivo .guru para executar")
    parser.add_argument("--hermeneutica", type=int, default=1, choices=range(1, 8),
                        metavar="N", help="Nível hermenêutico 1-7 (default: 1)")
    parser.add_argument("--dry-run",  action="store_true", help="Mostra relatório semântico")
    parser.add_argument("--json",     action="store_true", help="Output em JSON")
    parser.add_argument("--demo",     action="store_true", help="Executa todos os 7 níveis")
    parser.add_argument("--gurubyte", action="store_true", help="Mostra bytecode gerado")
    args = parser.parse_args()

    print(BANNER)

    if not args.arquivo:
        parser.print_help()
        sys.exit(0)

    if not os.path.exists(args.arquivo):
        print(f"\n✗ Arquivo não encontrado: {args.arquivo}")
        sys.exit(1)

    with open(args.arquivo, encoding="utf-8") as f:
        codigo = f.read()

    print(f"\n▶ Compilando {args.arquivo}…")
    try:
        gurubyte, analyzer = compilar(codigo)
    except (SyntaxError, ValueError) as e:
        print(f"✗ Erro de compilação: {e}")
        sys.exit(1)

    print(f"  ✓ {len(gurubyte['CODEBLOCKS'])} bloco(s) gerado(s)")

    if args.dry_run:
        relatorio = analyzer.relatorio_dry_run()
        print("\n── Semantic Dry-Run Report " + "─" * 30)
        print(f"  Total de anotações : {relatorio['total_anotacoes']}")
        print(f"  Com despacho ativo : {relatorio['ativas_com_despacho']}")
        print(f"  Inertes            : {relatorio['inertes']}")
        print(f"  Gap semântico      : {relatorio['gap_semantico']}")
        return

    if args.gurubyte:
        print("\n── GuruByte (.gurub) " + "─" * 30)
        print(json.dumps(gurubyte, ensure_ascii=False, indent=2))
        return

    niveis = list(range(1, 8)) if args.demo else [args.hermeneutica]

    for nivel in niveis:
        import copy
        gb = copy.deepcopy(gurubyte)
        saidas = executar(gb, nivel, RECURSOS_DEMO)
        print(formatar_saida(saidas, nivel, args.json and not args.demo))

    if args.demo:
        print("\n" + "─" * 60)
        print("✓ MVP Semântico demonstrado: 7 níveis hermenêuticos,")
        print("  outputs computacionalmente distintos por nível.")

if __name__ == "__main__":
    main()

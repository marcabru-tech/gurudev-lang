#!/usr/bin/env python3
"""
gurudev_cli.py — Interface de linha de comando GuruDev v0.1-MVP

Uso:
  gurudev build <arquivo.guru>       Compila para .gurub
  gurudev run <arquivo.guru>         Compila + executa
  gurudev <arquivo.guru> [opções]    Interface legada
"""
import argparse
import copy
import json
import os
import sys
from pathlib import Path

from compiler.bytecode_gen import BytecodeGenerator
from compiler.context_analyzer import ContextAnalyzer
from compiler.lexer import Lexer
from compiler.parser import Parser
from gurumatrix.core import GuruMatrix
from runtime.gurudvm import GuruDVM

BANNER = """
╔══════════════════════════════════════════╗
║   GuruDev® v0.1-MVP  ·  Semantic Runtime ║
╚══════════════════════════════════════════╝"""

RECURSOS_DEMO = {
    "formula_energia": "E = mc^2",
    "nota_musical": "Lá 440Hz",
    "formula_euler": "e^(iπ) + 1 = 0",
    "pi": 3.14159265,
    "sequencia": [1, 1, 2, 3, 5, 8, 13],
}


def compilar(codigo: str, filename: str = "<input>") -> tuple:
    tokens = Lexer(codigo, filename).tokenizar()
    ast = Parser(tokens).parse()
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
        dados = s["dados"]
        if opcode == "DISPLAY":
            modo = dados.get("modo", "?")
            output = dados.get("output", "")
            desc = dados.get("descricao", "")
            linhas.append(f"\n[DISPLAY] modo={modo}")
            linhas.append(f"  descricao: {desc}")
            if isinstance(output, dict):
                linhas.append("  output:")
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


def cmd_build(args) -> int:
    """Subcomando build: compila .guru para .gurub."""
    src_path = Path(args.arquivo)
    if not src_path.exists():
        print(f"✗ Arquivo não encontrado: {args.arquivo}")
        return 1

    with open(src_path, encoding="utf-8") as f:
        codigo = f.read()

    print(f"▶ Compilando {src_path}…")
    try:
        gurubyte, _ = compilar(codigo, str(src_path))
    except (SyntaxError, ValueError) as e:
        print(f"✗ Erro de compilação: {e}")
        return 1

    out_dir = src_path.parent / ".gurudev"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / (src_path.stem + ".gurub")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(gurubyte, f, ensure_ascii=False, indent=2)

    print(f"  ✓ {len(gurubyte['CODEBLOCKS'])} bloco(s) → {out_path}")
    return 0


def cmd_run(args) -> int:
    """Subcomando run: compila + executa."""
    src_path = Path(args.arquivo)
    if not src_path.exists():
        print(f"✗ Arquivo não encontrado: {args.arquivo}")
        return 1

    with open(src_path, encoding="utf-8") as f:
        codigo = f.read()

    print(f"▶ Compilando {src_path}…")
    try:
        gurubyte, analyzer = compilar(codigo, str(src_path))
    except (SyntaxError, ValueError) as e:
        print(f"✗ Erro de compilação: {e}")
        return 1

    print(f"  ✓ {len(gurubyte['CODEBLOCKS'])} bloco(s) gerado(s)")

    nivel = getattr(args, "hermeneutica", 1)
    saidas = executar(copy.deepcopy(gurubyte), nivel, RECURSOS_DEMO)
    print(formatar_saida(saidas, nivel, False))
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="gurudev",
        description="GuruDev® CLI v0.1-MVP — Semantic Programming Language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  gurudev build examples/mvp_demo.guru
  gurudev run examples/mvp_demo.guru --hermeneutica 4
  gurudev examples/mvp_demo.guru --demo
""",
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    # Subcomando: build
    p_build = subparsers.add_parser("build", help="Compila .guru para .gurub")
    p_build.add_argument("arquivo", help="Arquivo .guru para compilar")

    # Subcomando: run
    p_run = subparsers.add_parser("run", help="Compila e executa um arquivo .guru")
    p_run.add_argument("arquivo", help="Arquivo .guru para executar")
    p_run.add_argument(
        "--hermeneutica",
        type=int,
        default=1,
        choices=range(1, 8),
        metavar="N",
        help="Nível hermenêutico 1-7 (default: 1)",
    )

    # Interface legada (sem subcomando)
    parser.add_argument("arquivo", nargs="?", help="Arquivo .guru para executar")
    parser.add_argument(
        "--hermeneutica",
        type=int,
        default=1,
        choices=range(1, 8),
        metavar="N",
        help="Nível hermenêutico 1-7 (default: 1)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Mostra relatório semântico")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    parser.add_argument("--demo", action="store_true", help="Executa todos os 7 níveis")
    parser.add_argument("--gurubyte", action="store_true", help="Mostra bytecode gerado")

    args = parser.parse_args()
    print(BANNER)

    # Roteamento de subcomandos
    if args.subcommand == "build":
        sys.exit(cmd_build(args))
    elif args.subcommand == "run":
        sys.exit(cmd_run(args))

    # Interface legada
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
        gb = copy.deepcopy(gurubyte)
        saidas = executar(gb, nivel, RECURSOS_DEMO)
        print(formatar_saida(saidas, nivel, args.json and not args.demo))

    if args.demo:
        print("\n" + "─" * 60)
        print("✓ MVP Semântico demonstrado: 7 níveis hermenêuticos,")
        print("  outputs computacionalmente distintos por nível.")


if __name__ == "__main__":
    main()

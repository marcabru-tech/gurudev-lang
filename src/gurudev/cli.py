"""GuruDev CLI v0.2 - Interface moderna com Click e Rich."""
import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from compiler.bytecode_gen import BytecodeGenerator
from compiler.context_analyzer import ContextAnalyzer
from compiler.lexer import Lexer
from compiler.parser import Parser
from gurudev.exceptions import GuruDevError
from gurumatrix.core import GuruMatrix
from runtime.gurudvm import GuruDVM

console = Console()

BANNER = """
[bold cyan]╔══════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan] [bold yellow]GuruDev®[/bold yellow] [dim]v0.2[/dim] · [italic]Semantic Programming Language[/italic] [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════╝[/bold cyan]
"""

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
    matrix.popular_minimo()
    dvm = GuruDVM(matrix)

    for k, v in recursos.items():
        dvm.carregar_recurso(k, v)

    resultados = dvm.executar(gurubyte)
    status_mvp = dvm._verificar_mvp()
    return resultados, status_mvp

@click.group()
def main():
    """GuruDev CLI - Ferramenta de linha de comando para a linguagem GuruDev."""
    pass

@main.command()
@click.argument('arquivo', type=click.Path(exists=True))
@click.option('--output', '-o', help='Arquivo de saída para o bytecode (.gurub)')
def compile(arquivo, output):
    """Compila um arquivo .guru para bytecode .gurub."""
    console.print(BANNER)
    try:
        codigo = Path(arquivo).read_text()
        gurubyte, _ = compilar(codigo, arquivo)

        if output:
            with open(output, 'w') as f:
                json.dump(gurubyte, f, indent=4)
            console.print(f"[bold green]Sucesso![/bold green] Bytecode salvo em: {output}")
        else:
            console.print(Panel("[bold blue]Bytecode Gerado[/bold blue]"))
            console.print_json(data=gurubyte)

    except GuruDevError as e:
        console.print(f"[bold red]Erro de Compilação:[/bold red] {e}")

@main.command()
@click.argument('arquivo', type=click.Path(exists=True))
@click.option('--hermeneutica', '-h', default=1, type=int, help='Nível hermenêutico (1-7)')
@click.option('--demo', is_flag=True, help='Executa em todos os 7 níveis')
def run(arquivo, hermeneutica, demo):
    """Executa um arquivo .guru diretamente."""
    console.print(BANNER)

    try:
        codigo = Path(arquivo).read_text()

        if demo:
            for h in range(1, 8):
                console.print(Panel(f"[bold green]Executando Nível {h}[/bold green]"))
                gurubyte, _ = compilar(codigo, arquivo)
                resultados, status_mvp = executar(gurubyte, h, RECURSOS_DEMO)
                for res in resultados:
                    console.print(res)
                if status_mvp:
                    console.print("[dim italic]✓ MVP Semântico Verificado: outputs distintos detectados.[/dim italic]")
        else:
            gurubyte, _ = compilar(codigo, arquivo)
            resultados, status_mvp = executar(gurubyte, hermeneutica, RECURSOS_DEMO)
            for res in resultados:
                console.print(res)
            if status_mvp:
                console.print("[dim italic]✓ MVP Semântico Verificado: outputs distintos detectados.[/dim italic]")

    except GuruDevError as e:
        console.print(f"[bold red]Erro:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Erro inesperado:[/bold red] {e}")

@main.command()
@click.argument('arquivo', type=click.Path(exists=True))
def build(arquivo):
    """Alias para compile --output <arquivo>.gurub."""
    output = str(Path(arquivo).with_suffix('.gurub'))
    ctx = click.get_current_context()
    ctx.invoke(compile, arquivo=arquivo, output=output)

@main.command()
@click.argument('arquivo', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, help='Arquivo de saída Python (.py); padrão: stdout')
def export(arquivo, output):
    """Transpila um arquivo .guru ou .gurub para Python via pipeline IPII."""
    from gurudev.ipii import BytecodeAdapterReal, IntentAnalyzer, IPIIEngine

    console.print(BANNER)
    try:
        caminho = Path(arquivo)
        sufixo = caminho.suffix.lower()

        if sufixo == '.guru':
            codigo = caminho.read_text()
            gurubyte, _ = compilar(codigo, arquivo)
        elif sufixo == '.gurub':
            with open(arquivo, 'r') as f:
                gurubyte = json.load(f)
        else:
            console.print(f"[bold red]Erro:[/bold red] Extensão não suportada '{sufixo}'. Use .guru ou .gurub.")
            raise SystemExit(1)

        adapted = BytecodeAdapterReal().adapt(gurubyte)
        intent = IntentAnalyzer().analyze(adapted)
        py_source = IPIIEngine().generate(adapted, intent)

        if output:
            Path(output).write_text(py_source)
            console.print(
                f"[bold green]Sucesso![/bold green] Python exportado para: {output}\n"
                f"[dim]Intent: {intent.name} {intent.tags} herm={intent.hermeneutics}[/dim]"
            )
        else:
            console.print(Panel("[bold blue]Python Gerado (IPII)[/bold blue]"))
            console.print(Syntax(py_source, "python", theme="monokai", line_numbers=True))

    except GuruDevError as e:
        console.print(f"[bold red]Erro de Compilação:[/bold red] {e}")
        raise SystemExit(1)
    except Exception as e:
        console.print(f"[bold red]Erro inesperado:[/bold red] {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

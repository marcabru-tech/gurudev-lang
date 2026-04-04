"""GuruDev CLI v0.2 - Interface moderna com Click e Rich."""
import json
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from gurudev.exceptions import GuruDevError
from gurudev.pipeline import RECURSOS_DEMO, compilar, executar

console = Console()

BANNER = """
[bold cyan]╔══════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan] [bold yellow]GuruDev®[/bold yellow] [dim]v0.2[/dim] · [italic]Semantic Programming Language[/italic] [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════╝[/bold cyan]
"""


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
@click.option('--nivel', '-n', default=4, type=click.IntRange(1, 7),
              help='Nível hermenêutico alvo (1–7; padrão: 4)')
def export(arquivo, output, nivel):
    """Transpila um arquivo .guru ou .gurub para Python via pipeline IPII.

    O nível hermenêutico (--nivel) controla o contrato DecisionTrace gerado:
      1–3 → Python imperativo puro
      4   → DecisionTrace com 1 evento por bloco de controle
      5   → DecisionTrace com histórico completo de eventos
      6   → DecisionTrace com grafo de fluxo
      7   → DecisionTrace com snapshots de estado nas arestas do grafo
    """
    from gurudev.ipii.transpiler import IPIITranspiler

    console.print(BANNER)
    try:
        caminho = Path(arquivo)
        sufixo = caminho.suffix.lower()

        transpiler = IPIITranspiler()

        if sufixo == '.guru':
            codigo = caminho.read_text()
            py_source = transpiler.transpile_source(codigo, nivel=nivel,
                                                     filename=str(caminho))
        elif sufixo == '.gurub':
            with open(arquivo, 'r') as f:
                gurubyte = json.load(f)
            py_source = transpiler.transpile_bytecode(gurubyte, nivel=nivel)
        else:
            console.print(f"[bold red]Erro:[/bold red] Extensão não suportada '{sufixo}'. Use .guru ou .gurub.")
            raise SystemExit(1)

        if output:
            Path(output).write_text(py_source)
            console.print(
                f"[bold green]Sucesso![/bold green] Python exportado para: {output}\n"
                f"[dim]Nível hermenêutico: {nivel}[/dim]"
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

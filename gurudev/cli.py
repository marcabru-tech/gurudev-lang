"""GuruDev CLI v0.2 - Interface moderna com Click e Rich."""
import json
import sys
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

# Ajuste de path para imports internos
sys.path.append(str(Path(__file__).parent.parent))

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.context_analyzer import ContextAnalyzer
from compiler.bytecode_gen import BytecodeGenerator
from runtime.gurudvm import GuruDVM
from gurumatrix.core import GuruMatrix
from gurudev.exceptions import GuruDevError

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

def executar(gurubyte: dict, hermeneutica: int, recursos: dict) -> list:
    """Executa bytecode no GuruDVM."""
    # Injetar hermenêutica no contexto global do bytecode
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
        
    return dvm.executar(gurubyte)

@click.group()
def main():
    """GuruDev CLI - Ferramenta de linha de comando para a linguagem GuruDev."""
    pass

@main.command()
@click.argument('arquivo', type=click.Path(exists=True))
@click.option('--hermeneutica', '-h', default=1, type=int, help='Nível hermenêutico (1-7)')
@click.option('--demo', is_flag=True, help='Executa em todos os 7 níveis')
def run(arquivo, hermeneutica, demo):
    """Executa um arquivo .guru."""
    console.print(BANNER)
    
    try:
        codigo = Path(arquivo).read_text()
        
        if demo:
            for h in range(1, 8):
                console.print(Panel(f"[bold green]Executando Nível {h}[/bold green]"))
                gurubyte, _ = compilar(codigo, arquivo)
                resultados = executar(gurubyte, h, RECURSOS_DEMO)
                for res in resultados:
                    console.print(res)
        else:
            gurubyte, _ = compilar(codigo, arquivo)
            resultados = executar(gurubyte, hermeneutica, RECURSOS_DEMO)
            for res in resultados:
                console.print(res)
                
    except GuruDevError as e:
        console.print(f"[bold red]Erro:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Erro inesperado:[/bold red] {e}")

@main.command()
@click.argument('arquivo', type=click.Path(exists=True))
def inspect(arquivo):
    """Inspeciona o bytecode e análise semântica de um arquivo."""
    console.print(BANNER)
    
    try:
        codigo = Path(arquivo).read_text()
        gurubyte, analyzer = compilar(codigo, arquivo)
        
        console.print(Panel("[bold blue]Bytecode Gerado[/bold blue]"))
        console.print_json(data=gurubyte)
        
    except GuruDevError as e:
        console.print(f"[bold red]Erro:[/bold red] {e}")

if __name__ == "__main__":
    main()

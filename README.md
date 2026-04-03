# GuruDev® v0.1-MVP

Implementação mínima funcional focada no **MVP Semântico**:
provar que `DISPATCH_ON_HERMENEUTICS` produz outputs computacionalmente distintos.

## Documentação

A especificação técnica fundacional da linguagem pode ser encontrada em:
- [Especificação Fundacional v0.2](docs/especificacao-fundacional-v0.2.md)

## Estado do Projeto

| Componente | Status |
|---|---|
| Lexer | ✅ |
| Parser | ✅ |
| GuruMatrix | ⚠️ 33% densidade |
| Runtime DVM | ✅ |
| CLI (argparse) | ✅ |
| CLI (click/rich) | ⚠️ requer `click` e `rich` instalados |
| IPII Transpiler | 🧪 experimental |
| CI/CD | ✅ (Python 3.9–3.12) |
| Turing-completude | ❌ planejado |

## Instalação

```bash
# Instalar em modo editável com dependências de desenvolvimento
pip install -e ".[dev]"
```

## Execução

### CLI legado (argparse — sem dependências extras)

```bash
# Executar com nível hermenêutico específico
PYTHONPATH=src python3 gurudev-cli.py examples/mvp_demo.guru --hermeneutica 1
PYTHONPATH=src python3 gurudev-cli.py examples/mvp_demo.guru --hermeneutica 7

# Modo demo — executa todos os 7 níveis hermenêuticos
PYTHONPATH=src python3 gurudev-cli.py examples/mvp_demo.guru --demo

# Inspecionar bytecode gerado
PYTHONPATH=src python3 gurudev-cli.py examples/mvp_demo.guru --gurubyte
```

### CLI moderna (click + rich — após `pip install -e .`)

```bash
# Executar com nível específico
gurudev run examples/mvp_demo.guru --hermeneutica 4

# Modo demo (7 níveis)
gurudev run examples/mvp_demo.guru --demo

# Compilar para bytecode (.gurub)
gurudev compile examples/mvp_demo.guru

# Transpilar para Python via IPII
gurudev export examples/mvp_demo.guru
```

## Testes

```bash
# Executar todos os testes (requer pip install -e ".[dev]")
PYTHONPATH=src python -m pytest tests/ -v

# Ou simplesmente (pythonpath configurado em pyproject.toml)
pytest
```

## Estrutura do Repositório

```
gurudev-lang/
├── docs/
│   └── especificacao-fundacional-v0.2.md  # Whitepaper v0.2
├── examples/
│   └── mvp_demo.guru                      # Programa de demonstração
├── src/
│   ├── compiler/
│   │   ├── lexer.py             # .guru → tokens
│   │   ├── parser.py            # tokens → GuruAST
│   │   ├── context_analyzer.py  # propagação de contexto semântico
│   │   └── bytecode_gen.py      # GuruAST → GuruByte (dict)
│   ├── gurumatrix/
│   │   ├── core.py              # Espaço semântico 10x10 (Aristóteles × Domínios)
│   │   └── cells.py             # Definição de células semânticas
│   ├── runtime/
│   │   └── gurudvm.py           # Execução bicameral + DISPATCH_ON_HERMENEUTICS
│   ├── gurudev/
│   │   ├── cli.py               # CLI v0.2 (Click + Rich)
│   │   ├── exceptions.py        # Sistema de exceções customizadas
│   │   ├── logger.py            # Sistema de logging estruturado
│   │   └── ipii/                # Transpilador IPII → Python
│   └── cli/
│       └── gurudev_cli.py       # CLI entry point (click)
├── tests/                       # Suíte completa de testes (119+ casos)
├── gurudev-cli.py               # CLI legado (argparse, sem deps extras)
├── pyproject.toml               # Configuração moderna de projeto
└── requirements.txt             # Dependências
```

## O MVP Semântico

O teste central (`TestCasoZero.test_tres_outputs_computacionalmente_distintos`)
prova que a mesma instrução `display in context` produz:

| Hermenêutica | Modo       | Output                              |
|-------------|------------|-------------------------------------|
| 1           | LITERAL    | `"E = mc^2"` (string)               |
| 4           | CONTEXTUAL | `{valor, coordenada_gurumatrix}`     |
| 7           | ONTOLÓGICO | `{celula_origem, conexoes, relacoes}`|

Isso demonstra que o sistema semântico é operacional — não decorativo.

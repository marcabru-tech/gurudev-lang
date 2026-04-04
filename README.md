# GuruDev® v0.2

Implementação funcional focada no **MVP Semântico**:
provar que `DISPATCH_ON_HERMENEUTICS` produz outputs computacionalmente distintos.

## Documentação

A especificação técnica fundacional da linguagem pode ser encontrada em:
- [Especificação Fundacional v0.2](docs/especificacao-fundacional-v0.2.md)

## Estado do Projeto

| Componente | Status |
|---|---|
| Lexer | ✅ |
| Parser | ✅ |
| GuruMatrix | ✅ 60+ células (ARTE, CIÊNCIA, FILOSOFIA, LINGUAGEM, MATEMÁTICA, TECNOLOGIA) |
| Runtime DVM | ✅ |
| CLI (click/rich) | ✅ |
| Pipeline compartilhada | ✅ `gurudev.pipeline` |
| IPII Transpiler | 🧪 experimental |
| CI/CD | ✅ (Python 3.9–3.12) |
| Turing-completude | ❌ planejado |

## Instalação

```bash
# Instalar em modo editável com dependências de desenvolvimento
pip install -e ".[dev]"
```

## Execução

### CLI (click + rich — após `pip install -e .`)

```bash
# Executar com nível específico
gurudev run examples/mvp_demo.guru --hermeneutica 4

# Modo demo (7 níveis)
gurudev run examples/mvp_demo.guru --demo

# Compilar para bytecode (.gurub)
gurudev compile examples/mvp_demo.guru

# Construir bytecode (alias para compile --output)
gurudev build examples/mvp_demo.guru

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
│   └── gurudev/
│       ├── cli.py               # CLI v0.2 (Click + Rich)
│       ├── pipeline.py          # Pipeline compartilhada: compilar() e executar()
│       ├── exceptions.py        # Sistema de exceções customizadas
│       └── ipii/                # Transpilador IPII → Python
├── tests/                       # Suíte completa de testes (191+ casos)
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

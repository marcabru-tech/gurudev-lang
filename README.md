# GuruDev® v0.1-MVP

Implementação mínima funcional focada no **MVP Semântico**:
provar que `DISPATCH_ON_HERMENEUTICS` produz outputs computacionalmente distintos.

## Documentação

A especificação técnica fundacional da linguagem pode ser encontrada em:
- [Especificação Fundacional v0.2](docs/especificacao-fundacional-v0.2.md)

## Instalação

```bash
pip install pytest
```

## Execução rápida (CLI v0.2)

A nova CLI utiliza `click` e `rich` para uma experiência visual e funcional superior.

```text
╔══════════════════════════════════════════════════════════╗
║ GuruDev® v0.2 · Semantic Programming Language ║
╚══════════════════════════════════════════════════════════╝
```

### Comandos Principais

```bash
# Instalar em modo editável
pip install -e .

# Executar código diretamente (Nível 4 - CONTEXTUAL)
python gurudev/cli.py run examples/mvp_demo.guru --hermeneutica 4

# Executar modo Demo (todos os 7 níveis hermenêuticos)
python gurudev/cli.py run examples/mvp_demo.guru --demo

# Compilar para bytecode (.gurub)
python gurudev/cli.py build examples/mvp_demo.guru

# Inspecionar o bytecode gerado
python gurudev/cli.py compile examples/mvp_demo.guru
```

## Testes

```bash
python -m pytest tests/ -v
```

## Estrutura do Repositório

```
gurudev-repo/
├── docs/
│   └── especificacao-fundacional-v0.2.md  # Whitepaper v0.2
├── gurumatrix/core.py       # Espaço semântico 10x10 (Aristóteles × Domínios)
├── compiler/
│   ├── lexer.py             # .guru → tokens
│   ├── parser.py            # tokens → GuruAST
│   ├── context_analyzer.py  # propagação de contexto semântico
│   └── bytecode_gen.py      # GuruAST → GuruByte (dict)
├── runtime/gurudvm.py       # Execução bicameral + DISPATCH_ON_HERMENEUTICS
├── tests/test_mvp.py        # Suite completa de testes
├── examples/mvp_demo.guru   # Programa de demonstração
├── gurudev/                 # Novo pacote de infraestrutura
│   ├── cli.py               # Nova CLI v0.2 (Click + Rich)
│   ├── exceptions.py        # Sistema de exceções customizadas
│   └── logger.py            # Sistema de logging estruturado
├── pyproject.toml           # Configuração moderna de projeto
└── requirements.txt         # Dependências (atualizado)
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

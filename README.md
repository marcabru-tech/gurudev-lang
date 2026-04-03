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

## Execução rápida

```bash
# Nível 1 — modo LITERAL
python gurudev-cli.py examples/mvp_demo.guru --hermeneutica 1

# Nível 4 — modo CONTEXTUAL (coordenadas GuruMatrix)
python gurudev-cli.py examples/mvp_demo.guru --hermeneutica 4

# Nível 7 — modo ONTOLÓGICO (expansão completa)
python gurudev-cli.py examples/mvp_demo.guru --hermeneutica 7

# Demo completo — todos os 7 níveis
python gurudev-cli.py examples/mvp_demo.guru --demo

# Dry-run semântico
python gurudev-cli.py examples/mvp_demo.guru --dry-run

# Ver GuruByte gerado
python gurudev-cli.py examples/mvp_demo.guru --gurubyte
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
├── gurudev-cli.py           # CLI
└── requirements.txt         # Dependências
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

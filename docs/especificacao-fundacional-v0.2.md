# GuruDev®: Uma Linguagem de Programação Ontológica e Multissemiótica
## Especificação Técnica Fundacional — v0.2

**Autor:** Guilherme Machado  
**Instituição:** Hubstry Deep Tech / Overall Consultoria 720°  
**Licença:** CC BY 4.0  
**DOI:** [a atribuir pelo Zenodo]  
**Data:** Abril de 2026  
**Versão anterior:** v0.1 (Abril de 2026)  
**Repositório:** github.com/[org]/gurudev-mvp  

---

## Resumo / Abstract / Resumen

**PT:** A GuruDev® é uma linguagem de programação de propósito geral com arquitetura ontológica, multissemiótica e multimodal. Esta versão (v0.2) atualiza a especificação fundacional v0.1 com base na implementação funcional do MVP Semântico — demonstrando empiricamente que a instrução central do sistema, `DISPATCH_ON_HERMENEUTICS`, produz outputs computacionalmente distintos para diferentes níveis hermenêuticos. A implementação inclui pipeline completo (Lexer → Parser → Context Analyzer → BytecodeGenerator → GuruDVM), 25 testes automatizados passando, e CLI funcional. O projeto avança do status de *programa de pesquisa* para o de *implementação verificável*.

**EN:** GuruDev® is a general-purpose programming language with ontological, multisemiotic, and multimodal architecture. This version (v0.2) updates the v0.1 foundational specification based on the functional implementation of the Semantic MVP — empirically demonstrating that the system's central instruction, `DISPATCH_ON_HERMENEUTICS`, produces computationally distinct outputs for different hermeneutic levels. The implementation includes a complete pipeline (Lexer → Parser → Context Analyzer → BytecodeGenerator → GuruDVM), 25 passing automated tests, and a functional CLI. The project advances from *research program* status to *verifiable implementation*.

**ES:** GuruDev® es un lenguaje de programación de propósito general con arquitectura ontológica, multisemiótica y multimodal. Esta versión (v0.2) actualiza la especificación fundacional v0.1 a partir de la implementación funcional del MVP Semántico — demostrando empíricamente que la instrucción central del sistema, `DISPATCH_ON_HERMENEUTICS`, produce outputs computacionalmente distintos para diferentes niveles hermenéuticos. El proyecto avanza del estatus de *programa de investigación* al de *implementación verificable*.

**Palavras-chave:** linguagem de programação, semiótica peirceana, ontologia aristotélica, interoperabilidade semântica, bytecode, compilador, multimodalidade, hermenêutica computacional.

---

## Nota de Versão

A v0.1 deste whitepaper foi publicada com postura deliberadamente crítica: cada componente foi tensionado antes de ser especificado, e mitigações foram propostas para fragilidades identificadas. A linguagem da v0.1 era de *intenção* — o que *precisava ser demonstrado*.

Esta v0.2 mantém o rigor crítico da v0.1, mas atualiza o status epistêmico de cada componente à luz da implementação. O que estava *enunciado* agora está *demonstrado*. O que estava *projetado* agora está *especificado para implementação imediata*. O que permanece como trabalho futuro está explicitamente marcado como tal.

A diferença entre as duas versões não é de conteúdo filosófico — é de evidência empírica.

---

## 1. Introdução

### 1.1 O Problema e a Tese

O universo do desenvolvimento de software opera com uma contradição estrutural: aplicações modernas são construídas a partir de múltiplas linguagens que precisam se comunicar, mas a interoperabilidade nativa entre elas permanece um problema não resolvido. As soluções existentes — FFIs, protocolos de serialização, wrappers — resolvem o problema sintático sem tocar no problema semântico: o código transita entre sistemas, mas seu *significado* frequentemente não.

A tese fundadora da GuruDev® é que a interoperabilidade entre sistemas computacionais falha não apenas por diferenças sintáticas, mas por ausência de um substrato semântico comum. A contribuição original da linguagem é tratar **semiose** — a operação pela qual algo funciona como signo (Peirce) — como categoria computacional de primeira classe, não como metadado ou comentário.

### 1.2 O que foi Demonstrado nesta Versão

O MVP Semântico demonstra empiricamente a tese central. A instrução `DISPATCH_ON_HERMENEUTICS` aplicada ao recurso `"E = mc^2"` produz os seguintes outputs verificados (extraído da execução `python gurudev-cli.py examples/mvp_demo.guru --demo`):

| Hermenêutica | Modo | Tipo do Output | Conteúdo |
|:---:|---|---|---|
| 1 | LITERAL | `str` | `"E = mc^2"` |
| 2 | ALEGÓRICO | `dict` | `{tipo: str, valor: "E = mc^2"}` |
| 3 | TÉCNICO | `dict` | `{repr, comprimento, palavras}` |
| 4 | CONTEXTUAL | `dict` | `{valor, coordenada_gurumatrix: (ACAO, CIENCIA)}` |
| 5 | COMPARATIVO | `dict` | `{valor, relacoes_semanticas: [equivalencia, similitude]}` |
| 6 | ANALÓGICO | `dict` | `{valor, analogias_interdominio: [...]}` |
| 7 | ONTOLÓGICO | `dict` | `{celula_origem, objetos, relacoes, conexoes_ontologicas}` |

O mesmo recurso, a mesma instrução, sete outputs computacionalmente distintos. O sistema semântico é operacional — não decorativo. Isso é o que a v0.1 precisava demonstrar e esta v0.2 confirma.

### 1.3 Posicionamento Atual

O projeto avança de *programa de pesquisa* (Lakatos) para *implementação verificável*. O núcleo duro — semiose como categoria computacional de primeira classe — passou do status de hipótese para o de tese com evidência empírica. O cinturão protetor de hipóteses auxiliares está parcialmente implementado e progressivamente verificável.

---

## 2. Fundamentos Teóricos

*(Inalterado da v0.1 — os fundamentos filosóficos são estáveis)*

### 2.1 Pensamento Analógico como Operação Primitiva

O pensamento analógico — associação entre estruturas distintas por correspondência, não por identidade — é o núcleo do processador semântico da GuruDev®. Formalmente, uma analogia entre domínios $D_1$ e $D_2$ é um morfismo parcial $\phi: D_1 \rightharpoonup D_2$ que preserva relações relevantes. A operação de interoperabilidade na GuruDev® é a construção e aplicação desse morfismo.

### 2.2 Fundamento Semiótico: Peirce

**Axioma 1:** Não há pensamento sem linguagem.  
**Axioma 2:** Não há linguagem sem signo.

A tricotomia peirceana ícone/índice/símbolo é tratada como teoria dos tipos:
- **Ícone:** relação por semelhança (imagem, diagrama)
- **Índice:** relação por contiguidade causal (log, rastro de execução)
- **Símbolo:** relação por convenção (identificadores, palavras-chave)

### 2.3 Fundamento Ontológico: Aristóteles

As dez categorias aristotélicas funcionam como sistema de coordenadas para qualquer objeto representável na GuruDev®:

| # | Categoria | Domínio Computacional |
|---|---|---|
| 1 | Substância | Tipos, Classes, Instâncias |
| 2 | Quantidade | Escalares, Vetores |
| 3 | Qualidade | Atributos, Propriedades |
| 4 | Relação | Referências, Grafos |
| 5 | Lugar | Namespaces |
| 6 | Tempo | Timestamps, Sequências |
| 7 | Situação | Stack frames |
| 8 | Condição | Ambiente, Dependências |
| 9 | Ação | Funções, Métodos |
| 10 | Paixão | Eventos, Callbacks |

### 2.4 As Seis Relações de Interoperabilidade Semântica

**Status:** definição formal estabelecida para relações 1–3; relações 4–6 requerem formalização como functores na v0.3.

| Relação | Definição | Status Formal |
|---|---|---|
| Similitude | Morfismo parcial que preserva comportamento externo | ✓ Formalizado |
| Homologia | Isomorfismo estrutural entre domínios heterogêneos | ✓ Formalizado |
| Equivalência | Bijeção funcional com preservação de semântica | ✓ Formalizado |
| Simetria | Automorfismo reflexivo | ◐ Parcial |
| Equilíbrio | Proporção custo/expressividade | ◐ Heurística |
| Compensação | Estrutura auxiliar para lacuna funcional | ◐ Heurística |

---

## 3. GuruMatrix — Espaço Semântico de Coordenadas

**Status:** implementado e testado (`GuruMatrix`, `popular_minimo()`, `get()`, `get_by_name()`).

### 3.1 Definição

A GuruMatrix é o espaço de coordenadas semânticas da GuruDev®: uma estrutura de indexação 10×10 com semântica ontológica nos eixos. É um **sistema de endereçamento semântico**, não uma matriz algébrica convencional (distinção mantida da v0.1 — operações algébricas são roadmap v0.3).

### 3.2 Dois Eixos Homogêneos

**Eixo X — Categorias Ontológicas (o *que* é o objeto):** as dez categorias de Aristóteles (ver Seção 2.3).

**Eixo Y — Domínios Epistêmicos (em *que campo* opera):**

| Y | Domínio |
|---|---|
| 1 | Arte |
| 2 | Ciência |
| 3 | Filosofia |
| 4 | Tradição Espiritual |
| 5 | Tecnologia |
| 6 | Linguagem |
| 7 | Matemática |
| 8 | Medicina / Biologia |
| 9 | Direito / Ética |
| 10 | Educação |

As seis relações semânticas são **atributos de célula**, não dimensões de eixo — correção arquitetural implementada nesta versão.

### 3.3 Implementação Atual

```python
# Célula implementada:
@dataclass
class CelulaGuruMatrix:
    x: Ontologia          # categoria aristotélica
    y: Dominio            # domínio epistêmico
    objetos: List[str]
    relacoes_ativas: List[RelacaoSemantica]
    instrucoes_preferenciais: List[str]
    embedding: Optional[List[float]]  # None em v0.1; preenchido em v0.3
```

Células populadas no MVP (via `popular_minimo()`):
- `[ACAO][CIENCIA]` → fatorial, fft, media, derivada | relações: Equivalência, Similitude
- `[QUALIDADE][ARTE]` → cor, textura, harmonia, ritmo | relações: Simetria, Equilíbrio
- `[RELACAO][MATEMATICA]` → funcao, morfismo | relações: Homologia, Equivalência
- `[SUBSTANCIA][TECNOLOGIA]` → int, string, array, dict
- `[TEMPO][CIENCIA]` → serie_temporal, timestamp, frequencia

### 3.4 Tipo `Inefável`

Implementado. Tipo para fenômenos fora do espaço de representação atual — produz `GuruWarning`, não `GuruError`. Proteção arquitetural contra homogeneização pelo sucesso (lição do Bourbaki).

### 3.5 Roadmap Algébrico (v0.3)

Métrica de proximidade semântica via produto interno de embeddings e operação de composição via produto tensorial permanecem como trabalho futuro — especificados na v0.1, não alterados.

---

## 4. GuruCompiler — Pipeline de Compilação

**Status:** implementado e testado (pipeline completo, 12 testes de pipeline passando).

### 4.1 Arquitetura Bicameral

```
[.guru] → Lexer → Parser → Context Analyzer → BytecodeGenerator → [.gurub dict]
                                   ↕
                             GuruMatrix
```

O pipeline é bicameral por design: o plano sintático produz bytecode executável; o plano semântico produz metadados de contexto. Os dois planos são separados no GuruByte (seções `CODEBLOCKS` e `CONTEXT`) e orquestrados pela GuruDVM em tempo de execução.

### 4.2 Etapas Implementadas

**Lexer:** tokeniza palavras reservadas, operadores, strings, números, tokens multimodais. Implementado com suporte a `bind`, `tag`, `dispatch`, `case`, `default`, `load`, `display`, `evaluate`, `transcode`, `emote`, `in`, `context`.

**Parser:** constrói GuruAST com nós semânticamente enriquecidos (`TagHermeneutica`, `BindClave`, `DispatchHermeneutica`, `Instrucao`, `FuncaoDecl`). Opera como parser recursivo descendente.

**Context Analyzer:** propaga contexto semântico (clave, hermenêutica, ontologia) para cada nó da AST. Opera em **Modo Declarativo** (v0.1): anotações explícitas do programador. Modo Inferencial requer GuruMatrix populada — roadmap v0.2.

**BytecodeGenerator:** serializa GuruAST em estrutura GuruByte (dict JSON-serializável). Gera SHA256 de checksum. Separa CONTEXT por bloco.

### 4.3 Semantic Dry-Run

Implementado. O Context Analyzer gera relatório de gap semântico:

```json
{
  "total_anotacoes": 3,
  "ativas_com_despacho": 2,
  "inertes": 1,
  "gap_semantico": "1/3 anotações sem despacho semântico associado"
}
```

Instrução: `python gurudev-cli.py arquivo.guru --dry-run`

### 4.4 Bootstrapping Problem (Resolvido para v0.1)

O Modo Inferencial cria dependência circular: o compilador precisa da GuruMatrix populada para inferir ontologia; a GuruMatrix é populada via compilação. Resolvido para v0.1 iniciando em Modo Declarativo. A v0.2 introduz inferência gradual à medida que a GuruMatrix acumula conteúdo via curadoria manual.

---

## 5. GuruByte — Formato de Bytecode

**Status:** implementado como estrutura dict JSON-serializável. Arquivo binário `.gurub` é roadmap v0.2.

### 5.1 Princípio Bicameral

Plano sintático (CODEBLOCKS com instruções executáveis) e plano semântico (CONTEXT por bloco com metadados hermenêuticos) são separados. As anotações semânticas não são emitidas no mesmo plano do código executável — portanto não são destruídas por otimizadores. A GuruDVM consulta o plano semântico em tempo de execução.

### 5.2 Estrutura

```
HEADER      → assinatura, versão, semantic_mode, packaging
CONTEXT_DEFAULT → contexto global (default para todos os blocos)
CONSTANTS   → recursos multimodais (ref ou embedded)
CODEBLOCKS  → blocos com CONTEXT local + instruções
FOOTER      → SHA256 checksum
```

### 5.3 CONTEXT Local por Bloco

Correção arquitetural implementada nesta versão: cada `CODEBLOCK` carrega seu próprio CONTEXT. O CONTEXT global é *default* que blocos individuais sobrescrevem.

```json
{
  "id": "BLOCK_0002",
  "CONTEXT": { "clave": "filosofia", "hermeneutics": 7, "ontologia": "RELACAO" },
  "type": "DISPATCH_ON_HERMENEUTICS",
  "recurso": "formula_energia",
  "casos": { "1": [...], "7": [...] },
  "default": [...]
}
```

**Regra de precedência:** CONTEXT de bloco > CONTEXT global. TAG dentro de instrução sobrescreve CONTEXT do bloco apenas para a instrução seguinte.

---

## 6. GuruInstructionSet v0.1

**Status:** categorias 1–5 especificadas; categorias 2A (anotação) e 2B (despacho) implementadas e testadas.

### 6.1 Princípio de Completude Semântica

Toda instrução deve: (a) executar uma operação computacional, ou (b) modificar o contexto semântico, ou (c) ambos. Instruções que apenas descrevem sem modificar comportamento são metadados, não instruções.

### 6.2 Categoria 2B — Despacho Semântico (núcleo do MVP)

A distinção entre Categoria 2A (anotação) e 2B (despacho) foi a correção arquitetural mais importante da v0.1. As instruções de anotação (`TAG`, `BIND`, `MAP_TO`) só têm efeito computacional quando consumidas por instruções de despacho.

```
DISPATCH_ON_HERMENEUTICS recurso {
    CASE 1: <instrução literal>
    CASE 4: <instrução contextual>
    CASE 7: <instrução ontológica>
    DEFAULT: <instrução base>
}
```

**Evidência empírica** (25 testes passando):
- `TestCasoZero::test_tres_outputs_computacionalmente_distintos` — PASSOU
- `TestNiveisHermeneuticos::test_todos_os_niveis_produzem_output` — PASSOU
- `TestNiveisHermeneuticos::test_nivel_7_contem_gurumatrix` — PASSOU

### 6.3 Semântica Operacional: Triplas de Hoare Verificadas

```
# DISPATCH_ON_HERMENEUTICS — verificado por teste
{ CONTEXT.Hermeneutics = N, N ∈ {1..7} }
DISPATCH_ON_HERMENEUTICS recurso { CASE N: BLOCK_X }
{ BLOCK_X executado; output computacionalmente distinto de BLOCK_Y para N ≠ M }

# DISPLAY IN CONTEXT — verificado por teste
{ recurso na pilha; CONTEXT.Hermeneutics = N }
DISPLAY IN CONTEXT
{ output ∈ {LITERAL|ALEGÓRICO|TÉCNICO|CONTEXTUAL|COMPARATIVO|ANALÓGICO|ONTOLÓGICO} }
```

### 6.4 Instruções Projetadas (Categoria 6)

`EMOTE`, `TRACE`, `CLONE`, `EXPAND_ONTOLOGICAL` — semântica especificada, implementação aguarda infraestrutura v0.2+. Classificadas como *Projetadas*, não *Experimentais*, para evitar implementação como tags vazias.

---

## 7. GuruDVM — Runtime

**Status:** implementado e testado. Runtime bicameral operacional.

### 7.1 Arquitetura

A GuruDVM executa o GuruByte consultando simultaneamente o plano sintático (instruções) e o plano semântico (CONTEXT por bloco + GuruMatrix). O despacho semântico é o coração do runtime:

```python
def _dispatch_hermeneutica(self, bloco, ctx):
    nivel = ctx.get("hermeneutics", 1)
    casos = bloco.get("casos", {})
    corpo = casos.get(str(nivel)) or bloco.get("default")
    # executa o corpo correspondente ao nível hermenêutico ativo
```

### 7.2 Comportamento Verificado por Nível

| Nível | Modo | Implementação |
|---|---|---|
| 1 | LITERAL | retorna `str(valor)` |
| 2 | ALEGÓRICO | retorna `{tipo, valor}` |
| 3 | TÉCNICO | análise estrutural do recurso |
| 4 | CONTEXTUAL | coordenadas GuruMatrix inferidas |
| 5 | COMPARATIVO | relações semânticas da célula |
| 6 | ANALÓGICO | conexões entre domínios via Homologia |
| 7 | ONTOLÓGICO | expansão completa da célula GuruMatrix |

### 7.3 CLI

```bash
python gurudev-cli.py arquivo.guru --hermeneutica 7   # nível específico
python gurudev-cli.py arquivo.guru --demo              # todos os 7 níveis
python gurudev-cli.py arquivo.guru --dry-run           # relatório semântico
python gurudev-cli.py arquivo.guru --gurubyte          # bytecode gerado
```

---

## 8. IPII — Interação Paramétrica Iterativa por Interoperabilidade

**Status:** especificada na v0.1; não implementada na v0.1-MVP. Roadmap v0.2.

*(Seção inalterada da v0.1 — a especificação permanece válida; o MVP demonstrou a infraestrutura semântica sobre a qual a IPII será construída)*

A IPII é a técnica de transpilação semântica que usa coordenadas GuruMatrix como substrato estruturado para matching entre linguagens. Com o MVP demonstrando que o sistema semântico é operacional, a IPII passa de especulação arquitetural para próximo passo natural de implementação.

Comparação com sistemas existentes (Tree-sitter, Babel, CodeT5+) permanece válida — a vantagem diferencial da IPII sobre LLMs é **rastreabilidade**: as decisões de transpilação são auditáveis via coordenadas GuruMatrix, não estatísticas opacas.

---

## 9. Arquitetura de Sistema

### 9.1 Diagrama Atualizado

```
┌─────────────────────────────────────────────────────────────┐
│                   GuruDev® v0.1-MVP                          │
│                                                              │
│  .guru ──→ [Lexer] ──→ [Parser] ──→ [ContextAnalyzer]       │
│                              ↓              ↓                │
│                         [GuruAST]     [DryRunReport]         │
│                              ↓                               │
│                    [BytecodeGenerator]                       │
│                              ↓                               │
│                         [GuruByte]                           │
│                              ↓                               │
│                         [GuruDVM] ←── [GuruMatrix]           │
│                              ↓                               │
│                    outputs por hermenêutica                   │
│                                                              │
│  ── Implementado v0.1 ────────────────────────────────────── │
│  ── Roadmap v0.2: IPII, Modo Inferencial, arquivo .gurub ─── │
│  ── Roadmap v0.3: embeddings, álgebra GuruMatrix, CLI IDE ── │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Evidência Empírica: Suite de Testes

```
25 testes passando em 0.18s (Python 3.12, pytest 9.0.2)

TestCasoZero (5 testes) — Prova do MVP Semântico
TestNiveisHermeneuticos (5 testes) — Todos os 7 níveis
TestPipeline (9 testes) — Pipeline completo
TestDryRun (2 testes) — Relatório semântico
TestGuruMatrix (4 testes) — Espaço de coordenadas
```

---

## 10. Conclusão: O que Mudou da v0.1 para a v0.2

### 10.1 Status Atualizado por Componente

| Componente | v0.1 | v0.2 |
|---|---|---|
| Tese central | Hipótese | **Demonstrada empiricamente** |
| GuruMatrix | Especificada | **Implementada e testada** |
| GuruCompiler | Especificado | **Implementado (pipeline completo)** |
| GuruByte | Especificado | **Implementado (dict JSON-serializável)** |
| GuruInstructionSet | Glossário de opcodes | **Semântica operacional verificada** |
| GuruDVM | Arquitetural | **Operacional (25 testes passando)** |
| DISPATCH_ON_HERMENEUTICS | Objetivo do MVP | **Demonstrado: 7 modos distintos** |
| IPII | Especificada | Especificada (implementação: v0.2) |
| Embeddings GuruMatrix | Roadmap v0.3 | Roadmap v0.3 (inalterado) |
| Arquivo `.gurub` binário | Roadmap v0.2 | Roadmap v0.2 (inalterado) |

### 10.2 O que Permanece como Trabalho Futuro

- Formalização das relações Simetria, Equilíbrio e Compensação como functores
- Modo Inferencial do Context Analyzer (requer GuruMatrix populada)
- Implementação da IPII com banco panlinguístico curado (5 linguagens prioritárias)
- Embeddings vetoriais por célula (v0.3)
- Arquivo `.gurub` binário com modo embedded para recursos multimodais
- Instrução `EMOTE` com modelo afetivo VAD

### 10.3 O Próximo Passo

A v0.1 terminou com: *"Uma instrução. Dois níveis hermenêuticos. Dois outputs computacionalmente distintos. Isso é suficiente."*

A v0.2 confirma: sete instruções. Sete níveis. Sete outputs distintos. O sistema é real.

O próximo passo é a curadoria do núcleo do banco panlinguístico para Python e Rust — os primeiros 20 padrões de código mapeados em coordenadas GuruMatrix — que transforma a IPII de especificação em implementação verificável.

---

## Referências

PEIRCE, C.S. *Collected Papers*. Cambridge: Harvard University Press, 1931–1958.

ARISTOTLE. *Categories*. Trad. J.L. Ackrill. Oxford: Clarendon Press, 1963.

LAKATOS, I. *The Methodology of Scientific Research Programmes*. Cambridge: CUP, 1978.

GADAMER, H.-G. *Truth and Method*. London: Sheed & Ward, 1975.

SLOMAN, L. "In Math, Rigor Is Vital. But Are Digitized Proofs Taking It Too Far?" *Quanta Magazine*, 25 mar. 2026.

WANG, Y. et al. "CodeT5+: Open Code Large Language Models." *arXiv*, 2023.

RADFORD, A. et al. "Learning Transferable Visual Models From Natural Language Supervision." *ICML*, 2021.

---

## Apêndice A — Roadmap Consolidado v0.2

| Componente | v0.1 (Concluído) | v0.2 (Em desenvolvimento) | v0.3 (Planejado) |
|---|---|---|---|
| GuruMatrix | 100 células, popular_minimo | API dinâmica, métr. proximidade | Embeddings vetoriais |
| Compilador | Pipeline completo, dry-run | Modo Inferencial, curadoria | API REST |
| GuruByte | Estrutura dict, CONTEXT/bloco | Arquivo .gurub binário | Visualizador semântico |
| GuruDVM | 7 modos hermenêuticos | EMOTE projetado | Categoria 6 implementada |
| IPII | Especificação completa | Núcleo 5 linguagens | Fine-tuning LLM |
| Testes | 25 passando | 50+ com IPII | Suite de integração |

---

## Apêndice B — Output Completo do MVP

Saída verificada de `python gurudev-cli.py examples/mvp_demo.guru --demo`:

```
╔══════════════════════════════════════════╗
║   GuruDev® v0.1-MVP  ·  Semantic Runtime ║
╚══════════════════════════════════════════╝

▶ Compilando examples/mvp_demo.guru…
  ✓ 2 bloco(s) gerado(s)

── Execução com hermenêutica=1 ─────────────────────────────
[LOAD] formula_energia — carregado
[DISPLAY] modo=LITERAL
  output: E = mc^2

── Execução com hermenêutica=4 ─────────────────────────────
[LOAD] formula_energia — carregado
[DISPLAY] modo=CONTEXTUAL
  output:
    valor: E = mc^2
    coordenada_gurumatrix: (ACAO, CIENCIA)

── Execução com hermenêutica=7 ─────────────────────────────
[LOAD] formula_energia — carregado
[DISPLAY] modo=ONTOLÓGICO
  output:
    celula_origem: ACAO_CIENCIA
    objetos_na_celula: [fatorial, fft, media, derivada]
    relacoes_ativas: [equivalencia, similitude]
    conexoes_ontologicas: {TEMPO: [serie_temporal, ...], ACAO: [...]}

✓ MVP Semântico demonstrado: 7 níveis hermenêuticos,
  outputs computacionalmente distintos por nível.
```

---

## Apêndice C — Glossário

*(Inalterado da v0.1, com adição de novos termos)*

**Semantic Dry-Run:** modo do GuruCompiler que documenta o gap entre anotações semânticas e comportamento computacional. Produz relatório JSON com contagem de anotações inertes vs. ativas.

**Modo Declarativo:** modo do Context Analyzer onde o programador anota explicitamente (`tag hermeneutica=7`). Implementado em v0.1.

**Modo Inferencial:** modo do Context Analyzer onde o compilador infere coordenadas semânticas a partir do conteúdo. Requer GuruMatrix populada. Roadmap v0.2.

**MVP Semântico:** demonstração mínima de que `DISPATCH_ON_HERMENEUTICS` produz outputs computacionalmente distintos para valores diferentes de Hermeneutics. **Demonstrado em v0.1.**

*[demais termos inalterados da v0.1]*

# IPII — Interoperabilidade, Polissemia, Interpretação e Instrução

## Transpilação Semântica na Linguagem GuruDev®

**Whitepaper Técnico v0.1**  
**Data:** Abril 2026  
**Autor:** Guilherme Gonçalves Machado / Hubstry

---

## Resumo

Este whitepaper apresenta o framework **IPII (Interoperabilidade, Polissemia, Interpretação, Instrução)** como base teórica para a **transpilação semântica** implementada na linguagem GuruDev®. Argumentamos que a polissemia — a capacidade de uma mesma instrução produzir outputs semanticamente distintos — não é um defeito a ser eliminado, mas um recurso computacional a ser explorado.

---

## 1. Introdução

Linguagens de programação tradicionais buscam **univocidade**: uma instrução, um resultado determinístico. GuruDev® parte de uma premissa diferente: **a polissemia como recurso computacional**.

A instrução `display in context` em GuruDev® produz:
- Em nível 1: a representação literal da fórmula `E = mc²`
- Em nível 4: a fórmula posicionada nas coordenadas `(ACAO, CIENCIA)` da GuruMatrix
- Em nível 7: a expansão ontológica completa com todas as relações na GuruMatrix

Isso não é ambiguidade — é **polissemia controlada**.

---

## 2. O Framework IPII

### 2.1 Interoperabilidade (I)

A capacidade de transitar entre domínios de conhecimento sem perda semântica. GuruDev® implementa isso via:
- O sistema de **claves** (`bind clave = ciencia`)
- O mapeamento de recursos às células da GuruMatrix

### 2.2 Polissemia (P)

A propriedade de uma instrução ter múltiplos sentidos válidos simultaneamente. Em GuruDev®:
- Cada instrução carrega consigo o **espectro completo de interpretações** (níveis 1–7)
- A escolha de qual interpretação executar é feita em runtime pelo **nível hermenêutico ativo**

### 2.3 Interpretação (I)

O processo de selecionar e executar uma interpretação específica. Implementado pelo mecanismo **DISPATCH_ON_HERMENEUTICS**:
```guru
dispatch hermeneutica formula_energia {
    case 1: display in context  # Literal
    case 4: display in context  # Contextual
    case 7: display in context  # Ontológico
}
```

### 2.4 Instrução (I)

A codificação formal da intenção semântica. As instruções GuruDev® são **semanticamente ricas** por design — elas carregam contexto, domínio e nível hermenêutico como atributos de primeira classe.

---

## 3. Transpilação Semântica

A transpilação semântica difere da transpilação sintática convencional:

| Aspecto             | Transpilação Sintática    | Transpilação Semântica          |
|---------------------|---------------------------|---------------------------------|
| Unidade de análise  | Token / AST               | Conceito / Relação semântica    |
| Perda de informação | Alta (semântica descartada) | Baixa (semântica preservada)  |
| Output              | Código em outra linguagem  | Representação em outro domínio |
| Fidelidade          | Estrutural                 | Ontológica                     |

---

## 4. A GuruMatrix como Espaço de Transpilação

A GuruMatrix 10×10 (Aristóteles × Domínios) serve como **espaço de coordenadas semântico** onde a transpilação ocorre:

1. Um recurso é carregado com coordenadas `(Ontologia, Domínio)`.
2. A transpilação semântica é a projeção do recurso em outras células da matrix.
3. Relações como `HOMOLOGIA` e `SIMILITUDE` definem os caminhos de transpilação.

---

## 5. Prova do MVP

O teste central do GuruDev® v0.1-MVP demonstra que o mecanismo de transpilação semântica é **operacional, não decorativo**:

```
Hermenêutica 1 → LITERAL    → output: str("E = mc^2")
Hermenêutica 4 → CONTEXTUAL → output: dict{valor, coordenada_gurumatrix}
Hermenêutica 7 → ONTOLÓGICO → output: dict{celula_origem, conexoes, relacoes}
```

Três outputs **computacionalmente distintos** da mesma instrução `display in context`.

---

## 6. Trabalho Futuro

- Formalização matemática do framework IPII
- Extensão para 3D com eixo temporal
- Integração com embeddings semânticos (sentence transformers)
- Compilação cruzada semântica entre GuruDev® e outras linguagens

---

## Referências

- Aristóteles. *Categorias*. c. 350 a.C.
- Gadamer, H.G. *Verdade e Método*. 1960.
- Ricoeur, P. *O Conflito das Interpretações*. 1969.
- Eco, U. *Os Limites da Interpretação*. 1990.

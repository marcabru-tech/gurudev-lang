"""
GuruMatrix Cells v0.2
Registro completo das 100 células (10 Ontologias × 10 Domínios).
Cada célula tem: name, handler, stub, description.
Células sem dado carregado são marcadas como stub=True.
"""
from __future__ import annotations

from typing import Any, Callable

from .core import CelulaGuruMatrix, Dominio, Ontologia, RelacaoSemantica

__all__ = [
    "CelulaGuruMatrix",
    "Ontologia",
    "Dominio",
    "RelacaoSemantica",
    "CELLS",
    "cell_meta",
]

# ── Handlers de stub (noop com documentação inline) ──────────────────────────

def _stub_handler(cell_name: str) -> Callable:
    """Retorna handler stub que sinaliza célula pendente."""
    def handler(*args: Any, **kwargs: Any) -> dict:
        return {"status": "stub", "cell": cell_name, "note": "Cell not yet implemented"}
    handler.__name__ = f"handler_{cell_name}"
    return handler


# ── Descrições por ontologia × domínio ────────────────────────────────────────

_DESCRIPTIONS: dict[str, str] = {
    # SUBSTANCIA ──────────────────────────────────────────────────────────────
    "SUBSTANCIA_ARTE":               "Matéria-prima artística: pigmentos, texturas, suportes.",
    "SUBSTANCIA_CIENCIA":            "Substâncias e materiais estudados pela ciência.",
    "SUBSTANCIA_FILOSOFIA":          "Substância como categoria metafísica (Aristóteles, Spinoza).",
    "SUBSTANCIA_TRADICAO_ESPIRITUAL":"Substâncias sagradas: elementos, oferendas, incenso.",
    "SUBSTANCIA_TECNOLOGIA":         "Tipos primitivos computacionais: int, string, array, dict.",
    "SUBSTANCIA_LINGUAGEM":          "Morfemas, fonemas e unidades lexicais básicas.",
    "SUBSTANCIA_MATEMATICA":         "Conjuntos, números e objetos matemáticos fundamentais.",
    "SUBSTANCIA_MEDICINA_BIOLOGIA":  "Biomoléculas, células e componentes orgânicos.",
    "SUBSTANCIA_DIREITO_ETICA":      "Pessoas jurídicas, bens e objetos de direito.",
    "SUBSTANCIA_EDUCACAO":           "Conteúdo e material didático bruto.",
    # QUANTIDADE ──────────────────────────────────────────────────────────────
    "QUANTIDADE_ARTE":               "Proporções, escalas e métricas estéticas.",
    "QUANTIDADE_CIENCIA":            "Grandezas físicas, medições e unidades SI.",
    "QUANTIDADE_FILOSOFIA":          "Quantidade como categoria lógica e ontológica.",
    "QUANTIDADE_TRADICAO_ESPIRITUAL":"Números sagrados, numerologia e ciclos cósmicos.",
    "QUANTIDADE_TECNOLOGIA":         "Complexidade algorítmica, bits, bytes e métricas computacionais.",
    "QUANTIDADE_LINGUAGEM":          "Frequência lexical, contagem de tokens e estatísticas textuais.",
    "QUANTIDADE_MATEMATICA":         "Cardinalidade, ordinalidade e teoria dos números.",
    "QUANTIDADE_MEDICINA_BIOLOGIA":  "Dosagens, concentrações e métricas clínicas.",
    "QUANTIDADE_DIREITO_ETICA":      "Penas, prazos, valores pecuniários e cotas.",
    "QUANTIDADE_EDUCACAO":           "Notas, horas-aula e índices de desempenho.",
    # QUALIDADE ───────────────────────────────────────────────────────────────
    "QUALIDADE_ARTE":                "Cor, textura, harmonia e ritmo — atributos qualitativos da arte.",
    "QUALIDADE_CIENCIA":             "Propriedades observáveis: estado físico, cor, viscosidade.",
    "QUALIDADE_FILOSOFIA":           "Qualidades essenciais e acidentais (Aristóteles).",
    "QUALIDADE_TRADICAO_ESPIRITUAL": "Virtudes espirituais, pureza e estados de consciência.",
    "QUALIDADE_TECNOLOGIA":          "Atributos de software: confiabilidade, performance, usabilidade.",
    "QUALIDADE_LINGUAGEM":           "Registro, tom e qualidade estilística do discurso.",
    "QUALIDADE_MATEMATICA":          "Propriedades algébricas: comutatividade, associatividade.",
    "QUALIDADE_MEDICINA_BIOLOGIA":   "Fenótipos, sintomas e características clínicas.",
    "QUALIDADE_DIREITO_ETICA":       "Licitude, culpabilidade e caráter ético de atos.",
    "QUALIDADE_EDUCACAO":            "Qualidade pedagógica, clareza e profundidade do ensino.",
    # RELACAO ─────────────────────────────────────────────────────────────────
    "RELACAO_ARTE":                  "Relações entre obras, movimentos e influências artísticas.",
    "RELACAO_CIENCIA":               "Leis científicas, correlações e causalidade.",
    "RELACAO_FILOSOFIA":             "Categorias relacionais: dependência, semelhança, identidade.",
    "RELACAO_TRADICAO_ESPIRITUAL":   "Relações sagradas: karma, dharma, interdependência.",
    "RELACAO_TECNOLOGIA":            "APIs, interfaces e contratos entre sistemas.",
    "RELACAO_LINGUAGEM":             "Relações sintáticas, semânticas e pragmáticas.",
    "RELACAO_MATEMATICA":            "Funções, morfismos e relações de equivalência.",
    "RELACAO_MEDICINA_BIOLOGIA":     "Redes metabólicas, interações moleculares e ecossistemas.",
    "RELACAO_DIREITO_ETICA":         "Obrigações, direitos e relações jurídicas.",
    "RELACAO_EDUCACAO":              "Relações pedagógicas: tutor-aprendiz, currículo-objetivo.",
    # LUGAR ───────────────────────────────────────────────────────────────────
    "LUGAR_ARTE":                    "Espaços de exposição, palcos e contextos de apresentação.",
    "LUGAR_CIENCIA":                 "Laboratórios, campos de pesquisa e ecossistemas.",
    "LUGAR_FILOSOFIA":               "Topologia filosófica: espaço, mundo, contexto.",
    "LUGAR_TRADICAO_ESPIRITUAL":     "Lugares sagrados: templos, altares e sítios rituais.",
    "LUGAR_TECNOLOGIA":              "Infraestrutura computacional: servidores, redes, nuvem.",
    "LUGAR_LINGUAGEM":               "Variedades regionais e contextos comunicativos.",
    "LUGAR_MATEMATICA":              "Espaços topológicos, métricas e variedades.",
    "LUGAR_MEDICINA_BIOLOGIA":       "Biomas, habitats e sistemas corporais.",
    "LUGAR_DIREITO_ETICA":           "Jurisdições, territórios e foros legais.",
    "LUGAR_EDUCACAO":                "Ambientes de aprendizagem: escola, EaD, informal.",
    # TEMPO ────────────────────────────────────────────────────────────────────
    "TEMPO_ARTE":                    "Tempo musical, duração performática e periodização histórica.",
    "TEMPO_CIENCIA":                 "Séries temporais, frequência, timestamp e dinâmica.",
    "TEMPO_FILOSOFIA":               "Tempo como categoria fenomenológica e metafísica.",
    "TEMPO_TRADICAO_ESPIRITUAL":     "Ciclos cósmicos, calendários sagrados e eternidade.",
    "TEMPO_TECNOLOGIA":              "Latência, throughput, TTL e ciclos de processamento.",
    "TEMPO_LINGUAGEM":               "Tempo verbal, aspecto e temporalidade discursiva.",
    "TEMPO_MATEMATICA":              "Análise temporal, séries de Fourier e dinâmica.",
    "TEMPO_MEDICINA_BIOLOGIA":       "Cronobiologia, farmacocinética e evolução.",
    "TEMPO_DIREITO_ETICA":           "Prazos processuais, vigência e prescrição.",
    "TEMPO_EDUCACAO":                "Progressão curricular, carga horária e ritmo de aprendizagem.",
    # SITUACAO ────────────────────────────────────────────────────────────────
    "SITUACAO_ARTE":                 "Estado de uma obra: restauração, exposição, coleção.",
    "SITUACAO_CIENCIA":              "Estado de um sistema: equilíbrio, fase, configuração.",
    "SITUACAO_FILOSOFIA":            "Situação existencial, condição e facticidade.",
    "SITUACAO_TRADICAO_ESPIRITUAL":  "Estados espirituais: meditação, êxtase, iluminação.",
    "SITUACAO_TECNOLOGIA":           "Estado de sistema: running, idle, error, deprecated.",
    "SITUACAO_LINGUAGEM":            "Situação discursiva, register e contexto pragmático.",
    "SITUACAO_MATEMATICA":           "Configurações e estados de sistemas dinâmicos.",
    "SITUACAO_MEDICINA_BIOLOGIA":    "Estado clínico: diagnóstico, prognóstico, remissão.",
    "SITUACAO_DIREITO_ETICA":        "Situação jurídica: contencioso, acordo, nulidade.",
    "SITUACAO_EDUCACAO":             "Situação pedagógica: cursa, aprovado, evasão.",
    # CONDICAO ────────────────────────────────────────────────────────────────
    "CONDICAO_ARTE":                 "Condições de criação: censura, mecenato, liberdade expressiva.",
    "CONDICAO_CIENCIA":              "Condições experimentais: temperatura, pressão, controle.",
    "CONDICAO_FILOSOFIA":            "Condições de possibilidade (Kant), pressupostos.",
    "CONDICAO_TRADICAO_ESPIRITUAL":  "Requisitos espirituais: iniciação, purificação, votos.",
    "CONDICAO_TECNOLOGIA":           "Pré-condições e pós-condições de contratos de software.",
    "CONDICAO_LINGUAGEM":            "Condições de verdade e de felicidade de enunciados.",
    "CONDICAO_MATEMATICA":           "Hipóteses, axiomas e condições de contorno.",
    "CONDICAO_MEDICINA_BIOLOGIA":    "Comorbidades, fatores de risco e condições clínicas.",
    "CONDICAO_DIREITO_ETICA":        "Condições de validade de atos jurídicos.",
    "CONDICAO_EDUCACAO":             "Pré-requisitos e condições de acesso ao ensino.",
    # ACAO ────────────────────────────────────────────────────────────────────
    "ACAO_ARTE":                     "Atos criativos: pintar, compor, esculpir, performar.",
    "ACAO_CIENCIA":                  "Operações científicas: calcular, medir, experimentar.",
    "ACAO_FILOSOFIA":                "Atos filosóficos: argumentar, contemplar, refutar.",
    "ACAO_TRADICAO_ESPIRITUAL":      "Práticas espirituais: orar, meditar, ritualizar.",
    "ACAO_TECNOLOGIA":               "Operações computacionais: executar, compilar, testar.",
    "ACAO_LINGUAGEM":                "Atos de fala: afirmar, questionar, prometer.",
    "ACAO_MATEMATICA":               "Operações matemáticas: somar, integrar, provar.",
    "ACAO_MEDICINA_BIOLOGIA":        "Procedimentos médicos: diagnosticar, tratar, cirurgiar.",
    "ACAO_DIREITO_ETICA":            "Atos jurídicos: contratar, legislar, julgar.",
    "ACAO_EDUCACAO":                 "Atos pedagógicos: ensinar, avaliar, orientar.",
    # PAIXAO ──────────────────────────────────────────────────────────────────
    "PAIXAO_ARTE":                   "Emoções evocadas pela arte: catarse, sublime, beleza.",
    "PAIXAO_CIENCIA":                "Motivações científicas: curiosidade, descoberta, maravilha.",
    "PAIXAO_FILOSOFIA":              "Afetos filosóficos: espanto, dúvida, amor pelo saber.",
    "PAIXAO_TRADICAO_ESPIRITUAL":    "Devoção, fé, êxtase e amor transcendente.",
    "PAIXAO_TECNOLOGIA":             "Impacto humano da tecnologia: dependência, ansiedade, prazer.",
    "PAIXAO_LINGUAGEM":              "Carga emocional da linguagem: metáforas afetivas, retórica.",
    "PAIXAO_MATEMATICA":             "Elegância, beleza e prazer estético em matemática.",
    "PAIXAO_MEDICINA_BIOLOGIA":      "Empatia, sofrimento, cura e experiência do adoecer.",
    "PAIXAO_DIREITO_ETICA":          "Senso de justiça, indignação moral e compaixão.",
    "PAIXAO_EDUCACAO":               "Motivação intrínseca, paixão pelo aprendizado e vocação.",
}

# ── Construção do registro CELLS ──────────────────────────────────────────────

def _build_cells() -> dict[str, dict]:
    """Gera o registro CELLS cobrindo todas as 100 células (10×10)."""
    cells: dict[str, dict] = {}
    for ont in Ontologia:
        for dom in Dominio:
            name = f"{ont.name}_{dom.name}"
            desc = _DESCRIPTIONS.get(name, f"Célula {name}: stub pendente.")
            cells[name] = {
                "name": name,
                "ontologia": ont.name,
                "dominio": dom.name,
                "handler": _stub_handler(name),
                "stub": True,        # todas começam como stub; handler real substitui
                "description": desc,
            }
    return cells


CELLS: dict[str, dict] = _build_cells()
assert len(CELLS) == 100, f"CELLS must have exactly 100 entries, has {len(CELLS)}"


def cell_meta(ont: Ontologia, dom: Dominio) -> dict:
    """Retorna metadados da célula para (Ontologia, Dominio)."""
    name = f"{ont.name}_{dom.name}"
    return CELLS[name]


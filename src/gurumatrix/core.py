"""
GuruMatrix v0.1-MVP
Espaço de coordenadas semânticas 10x10
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum, auto

class Ontologia(Enum):
    SUBSTANCIA = 1
    QUANTIDADE = 2
    QUALIDADE  = 3
    RELACAO    = 4
    LUGAR      = 5
    TEMPO      = 6
    SITUACAO   = 7
    CONDICAO   = 8
    ACAO       = 9
    PAIXAO     = 10

class Dominio(Enum):
    ARTE               = 1
    CIENCIA            = 2
    FILOSOFIA          = 3
    TRADICAO_ESPIRITUAL= 4
    TECNOLOGIA         = 5
    LINGUAGEM          = 6
    MATEMATICA         = 7
    MEDICINA_BIOLOGIA  = 8
    DIREITO_ETICA      = 9
    EDUCACAO           = 10

class RelacaoSemantica(Enum):
    SIMILITUDE   = "similitude"
    HOMOLOGIA    = "homologia"
    EQUIVALENCIA = "equivalencia"
    SIMETRIA     = "simetria"
    EQUILIBRIO   = "equilibrio"
    COMPENSACAO  = "compensacao"

@dataclass
class CelulaGuruMatrix:
    x: Ontologia
    y: Dominio
    objetos: List[str]                        = field(default_factory=list)
    relacoes_ativas: List[RelacaoSemantica]   = field(default_factory=list)
    instrucoes_preferenciais: List[str]       = field(default_factory=list)
    embedding: Optional[List[float]]          = None

    def __post_init__(self):
        self.coordenada = (self.x.value, self.y.value)
        self.nome = f"{self.x.name}_{self.y.name}"

    def adicionar_objeto(self, nome: str):
        if nome not in self.objetos:
            self.objetos.append(nome)

    def __repr__(self):
        return f"Celula[{self.x.name}][{self.y.name}]: {len(self.objetos)} objetos"


class GuruMatrix:
    def __init__(self):
        self.celulas: Dict[tuple, CelulaGuruMatrix] = {}
        self._inicializar()

    def _inicializar(self):
        for x in Ontologia:
            for y in Dominio:
                self.celulas[(x.value, y.value)] = CelulaGuruMatrix(x, y)

    def get(self, x: Ontologia, y: Dominio) -> CelulaGuruMatrix:
        return self.celulas[(x.value, y.value)]

    def get_by_name(self, x_name: str, y_name: str) -> Optional[CelulaGuruMatrix]:
        try:
            x = Ontologia[x_name.upper()]
            y = Dominio[y_name.upper()]
            return self.get(x, y)
        except KeyError:
            return None

    def popular_minimo(self):
        c = self.get(Ontologia.ACAO, Dominio.CIENCIA)
        for obj in ["fatorial", "fft", "media", "derivada"]:
            c.adicionar_objeto(obj)
        c.relacoes_ativas = [RelacaoSemantica.EQUIVALENCIA, RelacaoSemantica.SIMILITUDE]
        c.instrucoes_preferenciais = ["EVALUATE", "APPLY", "COMPARE"]

        c = self.get(Ontologia.QUALIDADE, Dominio.ARTE)
        for obj in ["cor", "textura", "harmonia", "ritmo"]:
            c.adicionar_objeto(obj)
        c.relacoes_ativas = [RelacaoSemantica.SIMETRIA, RelacaoSemantica.EQUILIBRIO]
        c.instrucoes_preferenciais = ["DISPLAY", "TRANSCODE", "EMOTE"]

        c = self.get(Ontologia.RELACAO, Dominio.MATEMATICA)
        for obj in ["funcao", "morfismo", "isomorfismo"]:
            c.adicionar_objeto(obj)
        c.relacoes_ativas = [RelacaoSemantica.HOMOLOGIA, RelacaoSemantica.EQUIVALENCIA]
        c.instrucoes_preferenciais = ["MAP_TO", "INTEROP_MAP"]

        c = self.get(Ontologia.SUBSTANCIA, Dominio.TECNOLOGIA)
        for obj in ["int", "string", "array", "dict"]:
            c.adicionar_objeto(obj)
        c.instrucoes_preferenciais = ["LOAD", "BIND"]

        c = self.get(Ontologia.TEMPO, Dominio.CIENCIA)
        for obj in ["serie_temporal", "timestamp", "frequencia"]:
            c.adicionar_objeto(obj)
        c.instrucoes_preferenciais = ["APPLY FFT", "EVALUATE", "COMPARE"]

    def __repr__(self):
        total = sum(len(c.objetos) for c in self.celulas.values())
        return f"GuruMatrix(100 células, {total} objetos mapeados)"


class Inefavel:
    """Tipo para fenômenos fora do espaço de representação atual."""
    def __init__(self, motivo: str):
        self.motivo = motivo

    def __repr__(self):
        return f"Inefável: {self.motivo}"

    def to_guruwarning(self) -> dict:
        return {
            "tipo": "GuruWarning",
            "mensagem": f"Fenômeno não mapeável: {self.motivo}",
            "acao_recomendada": "Solicitar extensão de domínio ao usuário",
        }

"""
GuruMatrix v0.1-MVP
Espaço de coordenadas semânticas 10x10
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from gurudev.exceptions import SemanticError


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
        self._carregar_dados_v02()

    def _carregar_dados_v02(self):
        import json
        from pathlib import Path

        # Carregar objetos e relações
        data_path = Path(__file__).parent / "data_v0.2.json"
        if data_path.exists():
            with open(data_path, "r") as f:
                dados = json.load(f)
                for chave, info in dados.items():
                    try:
                        ont_name, dom_name = chave.split("_")
                        celula = self.get_by_name_safe(ont_name, dom_name)
                        if celula:
                            celula.objetos = info.get("objetos", [])
                            celula.relacoes_ativas = [RelacaoSemantica(r) for r in info.get("relacoes", [])]
                            celula.instrucoes_preferenciais = info.get("instrucoes", [])
                    except Exception:
                        continue

        # Carregar embeddings
        emb_path = Path(__file__).parent / "embeddings_v0.2.json"
        if emb_path.exists():
            with open(emb_path, "r") as f:
                embs = json.load(f)
                for nome_celula, vetor in embs.items():
                    try:
                        ont_name, dom_name = nome_celula.split("_")
                        celula = self.get_by_name_safe(ont_name, dom_name)
                        if celula:
                            celula.embedding = vetor
                    except Exception:
                        continue

    def get(self, x: Ontologia, y: Dominio) -> 'CelulaGuruMatrix':
        """Retorna célula pela coordenada (Ontologia, Dominio).

        Raises:
            SemanticError: se a coordenada não existir na matrix (nunca ocorre
                           com enums válidos, mas protege contra extensões futuras).
        """
        key = (x.value, y.value)
        if key not in self.celulas:
            raise SemanticError(
                f"Célula fantasma detectada: ({x.name}, {y.name}) não existe na GuruMatrix.",
                suggestion="Use um valor válido de Ontologia e Dominio.",
            )
        return self.celulas[key]

    def get_by_name(self, x_name: str, y_name: str) -> 'CelulaGuruMatrix':
        """Retorna célula pelos nomes das enums.

        Raises:
            SemanticError: se qualquer um dos nomes for inválido.
        """
        try:
            x = Ontologia[x_name.upper()]
        except KeyError:
            valid = [o.name for o in Ontologia]
            raise SemanticError(
                f"Ontologia inválida: '{x_name}'. Valores válidos: {valid}",
                suggestion=f"Use um dos valores válidos de Ontologia: {valid}",
            )
        try:
            y = Dominio[y_name.upper()]
        except KeyError:
            valid = [d.name for d in Dominio]
            raise SemanticError(
                f"Domínio inválido: '{y_name}'. Valores válidos: {valid}",
                suggestion=f"Use um dos valores válidos de Dominio: {valid}",
            )
        return self.get(x, y)

    def get_by_name_safe(self, x_name: str, y_name: str) -> Optional['CelulaGuruMatrix']:
        """Versão que retorna None em vez de levantar exceção (para compatibilidade)."""
        try:
            return self.get_by_name(x_name, y_name)
        except SemanticError:
            return None

    def validate_cell_reference(self, name: str) -> bool:
        """Valida se um nome de célula 'ONTOLOGIA_DOMINIO' é válido.

        Returns True se válido, raises SemanticError se não.
        """
        parts = name.split("_", 1)
        if len(parts) != 2:
            raise SemanticError(
                f"Nome de célula inválido: '{name}'. Formato esperado: 'ONTOLOGIA_DOMINIO'.",
                suggestion="Use o formato ONTOLOGIA_DOMINIO, ex: ACAO_CIENCIA",
            )
        self.get_by_name(parts[0], parts[1])
        return True

    def buscar_homologos(self, ont: Ontologia, dom_origem: Dominio) -> List[Dict[str, Any]]:
        """Busca objetos na mesma categoria ontológica em outros domínios."""
        homologos = []
        for dom in Dominio:
            if dom == dom_origem:
                continue
            celula = self.get(ont, dom)
            if celula.objetos:
                homologos.append({
                    "dominio": dom.name,
                    "objetos": celula.objetos,
                    "relacao": RelacaoSemantica.HOMOLOGIA.value
                })
        return homologos

    def buscar_similitudes(self, dom: Dominio, ont_origem: Ontologia) -> List[Dict[str, Any]]:
        """Busca objetos no mesmo domínio em outras categorias ontológicas."""
        similitudes = []
        for ont in Ontologia:
            if ont == ont_origem:
                continue
            celula = self.get(ont, dom)
            if celula.objetos:
                similitudes.append({
                    "ontologia": ont.name,
                    "objetos": celula.objetos,
                    "relacao": RelacaoSemantica.SIMILITUDE.value
                })
        return similitudes

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

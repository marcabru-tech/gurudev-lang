"""GuruDev Instruction Set — opcodes e estruturas de instrução."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ── Opcodes disponíveis ─────────────────────────────────────────────────────

OPCODES = {
    "LOAD": "Carrega um recurso no contexto de execução.",
    "DISPLAY": "Exibe um recurso com comportamento dependente do nível hermenêutico.",
    "EVALUATE": "Avalia um recurso (literal, simbólico ou ontológico).",
    "TRANSCODE": "Transcreve um recurso para outro domínio ou formato.",
    "BIND": "Vincula a clave do contexto.",
    "TAG": "Define o nível hermenêutico do contexto.",
    "MAP_TO": "Mapeia o contexto para uma nova clave.",
    "DISPATCH_ON_HERMENEUTICS": "Executa um bloco condicional por nível hermenêutico.",
    "EMOTE": "Emite uma expressão emocional/estética (nível 6+).",
}


@dataclass
class Instruction:
    """Representa uma instrução GuruByte."""

    opcode: str
    operandos: List[Any] = field(default_factory=list)
    modificadores: Dict[str, Any] = field(default_factory=dict)
    contexto_hermeneutica: int = 1
    contexto_clave: str = "geral"
    linha: int = 0

    def to_dict(self) -> dict:
        return {
            "opcode": self.opcode,
            "operandos": self.operandos,
            "modificadores": self.modificadores,
            "contexto_hermeneutica": self.contexto_hermeneutica,
            "contexto_clave": self.contexto_clave,
            "linha": self.linha,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Instruction":
        return cls(
            opcode=data.get("opcode", "NOP"),
            operandos=data.get("operandos", []),
            modificadores=data.get("modificadores", {}),
            contexto_hermeneutica=data.get("contexto_hermeneutica", 1),
            contexto_clave=data.get("contexto_clave", "geral"),
            linha=data.get("linha", 0),
        )

    def __repr__(self) -> str:
        ops = ", ".join(str(o) for o in self.operandos)
        return f"Instruction({self.opcode}, [{ops}], h={self.contexto_hermeneutica})"


def is_valid_opcode(opcode: str) -> bool:
    """Verifica se um opcode é válido."""
    return opcode in OPCODES


def describe_opcode(opcode: str) -> Optional[str]:
    """Retorna a descrição de um opcode."""
    return OPCODES.get(opcode)

"""GuruDev Dispatch — mecanismo de dispatch hermenêutico."""
from typing import Any, Callable, Dict, List, Optional


# ── Registro de handlers por nível ─────────────────────────────────────────

_HANDLERS: Dict[int, Callable] = {}


def register_handler(nivel: int):
    """Decorator para registrar um handler de nível hermenêutico."""
    def decorator(fn: Callable) -> Callable:
        _HANDLERS[nivel] = fn
        return fn
    return decorator


def dispatch(nivel: int, recurso_nome: str, valor: Any, clave: str) -> dict:
    """
    Despacha a execução para o handler do nível hermenêutico.

    Args:
        nivel: Nível hermenêutico (1–7).
        recurso_nome: Nome do recurso sendo processado.
        valor: Valor do recurso.
        clave: Clave semântica do contexto atual.

    Returns:
        dict com o resultado do dispatch.
    """
    handler = _HANDLERS.get(nivel) or _HANDLERS.get(0)
    if handler is None:
        return _default_dispatch(nivel, recurso_nome, valor, clave)
    return handler(recurso_nome, valor, clave)


def _default_dispatch(nivel: int, nome: str, valor: Any, clave: str) -> dict:
    """Handler padrão quando nenhum handler específico está registrado."""
    return {
        "nivel": nivel,
        "modo": "DEFAULT",
        "output": str(valor),
        "recurso": nome,
        "clave": clave,
    }


# ── Handlers padrão registrados ────────────────────────────────────────────

@register_handler(1)
def _handle_literal(nome: str, valor: Any, clave: str) -> dict:
    """Nível 1 — LITERAL: representação bruta do valor."""
    return {
        "nivel": 1,
        "modo": "LITERAL",
        "output": str(valor),
        "descricao": "Representação literal do recurso sem interpretação.",
    }


@register_handler(4)
def _handle_contextual(nome: str, valor: Any, clave: str) -> dict:
    """Nível 4 — CONTEXTUAL: valor contextualizado na GuruMatrix."""
    coord = f"ACAO_{clave.upper()}" if clave else "SUBSTANCIA_TECNOLOGIA"
    return {
        "nivel": 4,
        "modo": "CONTEXTUAL",
        "output": {"valor": str(valor), "coordenada_gurumatrix": coord},
        "descricao": "Recurso contextualizado na GuruMatrix.",
    }


@register_handler(7)
def _handle_ontologico(nome: str, valor: Any, clave: str) -> dict:
    """Nível 7 — ONTOLÓGICO: expansão completa na GuruMatrix."""
    return {
        "nivel": 7,
        "modo": "ONTOLÓGICO",
        "output": {
            "celula_origem": f"ACAO_{clave.upper()}" if clave else "SUBSTANCIA_TECNOLOGIA",
            "objetos_na_celula": [str(valor)],
            "relacoes_ativas": [],
            "instrucoes_preferenciais": [],
            "conexoes_ontologicas": {},
        },
        "descricao": "Expansão ontológica completa: todas as relações na GuruMatrix.",
    }


def list_registered_levels() -> List[int]:
    """Retorna os níveis hermenêuticos com handlers registrados."""
    return sorted(_HANDLERS.keys())

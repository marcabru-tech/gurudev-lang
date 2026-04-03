"""
GuruDev Context Analyzer v0.1-MVP
Percorre a GuruAST e propaga contexto semântico
(clave, hermeneutica, ontologia) para cada nó.
Modo: Declarativo (anotações explícitas do programador).
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from compiler.parser import (
    NoAST, Programa, TagHermeneutica, BindClave,
    Instrucao, DispatchHermeneutica, FuncaoDecl, Literal, Identificador
)

CLAVE_PARA_ONTOLOGIA: Dict[str, str] = {
    "ciencia":   "ACAO",
    "arte":      "QUALIDADE",
    "filosofia": "RELACAO",
    "matematica":"RELACAO",
    "tecnologia":"SUBSTANCIA",
    "linguagem": "SUBSTANCIA",
    "educacao":  "SITUACAO",
    "geral":     "SUBSTANCIA",
}

@dataclass
class ContextoAtual:
    clave: str = "geral"
    hermeneutica: int = 1
    ontologia: str = "SUBSTANCIA"

    def copia(self) -> 'ContextoAtual':
        return ContextoAtual(self.clave, self.hermeneutica, self.ontologia)

    def atualizar_clave(self, clave: str):
        self.clave = clave
        self.ontologia = CLAVE_PARA_ONTOLOGIA.get(clave, "SUBSTANCIA")

    def to_dict(self) -> dict:
        return {"clave": self.clave, "hermeneutica": self.hermeneutica,
                "ontologia": self.ontologia}


class ContextAnalyzer:
    def __init__(self):
        self.dry_run_report: List[dict] = []

    def analisar(self, programa: Programa) -> Programa:
        ctx = ContextoAtual()
        self._visitar_lista(programa.declaracoes, ctx)
        return programa

    def _visitar_lista(self, nos: List[NoAST], ctx: ContextoAtual):
        for no in nos:
            self._visitar(no, ctx)

    def _visitar(self, no: NoAST, ctx: ContextoAtual):
        if isinstance(no, TagHermeneutica):
            ctx.hermeneutica = no.nivel
            no.hermeneutica = no.nivel

        elif isinstance(no, BindClave):
            ctx.atualizar_clave(no.campo)
            no.clave = no.campo
            no.ontologia = ctx.ontologia

        elif isinstance(no, Instrucao):
            # Propaga contexto para a instrução
            no.clave = ctx.clave
            no.hermeneutica = ctx.hermeneutica
            no.ontologia = ctx.ontologia

            # Dry-run: verifica se anotações têm despacho associado
            if no.opcode in ("DISPLAY", "EVALUATE", "LOAD"):
                tem_dispatch = False  # será verificado pelo bytecode gen
                self.dry_run_report.append({
                    "opcode": no.opcode,
                    "hermeneutica": ctx.hermeneutica,
                    "clave": ctx.clave,
                    "linha": no.linha,
                    "status": "PENDENTE_VERIFICACAO",
                })

        elif isinstance(no, DispatchHermeneutica):
            no.clave = ctx.clave
            no.hermeneutica = ctx.hermeneutica
            no.ontologia = ctx.ontologia

            # Marca todos os casos com contexto local
            for nivel, corpo in no.casos.items():
                ctx_caso = ctx.copia()
                ctx_caso.hermeneutica = nivel
                self._visitar_lista(corpo.instrucoes, ctx_caso)
            if no.padrao:
                self._visitar_lista(no.padrao, ctx)

            # Atualiza dry-run: dispatch encontrado, instrução é semântica real
            for entry in self.dry_run_report:
                if entry["status"] == "PENDENTE_VERIFICACAO":
                    entry["status"] = "ATIVA_COM_DESPACHO"

        elif isinstance(no, FuncaoDecl):
            ctx_func = ctx.copia()
            self._visitar_lista(no.corpo, ctx_func)

    def relatorio_dry_run(self) -> dict:
        inertes = [e for e in self.dry_run_report if e["status"] == "PENDENTE_VERIFICACAO"]
        ativos  = [e for e in self.dry_run_report if e["status"] == "ATIVA_COM_DESPACHO"]
        total   = len(self.dry_run_report)
        return {
            "total_anotacoes": total,
            "ativas_com_despacho": len(ativos),
            "inertes": len(inertes),
            "gap_semantico": f"{len(inertes)}/{total} anotações sem despacho semântico associado",
            "detalhes": self.dry_run_report,
        }

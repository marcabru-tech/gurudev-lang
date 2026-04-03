"""
GuruDev Bytecode Generator v0.1-MVP
GuruAST → GuruByte (representação dict, serializável em JSON)
"""
import json
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from compiler.parser import (
    NoAST, Programa, TagHermeneutica, BindClave,
    Instrucao, DispatchHermeneutica, FuncaoDecl, Literal, Identificador
)

class BytecodeGenerator:
    def __init__(self, versao: str = "0.1.0"):
        self.versao = versao
        self.bloco_idx = 0
        self.contexto_global = {
            "clave": "geral", "hermeneutics": 1, "ontologia": "SUBSTANCIA", "tags": []
        }

    def _novo_id_bloco(self) -> str:
        self.bloco_idx += 1
        return f"BLOCK_{self.bloco_idx:04d}"

    def gerar(self, programa: Programa, semantic_mode: str = "declarative") -> dict:
        self.bloco_idx = 0
        codeblocks = []
        constantes = {}
        contexto_atual = dict(self.contexto_global)

        for no in programa.declaracoes:
            resultado = self._gerar_no(no, contexto_atual, constantes)
            if resultado:
                codeblocks.extend(resultado if isinstance(resultado, list) else [resultado])

        gurubyte = {
            "HEADER": {
                "signature": "GURU",
                "version": self.versao,
                "encoding": "UTF-8",
                "compiler": f"GuruCompiler {self.versao}",
                "semantic_mode": semantic_mode,
                "packaging": "ref",
            },
            "CONTEXT_DEFAULT": dict(self.contexto_global),
            "CONSTANTS": constantes,
            "CODEBLOCKS": codeblocks,
            "FOOTER": {}
        }

        # Checksum
        payload = json.dumps(codeblocks, ensure_ascii=False).encode()
        gurubyte["FOOTER"]["checksum"] = f"SHA256-{hashlib.sha256(payload).hexdigest()[:16]}"
        gurubyte["FOOTER"]["compiler"] = f"GuruCompiler {self.versao}"

        return gurubyte

    def _gerar_no(self, no: NoAST, ctx: dict, constantes: dict) -> Optional[Any]:
        if isinstance(no, TagHermeneutica):
            ctx["hermeneutics"] = no.nivel
            return None  # anotação pura — sem bloco

        elif isinstance(no, BindClave):
            ctx["clave"] = no.campo
            return None

        elif isinstance(no, Instrucao):
            bid = self._novo_id_bloco()
            return {
                "id": bid,
                "CONTEXT": dict(ctx),
                "instructions": [self._serializar_instrucao(no)],
            }

        elif isinstance(no, DispatchHermeneutica):
            bid = self._novo_id_bloco()
            casos_serializados = {}
            for nivel, corpo in no.casos.items():
                casos_serializados[str(nivel)] = [
                    self._serializar_instrucao(i) for i in corpo.instrucoes
                ]
            padrao_serial = None
            if no.padrao:
                padrao_serial = [self._serializar_instrucao(i) for i in no.padrao]

            return {
                "id": bid,
                "CONTEXT": dict(ctx),
                "type": "DISPATCH_ON_HERMENEUTICS",
                "recurso": no.recurso,
                "casos": casos_serializados,
                "default": padrao_serial,
            }

        elif isinstance(no, FuncaoDecl):
            bid = self._novo_id_bloco()
            instrucoes = []
            for filho in no.corpo:
                r = self._gerar_no(filho, dict(ctx), constantes)
                if r:
                    instrucoes.append(r)
            return {
                "id": bid,
                "CONTEXT": dict(ctx),
                "type": "FUNCTION",
                "nome": no.nome,
                "parametros": no.parametros,
                "corpo": instrucoes,
            }

        return None

    def _serializar_instrucao(self, no: NoAST) -> dict:
        if isinstance(no, Instrucao):
            return {
                "opcode": no.opcode,
                "operandos": no.operandos,
                "modificadores": no.modificadores,
                "contexto_hermeneutica": no.hermeneutica,
                "contexto_clave": no.clave,
            }
        elif isinstance(no, TagHermeneutica):
            return {"opcode": "TAG", "hermeneutica": no.nivel}
        elif isinstance(no, BindClave):
            return {"opcode": "BIND", "clave": no.campo}
        elif isinstance(no, DispatchHermeneutica):
            # dispatch aninhado
            casos = {str(k): [self._serializar_instrucao(i) for i in v.instrucoes]
                     for k, v in no.casos.items()}
            return {"opcode": "DISPATCH_ON_HERMENEUTICS", "recurso": no.recurso, "casos": casos}
        return {"opcode": "UNKNOWN", "no": str(type(no))}

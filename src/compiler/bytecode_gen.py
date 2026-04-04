"""
GuruDev Bytecode Generator v0.2
GuruAST → GuruByte (representação dict, serializável em JSON)
"""
import hashlib
import json
from typing import Any, List, Optional

from compiler.parser import (
    AssignNode,
    BinaryOpNode,
    BindClave,
    BlockNode,
    CallNode,
    DispatchHermeneutica,
    ForNode,
    FuncaoDecl,
    Identificador,
    IfNode,
    Instrucao,
    Literal,
    NoAST,
    Programa,
    TagHermeneutica,
    WhileNode,
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

        elif isinstance(no, AssignNode):
            bid = self._novo_id_bloco()
            return {
                "id": bid,
                "CONTEXT": dict(ctx),
                "type": "ASSIGN",
                "var": no.name,
                "expr": self._serializar_expr(no.value),
            }

        elif isinstance(no, IfNode):
            bid = self._novo_id_bloco()
            then_blocks = self._gerar_bloco(no.then_block, ctx, constantes)
            else_blocks = self._gerar_bloco(no.else_block, ctx, constantes) if no.else_block else []
            return {
                "id": bid,
                "CONTEXT": dict(ctx),
                "type": "IF",
                "condition": self._serializar_expr(no.condition),
                "then": then_blocks,
                "else": else_blocks,
            }

        elif isinstance(no, WhileNode):
            bid = self._novo_id_bloco()
            body_blocks = self._gerar_bloco(no.body_block, ctx, constantes)
            return {
                "id": bid,
                "CONTEXT": dict(ctx),
                "type": "WHILE",
                "condition": self._serializar_expr(no.condition),
                "body": body_blocks,
            }

        elif isinstance(no, ForNode):
            bid = self._novo_id_bloco()
            body_blocks = self._gerar_bloco(no.body_block, ctx, constantes)
            return {
                "id": bid,
                "CONTEXT": dict(ctx),
                "type": "FOR",
                "var": no.var_name,
                "iterable": self._serializar_expr(no.iterable_expr),
                "body": body_blocks,
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

    def _gerar_bloco(self, bloco: Optional[BlockNode], ctx: dict, constantes: dict) -> List[dict]:
        """Serializa um BlockNode como lista de sub-blocos."""
        if bloco is None:
            return []
        result = []
        for stmt in bloco.statements:
            r = self._gerar_no(stmt, dict(ctx), constantes)
            if r is not None:
                result.append(r)
        return result

    def _serializar_expr(self, no: Optional[NoAST]) -> dict:
        """Serializa uma expressão AST como dict JSON-serializável."""
        if no is None:
            return {"kind": "literal", "value": None}
        if isinstance(no, Literal):
            return {"kind": "literal", "value": no.valor}
        if isinstance(no, Identificador):
            return {"kind": "var", "name": no.nome}
        if isinstance(no, BinaryOpNode):
            return {
                "kind": "binop",
                "op": no.op,
                "left": self._serializar_expr(no.left),
                "right": self._serializar_expr(no.right),
            }
        if isinstance(no, CallNode):
            return {
                "kind": "call",
                "func": no.func,
                "args": [self._serializar_expr(a) for a in no.args],
            }
        return {"kind": "unknown"}

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

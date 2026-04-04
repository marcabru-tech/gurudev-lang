"""
GuruDVM v0.2
Runtime bicameral: executa plano sintático e plano semântico simultaneamente.
Núcleo do MVP: DISPATCH_ON_HERMENEUTICS produz outputs computacionalmente distintos.
Controle de fluxo (if/while/for) com DecisionTrace para níveis 4–7.
"""
from typing import Any, Dict, List, Optional

from gurumatrix.core import Dominio, GuruMatrix, Ontologia

# ── DecisionTrace ────────────────────────────────────────────────────────────

def _make_decision_trace(
    kind: str,
    level: int,
    condition: str,
    condition_value: Optional[bool],
    taken_branch: Optional[str],
    iterations: Optional[int],
    events: List[dict],
) -> dict:
    """Cria o contrato único DecisionTrace para níveis 4–7."""
    # nível 4: 1 evento; níveis 5+: histórico completo
    eventos_saida = events[:1] if level == 4 else list(events)
    graph = None
    if level >= 6:
        graph = _make_graph(kind, events, level)
    return {
        "kind": kind,
        "level": level,
        "condition": condition,
        "condition_value": condition_value,
        "taken_branch": taken_branch,
        "iterations": iterations,
        "events": eventos_saida,
        "graph": graph,
    }


# Keys that are metadata (not variable snapshots) in loop iteration events
_GRAPH_EVENT_META_KEYS = frozenset(("event", "iteration", "condition_value", "env_snapshot"))


def _make_graph(kind: str, events: List[dict], level: int) -> dict:
    """Cria representação em grafo do fluxo de controle."""
    nodes: List[dict] = []
    edges: List[dict] = []

    if kind == "if":
        nodes.append({"id": "condition", "type": "condition"})
        nodes.append({"id": "then", "type": "branch", "label": "then"})
        nodes.append({"id": "else", "type": "branch", "label": "else"})
        edges.append({"from": "condition", "to": "then", "label": "true"})
        edges.append({"from": "condition", "to": "else", "label": "false"})
    else:  # while / for
        nodes.append({"id": "start", "type": "start"})
        nodes.append({"id": "condition", "type": "condition"})
        nodes.append({"id": "end", "type": "end"})
        edges.append({"from": "start", "to": "condition"})
        edges.append({"from": "condition", "to": "end", "label": "exit"})

        for i, event in enumerate(events):
            node_id = f"iter_{i}"
            node: dict = {"id": node_id, "type": "iteration", "iteration": i}
            if level >= 7:
                # Level 7: include variable snapshot in graph node
                node["env_snapshot"] = {k: v for k, v in event.items()
                                         if k not in _GRAPH_EVENT_META_KEYS}
            nodes.append(node)
            if i == 0:
                edges.append({"from": "condition", "to": node_id, "label": "loop"})
            else:
                edges.append({"from": f"iter_{i - 1}", "to": node_id})
            edges.append({"from": node_id, "to": "condition"})

    return {"nodes": nodes, "edges": edges}


class GuruDVM:
    def __init__(self, gurumatrix: GuruMatrix):
        self.matrix = gurumatrix
        self.pilha: List[Any] = []
        self.contexto: Dict[str, Any] = {
            "clave": "geral", "hermeneutics": 1, "ontologia": "SUBSTANCIA"
        }
        self.saida: List[dict] = []   # log de outputs para os testes inspecionarem
        self.recursos: Dict[str, Any] = {}   # banco de recursos carregados
        self.env: Dict[str, Any] = {}   # variáveis do programa em execução

    # ── API pública ─────────────────────────────────────────────────────────

    def carregar_recurso(self, nome: str, valor: Any):
        """Registra um recurso disponível para LOAD."""
        self.recursos[nome] = valor

    def executar(self, gurubyte: dict) -> List[dict]:
        """Executa um arquivo GuruByte completo."""
        self.saida = []
        self.env = {}
        ctx_default = gurubyte.get("CONTEXT_DEFAULT", {})
        self.contexto.update(ctx_default)

        for bloco in gurubyte.get("CODEBLOCKS", []):
            self._executar_bloco(bloco)

        return self.saida

    # ── Execução de blocos ──────────────────────────────────────────────────

    def _executar_bloco(self, bloco: dict, parent_ctx: Optional[Dict[str, Any]] = None):
        base = parent_ctx if parent_ctx is not None else self.contexto
        ctx_bloco: Dict[str, Any] = {**base, **bloco.get("CONTEXT", {})}
        # When a parent context is supplied (runtime override), its hermeneutics level
        # propagates to all descendant blocks so the entire subtree runs at the same level.
        if parent_ctx is not None:
            ctx_bloco["hermeneutics"] = parent_ctx.get("hermeneutics",
                                                        ctx_bloco.get("hermeneutics", 1))
        tipo = bloco.get("type", "INSTRUCOES")

        if tipo == "DISPATCH_ON_HERMENEUTICS":
            self._dispatch_hermeneutica(bloco, ctx_bloco)
        elif tipo == "FUNCTION":
            for sub in bloco.get("corpo", []):
                self._executar_bloco(sub, ctx_bloco)
        elif tipo == "IF":
            self._executar_if(bloco, ctx_bloco)
        elif tipo == "WHILE":
            self._executar_while(bloco, ctx_bloco)
        elif tipo == "FOR":
            self._executar_for(bloco, ctx_bloco)
        elif tipo == "ASSIGN":
            self._executar_assign(bloco)
        else:
            for instr in bloco.get("instructions", []):
                self._executar_instrucao(instr, ctx_bloco)

    def _dispatch_hermeneutica(self, bloco: dict, ctx: dict):
        """
        *** NÚCLEO DO MVP ***
        Seleciona e executa o corpo correspondente ao nível hermenêutico ativo.
        Demonstra que a mesma instrução produce outputs computacionalmente distintos.
        """
        nivel = ctx.get("hermeneutics", 1)
        recurso = bloco.get("recurso", "")
        casos = bloco.get("casos", {})

        # Busca o case mais específico; fallback para default
        corpo = casos.get(str(nivel)) or casos.get(nivel)
        if corpo is None:
            corpo = bloco.get("default")

        if corpo is None:
            self._registrar_saida("DISPATCH_ON_HERMENEUTICS", nivel, recurso,
                                  {"aviso": f"Nenhum case para hermeneutica={nivel}"})
            return

        ctx_dispatch = {**ctx, "hermeneutics": nivel}
        for instr in corpo:
            self._executar_instrucao(instr, ctx_dispatch)

    # ── Controle de fluxo ───────────────────────────────────────────────────

    def _executar_assign(self, bloco: dict):
        """Executa uma atribuição de variável: var = expr."""
        var_name = bloco.get("var", "")
        expr = bloco.get("expr", {})
        value = self._eval_expr(expr)
        self.env[var_name] = value

    def _executar_if(self, bloco: dict, ctx: dict):
        """Executa if/else. Emite DecisionTrace para níveis 4–7."""
        condition = bloco.get("condition", {})
        condition_repr = self._repr_expr(condition)
        condition_val = bool(self._eval_expr(condition))
        herm = ctx.get("hermeneutics", 1)
        taken = "then" if condition_val else "else"

        events: List[dict] = [{"event": "branch", "condition_value": condition_val, "taken": taken}]

        if condition_val:
            for sub in bloco.get("then", []):
                self._executar_bloco(sub, ctx)
        else:
            for sub in bloco.get("else", []):
                self._executar_bloco(sub, ctx)

        if herm >= 4:
            trace = _make_decision_trace("if", herm, condition_repr, condition_val,
                                         taken, None, events)
            self._registrar_saida("DECISION_TRACE", herm, "if", trace)

    def _executar_while(self, bloco: dict, ctx: dict):
        """Executa while. Emite DecisionTrace para níveis 4–7."""
        condition = bloco.get("condition", {})
        condition_repr = self._repr_expr(condition)
        herm = ctx.get("hermeneutics", 1)

        iterations = 0
        events: List[dict] = []

        while True:
            cond_val = bool(self._eval_expr(condition))
            if not cond_val:
                break
            event: Dict[str, Any] = {
                "event": "iteration",
                "iteration": iterations,
                "condition_value": cond_val,
            }
            if herm >= 7:
                event["env_snapshot"] = dict(self.env)
            events.append(event)
            for sub in bloco.get("body", []):
                self._executar_bloco(sub, ctx)
            iterations += 1

        if herm >= 4:
            trace = _make_decision_trace("while", herm, condition_repr, None,
                                         None, iterations, events)
            self._registrar_saida("DECISION_TRACE", herm, "while", trace)

    def _executar_for(self, bloco: dict, ctx: dict):
        """Executa for..in. Emite DecisionTrace para níveis 4–7."""
        var_name = bloco.get("var", "i")
        iterable_expr = bloco.get("iterable", {})
        iterable = self._eval_expr(iterable_expr)
        herm = ctx.get("hermeneutics", 1)

        iterations = 0
        events: List[dict] = []

        for val in (iterable if iterable is not None else []):
            self.env[var_name] = val
            event: Dict[str, Any] = {
                "event": "iteration",
                "iteration": iterations,
                var_name: val,
                "condition_value": True,
            }
            if herm >= 7:
                event["env_snapshot"] = dict(self.env)
            events.append(event)
            for sub in bloco.get("body", []):
                self._executar_bloco(sub, ctx)
            iterations += 1

        if herm >= 4:
            trace = _make_decision_trace("for", herm, self._repr_expr(iterable_expr),
                                         None, None, iterations, events)
            self._registrar_saida("DECISION_TRACE", herm, "for", trace)

    # ── Avaliador de expressões ─────────────────────────────────────────────

    def _eval_expr(self, expr: dict) -> Any:
        """Avalia uma expressão serializada (dict) usando self.env."""
        kind = expr.get("kind", "")
        if kind == "literal":
            return expr.get("value")
        elif kind == "var":
            return self.env.get(expr.get("name", ""), 0)
        elif kind == "binop":
            left = self._eval_expr(expr.get("left", {}))
            right = self._eval_expr(expr.get("right", {}))
            return self._apply_op(expr.get("op", ""), left, right)
        elif kind == "call":
            func = expr.get("func", "")
            args = [self._eval_expr(a) for a in expr.get("args", [])]
            return self._call_builtin(func, args)
        return None

    def _apply_op(self, op: str, left: Any, right: Any) -> Any:
        if op == "+":  return left + right
        if op == "-":  return left - right
        if op == "*":  return left * right
        if op == "/":  return (left / right) if right else 0
        if op == ">":  return left > right
        if op == "<":  return left < right
        if op == ">=": return left >= right
        if op == "<=": return left <= right
        if op == "==": return left == right
        if op == "!=": return left != right
        return None

    def _call_builtin(self, func: str, args: List[Any]) -> Any:
        if func == "range":
            return range(*[int(a) for a in args])
        return None

    def _repr_expr(self, expr: dict) -> str:
        kind = expr.get("kind", "")
        if kind == "literal":    return repr(expr.get("value"))
        if kind == "var":        return expr.get("name", "?")
        if kind == "binop":
            return (f"{self._repr_expr(expr.get('left', {}))} "
                    f"{expr.get('op')} "
                    f"{self._repr_expr(expr.get('right', {}))}")
        if kind == "call":
            args = ", ".join(self._repr_expr(a) for a in expr.get("args", []))
            return f"{expr.get('func')}({args})"
        return "?"

    # ── Execução de instruções individuais ─────────────────────────────────

    def _executar_instrucao(self, instr: dict, ctx: dict):
        opcode = instr.get("opcode", "")
        operandos = instr.get("operandos", [])
        mods = instr.get("modificadores", {})
        herm = ctx.get("hermeneutics", instr.get("contexto_hermeneutica", 1))
        clave = ctx.get("clave", instr.get("contexto_clave", "geral"))

        if opcode == "LOAD":
            self._op_load(operandos, ctx)
        elif opcode == "DISPLAY":
            self._op_display(operandos, mods, herm, clave, ctx)
        elif opcode == "EVALUATE":
            self._op_evaluate(operandos, mods, herm, clave, ctx)
        elif opcode == "TRANSCODE":
            self._op_transcode(operandos, ctx)
        elif opcode == "BIND":
            ctx["clave"] = instr.get("clave", clave)
        elif opcode == "TAG":
            ctx["hermeneutics"] = instr.get("hermeneutica", herm)
        elif opcode == "MAP_TO":
            self._op_map_to(operandos, ctx)
        elif opcode == "DISPATCH_ON_HERMENEUTICS":
            # dispatch aninhado
            self._dispatch_hermeneutica(instr, ctx)
        else:
            self._registrar_saida(opcode, herm, str(operandos), {"status": "NÃO_IMPLEMENTADO"})

    # ── Implementações das instruções ───────────────────────────────────────

    def _op_load(self, operandos: List, ctx: dict):
        nome = operandos[0] if operandos else "?"
        valor = self.recursos.get(nome, f"<recurso:{nome}>")
        self.pilha.append({"nome": nome, "valor": valor})
        self._registrar_saida("LOAD", ctx.get("hermeneutics", 1), nome,
                              {"carregado": True, "valor_preview": str(valor)[:60]})

    def _op_display(self, operandos: List, mods: dict, herm: int, clave: str, ctx: dict):
        """
        DISPLAY: pode exibir literal, variável do env, ou recurso da pilha.
        DISPLAY IN CONTEXT: comportamento varia com nível hermenêutico (MVP).
        """
        if not mods.get("in_context") and operandos:
            # Operand direto: variável do env ou literal de string
            raw = operandos[0]
            if raw in self.env:
                valor: Any = self.env[raw]
                nome_recurso = raw
            else:
                valor = raw
                nome_recurso = raw
        else:
            recurso = self.pilha[-1] if self.pilha else {"nome": "?", "valor": None}
            nome_recurso = recurso.get("nome", "?")
            valor = recurso.get("valor")

        resultado = self._render_por_hermeneutica(nome_recurso, valor, herm, clave)
        self._registrar_saida("DISPLAY", herm, nome_recurso, resultado)

    def _render_por_hermeneutica(self, nome: str, valor: Any, herm: int, clave: str) -> dict:
        """
        Comportamento computacionalmente distinto por nível hermenêutico.
        Este método é a demonstração central do MVP.
        """
        if herm == 1:
            # Literal: representação bruta
            return {
                "nivel": 1,
                "modo": "LITERAL",
                "output": str(valor),
                "descricao": "Representação literal do recurso sem interpretação.",
            }
        elif herm == 2:
            # Alegórico: representação com tipo e estrutura
            return {
                "nivel": 2,
                "modo": "ALEGÓRICO",
                "output": {"tipo": type(valor).__name__, "valor": str(valor)},
                "descricao": "Representação tipada com estrutura explícita.",
            }
        elif herm == 3:
            # Técnico: análise computacional
            analise = self._analisar_tecnicamente(valor)
            return {
                "nivel": 3,
                "modo": "TÉCNICO",
                "output": analise,
                "descricao": "Análise técnica do recurso.",
            }
        elif herm == 4:
            # Contextual: posição na GuruMatrix
            coord = self._inferir_coordenada(nome, clave)
            return {
                "nivel": 4,
                "modo": "CONTEXTUAL",
                "output": {"valor": str(valor), "coordenada_gurumatrix": str(coord)},
                "descricao": "Recurso contextualizado na GuruMatrix.",
            }
        elif herm == 5:
            # Comparativo: relações semânticas disponíveis
            coord = self._inferir_coordenada(nome, clave)
            relacoes = self._buscar_relacoes(coord)
            return {
                "nivel": 5,
                "modo": "COMPARATIVO",
                "output": {"valor": str(valor), "relacoes_semanticas": relacoes},
                "descricao": "Recurso com mapa de relações semânticas.",
            }
        elif herm == 6:
            # Analógico: conexões entre domínios
            analogias = self._encontrar_analogias(nome, clave)
            return {
                "nivel": 6,
                "modo": "ANALÓGICO",
                "output": {"valor": str(valor), "analogias_interdominio": analogias},
                "descricao": "Recurso com conexões analógicas entre domínios.",
            }
        elif herm == 7:
            # Ontológico: expansão completa na GuruMatrix
            expansao = self._expandir_ontologicamente(nome, clave)
            return {
                "nivel": 7,
                "modo": "ONTOLÓGICO",
                "output": expansao,
                "descricao": "Expansão ontológica completa: todas as relações na GuruMatrix.",
            }
        else:
            return {"nivel": herm, "modo": "DESCONHECIDO", "output": str(valor)}

    def _analisar_tecnicamente(self, valor: Any) -> dict:
        analise = {"repr": str(valor), "tipo_python": type(valor).__name__}
        if isinstance(valor, str):
            analise["comprimento"] = len(valor)
            analise["palavras"] = len(valor.split())
        elif isinstance(valor, (int, float)):
            analise["magnitude"] = abs(valor)
            analise["positivo"] = valor > 0
        elif isinstance(valor, (list, tuple)):
            analise["tamanho"] = len(valor)
        return analise

    def _inferir_coordenada(self, nome: str, clave: str) -> tuple:
        mapa = {
            "ciencia":   (Ontologia.ACAO, Dominio.CIENCIA),
            "arte":      (Ontologia.QUALIDADE, Dominio.ARTE),
            "filosofia": (Ontologia.RELACAO, Dominio.FILOSOFIA),
            "matematica":(Ontologia.RELACAO, Dominio.MATEMATICA),
            "tecnologia":(Ontologia.SUBSTANCIA, Dominio.TECNOLOGIA),
        }
        return mapa.get(clave.lower(), (Ontologia.SUBSTANCIA, Dominio.TECNOLOGIA))

    def _buscar_relacoes(self, coord: tuple) -> List[str]:
        try:
            celula = self.matrix.get(coord[0], coord[1])
            return [r.value for r in celula.relacoes_ativas]
        except (KeyError, AttributeError, TypeError):
            return []

    def _encontrar_analogias(self, nome: str, clave: str) -> List[dict]:
        """Busca objetos semelhantes em outros domínios via relação de Homologia."""
        coord = self._inferir_coordenada(nome, clave)
        analogias = []
        for dominio in Dominio:
            try:
                celula = self.matrix.get(coord[0], dominio)
                if celula.objetos and dominio.name.lower() != clave.lower():
                    analogias.append({
                        "dominio": dominio.name,
                        "objetos_analogos": celula.objetos[:3],
                        "relacao": "HOMOLOGIA",
                    })
            except (KeyError, AttributeError, TypeError):
                pass
        return analogias[:4]  # limita para legibilidade

    def _expandir_ontologicamente(self, nome: str, clave: str) -> dict:
        """Expansão ontológica completa: mapeia o objeto em toda a GuruMatrix."""
        coord = self._inferir_coordenada(nome, clave)
        celula_origem = self.matrix.get(coord[0], coord[1])
        expansao = {
            "celula_origem": f"{coord[0].name}_{coord[1].name}",
            "objetos_na_celula": celula_origem.objetos,
            "relacoes_ativas": [r.value for r in celula_origem.relacoes_ativas],
            "instrucoes_preferenciais": celula_origem.instrucoes_preferenciais,
            "conexoes_ontologicas": {},
        }
        # Adiciona conexões com todas as categorias ontológicas no mesmo domínio
        for ont in Ontologia:
            celula = self.matrix.get(ont, coord[1])
            if celula.objetos:
                expansao["conexoes_ontologicas"][ont.name] = celula.objetos
        return expansao

    def _op_evaluate(self, operandos: List, mods: dict, herm: int, clave: str, ctx: dict):
        recurso = self.pilha[-1] if self.pilha else {"nome": "?", "valor": None}
        nome = recurso.get("nome", "?")
        valor = recurso.get("valor")
        modo = mods.get("modo", "symbolic")

        if herm <= 2 or modo == "numeric":
            resultado = {"modo": "numeric", "output": str(valor),
                         "nota": "Avaliação literal/numérica."}
        elif herm <= 4 or modo == "symbolic":
            resultado = {"modo": "symbolic", "output": f"repr({valor})",
                         "nota": "Avaliação simbólica — estrutura sem cômputo numérico."}
        else:  # herm >= 5 ou modo == "ontological"
            expansao = self._expandir_ontologicamente(nome, clave)
            resultado = {"modo": "ontological", "output": expansao,
                         "nota": "Avaliação ontológica — expansão completa na GuruMatrix."}

        self._registrar_saida("EVALUATE", herm, nome, resultado)
        self.pilha.append({"nome": f"eval({nome})", "valor": resultado})

    def _op_transcode(self, operandos: List, ctx: dict):
        # operandos: [recurso, 'to', destino]
        if len(operandos) >= 3:
            origem = operandos[0]; destino = operandos[2]
        else:
            origem = str(operandos); destino = "DESCONHECIDO"
        resultado = {
            "origem": origem, "destino": destino,
            "output": f"TRANSCODE({origem} → {destino}): [representação convertida]",
        }
        self._registrar_saida("TRANSCODE", ctx.get("hermeneutics", 1), origem, resultado)

    def _op_map_to(self, operandos: List, ctx: dict):
        clave = " ".join(operandos).replace("CLAVE", "").strip().lower()
        ctx["clave"] = clave
        self._registrar_saida("MAP_TO", ctx.get("hermeneutics", 1), clave,
                              {"nova_clave": clave})

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _registrar_saida(self, opcode: str, herm: int, alvo: str, dados: dict):
        self.saida.append({
            "opcode": opcode,
            "hermeneutica": herm,
            "alvo": alvo,
            "dados": dados,
        })

    def _verificar_mvp(self) -> bool:
        """
        Verifica se a execução atual produziu outputs computacionalmente distintos.
        Critério: pelo menos 2 modos hermenêuticos diferentes registrados em operações DISPLAY.
        """
        modos = {o["dados"].get("modo") for o in self.saida
                 if o["opcode"] == "DISPLAY" and "modo" in o["dados"]}
        return len(modos) >= 2



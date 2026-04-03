"""
GuruDVM v0.1-MVP
Runtime bicameral: executa plano sintático e plano semântico simultaneamente.
Núcleo do MVP: DISPATCH_ON_HERMENEUTICS produz outputs computacionalmente distintos.
"""
from typing import Any, Dict, List

from gurumatrix.core import Dominio, GuruMatrix, Ontologia


class GuruDVM:
    def __init__(self, gurumatrix: GuruMatrix):
        self.matrix = gurumatrix
        self.pilha: List[Any] = []
        self.contexto: Dict[str, Any] = {
            "clave": "geral", "hermeneutics": 1, "ontologia": "SUBSTANCIA"
        }
        self.saida: List[dict] = []   # log de outputs para os testes inspecionarem
        self.recursos: Dict[str, Any] = {}   # banco de recursos carregados

    # ── API pública ─────────────────────────────────────────────────────────

    def carregar_recurso(self, nome: str, valor: Any):
        """Registra um recurso disponível para LOAD."""
        self.recursos[nome] = valor

    def executar(self, gurubyte: dict) -> List[dict]:
        """Executa um arquivo GuruByte completo."""
        self.saida = []
        ctx_default = gurubyte.get("CONTEXT_DEFAULT", {})
        self.contexto.update(ctx_default)

        for bloco in gurubyte.get("CODEBLOCKS", []):
            self._executar_bloco(bloco)

        return self.saida

    # ── Execução de blocos ──────────────────────────────────────────────────

    def _executar_bloco(self, bloco: dict):
        ctx_bloco = {**self.contexto, **bloco.get("CONTEXT", {})}
        tipo = bloco.get("type", "INSTRUCOES")

        if tipo == "DISPATCH_ON_HERMENEUTICS":
            self._dispatch_hermeneutica(bloco, ctx_bloco)
        elif tipo == "FUNCTION":
            for sub in bloco.get("corpo", []):
                self._executar_bloco(sub)
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
        DISPLAY IN CONTEXT: comportamento varia com nível hermenêutico.
        Este é o caso demonstrável do MVP.
        """
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
            "ciencia": (Ontologia.ACAO, Dominio.CIENCIA),
            "arte": (Ontologia.QUALIDADE, Dominio.ARTE),
            "filosofia": (Ontologia.RELACAO, Dominio.FILOSOFIA),
            "matematica": (Ontologia.RELACAO, Dominio.MATEMATICA),
            "tecnologia": (Ontologia.SUBSTANCIA, Dominio.TECNOLOGIA),
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

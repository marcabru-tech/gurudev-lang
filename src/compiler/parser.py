"""GuruDev Parser v0.1-MVP — tokens → GuruAST"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from compiler.lexer import Token, TokenType

# ── AST nodes ──────────────────────────────────────────────────────────────

@dataclass
class NoAST:
    tipo: str = "NÓ"
    filhos: List['NoAST'] = field(default_factory=list)
    clave: Optional[str] = None
    hermeneutica: Optional[int] = None
    ontologia: Optional[str] = None
    coordenada_gurumatrix: Optional[tuple] = None
    relacoes_semanticas: List[str] = field(default_factory=list)
    linha: int = 0

@dataclass
class Programa(NoAST):
    declaracoes: List[NoAST] = field(default_factory=list)
    def __post_init__(self): self.tipo = "PROGRAMA"

@dataclass
class TagHermeneutica(NoAST):
    nivel: int = 1
    def __post_init__(self): self.tipo = "TAG_HERMENEUTICA"; self.hermeneutica = self.nivel

@dataclass
class BindClave(NoAST):
    campo: str = ""
    def __post_init__(self): self.tipo = "BIND_CLAVE"; self.clave = self.campo

@dataclass
class Instrucao(NoAST):
    opcode: str = ""
    operandos: List[Any] = field(default_factory=list)
    modificadores: Dict[str, Any] = field(default_factory=dict)
    def __post_init__(self): self.tipo = "INSTRUCAO"

@dataclass
class DispatchHermeneutica(NoAST):
    recurso: str = ""
    casos: Dict[int, 'CorpoDispatch'] = field(default_factory=dict)
    padrao: Optional[List[NoAST]] = None
    def __post_init__(self): self.tipo = "DISPATCH_HERMENEUTICA"

@dataclass
class CorpoDispatch:
    instrucoes: List[NoAST] = field(default_factory=list)

@dataclass
class FuncaoDecl(NoAST):
    nome: str = ""
    parametros: List[str] = field(default_factory=list)
    corpo: List[NoAST] = field(default_factory=list)
    def __post_init__(self): self.tipo = "FUNCAO"

@dataclass
class Literal(NoAST):
    valor: Any = None
    def __post_init__(self): self.tipo = "LITERAL"

@dataclass
class Identificador(NoAST):
    nome: str = ""
    def __post_init__(self): self.tipo = "IDENTIFICADOR"

# ── Parser ─────────────────────────────────────────────────────────────────

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def erro(self, msg: str):
        t = self.atual()
        raise SyntaxError(f"Linha {t.linha}: {msg} (encontrado '{t.valor}')")

    def atual(self) -> Token:
        return self.tokens[min(self.pos, len(self.tokens)-1)]

    def avancar(self) -> Token:
        t = self.atual(); self.pos += 1; return t

    def consumir(self, tipo: TokenType) -> Token:
        if self.atual().tipo != tipo:
            self.erro(f"Esperado {tipo.name}")
        return self.avancar()

    def pular_newlines(self):
        while self.atual().tipo == TokenType.NEWLINE:
            self.avancar()

    def parse(self) -> Programa:
        prog = Programa(declaracoes=[])
        while self.atual().tipo != TokenType.EOF:
            self.pular_newlines()
            if self.atual().tipo == TokenType.EOF:
                break
            no = self.parse_declaracao()
            if no:
                prog.declaracoes.append(no)
            self.pular_newlines()
        return prog

    def parse_declaracao(self) -> Optional[NoAST]:
        t = self.atual()
        if   t.tipo == TokenType.DEF:        return self.parse_funcao()
        elif t.tipo == TokenType.TAG:        return self.parse_tag()
        elif t.tipo == TokenType.BIND:       return self.parse_bind()
        elif t.tipo == TokenType.LOAD:       return self.parse_instrucao_simples("LOAD")
        elif t.tipo == TokenType.DISPLAY:    return self.parse_display()
        elif t.tipo == TokenType.EVALUATE:   return self.parse_evaluate()
        elif t.tipo == TokenType.DISPATCH:   return self.parse_dispatch()
        elif t.tipo == TokenType.TRANSCODE:  return self.parse_transcode()
        elif t.tipo == TokenType.EMOTE:      return self.parse_instrucao_simples("EMOTE")
        elif t.tipo == TokenType.IDENTIFIER: return self.parse_identificador()
        else:
            self.erro(f"Declaração inesperada")

    # ── Instruções simples ──────────────────────────────────────────────────

    def parse_instrucao_simples(self, opcode: str) -> Instrucao:
        linha = self.atual().linha
        self.avancar()  # consome a palavra-chave
        operandos = []
        # lê operandos até nova linha ou EOF
        while self.atual().tipo not in (TokenType.NEWLINE, TokenType.EOF,
                                        TokenType.RBRACE, TokenType.SEMICOLON):
            operandos.append(self.atual().valor)
            self.avancar()
        instr = Instrucao(opcode=opcode, operandos=operandos, linha=linha)
        return instr

    def parse_tag(self) -> TagHermeneutica:
        linha = self.atual().linha
        self.consumir(TokenType.TAG)
        self.consumir(TokenType.HERMENEUTICA)
        self.consumir(TokenType.ASSIGN)
        nivel = int(self.consumir(TokenType.NUMBER).valor)
        if not 1 <= nivel <= 7:
            raise ValueError(f"Hermeneutica deve ser 1-7, recebido {nivel}")
        return TagHermeneutica(nivel=nivel, linha=linha)

    def parse_bind(self) -> BindClave:
        linha = self.atual().linha
        self.consumir(TokenType.BIND)
        self.consumir(TokenType.CLAVE)
        self.consumir(TokenType.ASSIGN)
        campo = self.consumir(TokenType.IDENTIFIER).valor
        return BindClave(campo=campo, linha=linha)

    def parse_display(self) -> Instrucao:
        linha = self.atual().linha
        self.consumir(TokenType.DISPLAY)
        mods = {}
        operandos = []
        # display [recurso] [in context]
        while self.atual().tipo not in (TokenType.NEWLINE, TokenType.EOF,
                                        TokenType.RBRACE, TokenType.SEMICOLON):
            if self.atual().tipo == TokenType.IN:
                self.avancar()
                if self.atual().tipo == TokenType.CONTEXT:
                    mods['in_context'] = True
                    self.avancar()
            else:
                operandos.append(self.atual().valor)
                self.avancar()
        return Instrucao(opcode="DISPLAY", operandos=operandos, modificadores=mods, linha=linha)

    def parse_evaluate(self) -> Instrucao:
        """evaluate <recurso> [numeric|symbolic|ontological]"""
        linha = self.atual().linha
        self.consumir(TokenType.EVALUATE)
        operandos = []
        mods = {}
        while self.atual().tipo not in (TokenType.NEWLINE, TokenType.EOF,
                                        TokenType.RBRACE, TokenType.SEMICOLON):
            val = self.atual().valor.lower()
            if val in ('numeric', 'symbolic', 'ontological'):
                mods['modo'] = val
            else:
                operandos.append(self.atual().valor)
            self.avancar()
        return Instrucao(opcode="EVALUATE", operandos=operandos, modificadores=mods, linha=linha)

    def parse_transcode(self) -> Instrucao:
        """transcode <recurso> to <destino>"""
        linha = self.atual().linha
        self.consumir(TokenType.TRANSCODE)
        operandos = []
        while self.atual().tipo not in (TokenType.NEWLINE, TokenType.EOF,
                                        TokenType.RBRACE, TokenType.SEMICOLON):
            operandos.append(self.atual().valor)
            self.avancar()
        return Instrucao(opcode="TRANSCODE", operandos=operandos, linha=linha)

    def parse_identificador(self) -> Identificador:
        nome = self.avancar().valor
        return Identificador(nome=nome)

    def parse_tipo(self):
        """Consome anotação de tipo (ignorada no MVP)"""
        while self.atual().tipo not in (TokenType.LBRACE, TokenType.NEWLINE, TokenType.EOF):
            self.avancar()

    # ── dispatch on hermeneutica ────────────────────────────────────────────

    def parse_dispatch(self) -> DispatchHermeneutica:
        """
        dispatch hermeneutica recurso {
            case 1: instrucao
            case 7: instrucao
            default: instrucao
        }
        """
        linha = self.atual().linha
        self.consumir(TokenType.DISPATCH)
        self.consumir(TokenType.HERMENEUTICA)
        recurso = self.consumir(TokenType.IDENTIFIER).valor
        self.consumir(TokenType.LBRACE)
        self.pular_newlines()

        node = DispatchHermeneutica(recurso=recurso, linha=linha)

        while self.atual().tipo != TokenType.RBRACE:
            self.pular_newlines()
            if self.atual().tipo == TokenType.RBRACE:
                break

            if self.atual().tipo == TokenType.CASE:
                self.avancar()
                nivel = int(self.consumir(TokenType.NUMBER).valor)
                self.consumir(TokenType.COLON)
                instrucoes = self._parse_corpo_case()
                node.casos[nivel] = CorpoDispatch(instrucoes=instrucoes)

            elif self.atual().tipo == TokenType.DEFAULT:
                self.avancar()
                self.consumir(TokenType.COLON)
                node.padrao = CorpoDispatch(instrucoes=self._parse_corpo_case()).instrucoes

            else:
                self.erro("Esperado 'case N:' ou 'default:' dentro de dispatch")

            self.pular_newlines()

        self.consumir(TokenType.RBRACE)
        return node

    def _parse_corpo_case(self) -> List[NoAST]:
        """Lê instrução(ões) de um case — pode ser linha única ou bloco {}"""
        self.pular_newlines()
        instrucoes = []
        if self.atual().tipo == TokenType.LBRACE:
            self.avancar(); self.pular_newlines()
            while self.atual().tipo != TokenType.RBRACE:
                no = self.parse_declaracao()
                if no: instrucoes.append(no)
                self.pular_newlines()
            self.consumir(TokenType.RBRACE)
        else:
            no = self.parse_declaracao()
            if no: instrucoes.append(no)
        return instrucoes

    # ── função ──────────────────────────────────────────────────────────────

    def parse_funcao(self) -> FuncaoDecl:
        linha = self.atual().linha
        self.consumir(TokenType.DEF)
        nome = self.consumir(TokenType.IDENTIFIER).valor
        self.consumir(TokenType.LPAREN)
        params = []
        if self.atual().tipo != TokenType.RPAREN:
            params.append(self.consumir(TokenType.IDENTIFIER).valor)
            while self.atual().tipo == TokenType.COMMA:
                self.avancar()
                params.append(self.consumir(TokenType.IDENTIFIER).valor)
        self.consumir(TokenType.RPAREN)
        if self.atual().tipo == TokenType.ARROW:
            self.avancar(); self.parse_tipo()
        self.consumir(TokenType.LBRACE)
        self.pular_newlines()
        corpo = []
        while self.atual().tipo != TokenType.RBRACE:
            no = self.parse_declaracao()
            if no: corpo.append(no)
            self.pular_newlines()
        self.consumir(TokenType.RBRACE)
        return FuncaoDecl(nome=nome, parametros=params, corpo=corpo, linha=linha)

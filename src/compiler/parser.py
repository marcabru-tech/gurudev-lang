"""GuruDev Parser v0.2 — tokens → GuruAST com controle de fluxo"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, NoReturn, Optional

from compiler.lexer import Token, TokenType
from gurudev.exceptions import HermeneuticsError, ParserError

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

# ── Novos nós para controle de fluxo ─────────────────────────────────────

@dataclass
class BinaryOpNode(NoAST):
    op: str = ""
    left: Optional[NoAST] = None
    right: Optional[NoAST] = None
    def __post_init__(self): self.tipo = "BINOP"

@dataclass
class CallNode(NoAST):
    func: str = ""
    args: List[NoAST] = field(default_factory=list)
    def __post_init__(self): self.tipo = "CALL"

@dataclass
class BlockNode(NoAST):
    statements: List[NoAST] = field(default_factory=list)
    def __post_init__(self): self.tipo = "BLOCK"

@dataclass
class AssignNode(NoAST):
    name: str = ""
    value: Optional[NoAST] = None
    def __post_init__(self): self.tipo = "ASSIGN"

@dataclass
class IfNode(NoAST):
    condition: Optional[NoAST] = None
    then_block: Optional[BlockNode] = None
    else_block: Optional[BlockNode] = None
    def __post_init__(self): self.tipo = "IF"

@dataclass
class WhileNode(NoAST):
    condition: Optional[NoAST] = None
    body_block: Optional[BlockNode] = None
    def __post_init__(self): self.tipo = "WHILE"

@dataclass
class ForNode(NoAST):
    var_name: str = ""
    iterable_expr: Optional[NoAST] = None
    body_block: Optional[BlockNode] = None
    def __post_init__(self): self.tipo = "FOR"

# ── Parser ─────────────────────────────────────────────────────────────────

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def erro(self, msg: str) -> NoReturn:
        t = self.atual()
        raise ParserError(expected=msg, found=t.valor, line=t.linha)

    def atual(self) -> Token:
        return self.tokens[min(self.pos, len(self.tokens)-1)]

    def proximo(self) -> Token:
        pos2 = min(self.pos + 1, len(self.tokens) - 1)
        return self.tokens[pos2]

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
        elif t.tipo == TokenType.IF:         return self.parse_if()
        elif t.tipo == TokenType.WHILE:      return self.parse_while()
        elif t.tipo == TokenType.FOR:        return self.parse_for()
        elif t.tipo == TokenType.IDENTIFIER:
            # Look ahead: IDENTIFIER ASSIGN → assignment statement
            if self.proximo().tipo == TokenType.ASSIGN:
                return self.parse_assign()
            return self.parse_identificador()
        else:
            self.erro("Declaração inesperada")

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
            raise HermeneuticsError(nivel)
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

    # ── Controle de fluxo ──────────────────────────────────────────────────

    def parse_assign(self) -> AssignNode:
        """identifier = expression"""
        linha = self.atual().linha
        name = self.consumir(TokenType.IDENTIFIER).valor
        self.consumir(TokenType.ASSIGN)
        value = self.parse_expression()
        return AssignNode(name=name, value=value, linha=linha)

    def parse_if(self) -> IfNode:
        """if <condition> { <then> } [else { <else> }]"""
        linha = self.atual().linha
        self.consumir(TokenType.IF)
        condition = self.parse_expression()
        then_block = self.parse_block()
        else_block = None
        self.pular_newlines()
        if self.atual().tipo == TokenType.ELSE:
            self.avancar()
            self.pular_newlines()
            if self.atual().tipo == TokenType.IF:
                # else if chaining
                else_if = self.parse_if()
                else_block = BlockNode(statements=[else_if])
            else:
                else_block = self.parse_block()
        return IfNode(condition=condition, then_block=then_block, else_block=else_block, linha=linha)

    def parse_while(self) -> WhileNode:
        """while <condition> { <body> }"""
        linha = self.atual().linha
        self.consumir(TokenType.WHILE)
        condition = self.parse_expression()
        body_block = self.parse_block()
        return WhileNode(condition=condition, body_block=body_block, linha=linha)

    def parse_for(self) -> ForNode:
        """for <var> in <iterable_expr> { <body> }"""
        linha = self.atual().linha
        self.consumir(TokenType.FOR)
        var_name = self.consumir(TokenType.IDENTIFIER).valor
        self.consumir(TokenType.IN)
        iterable_expr = self.parse_expression()
        body_block = self.parse_block()
        return ForNode(var_name=var_name, iterable_expr=iterable_expr, body_block=body_block, linha=linha)

    def parse_block(self) -> BlockNode:
        """{ <statements...> }"""
        self.pular_newlines()
        self.consumir(TokenType.LBRACE)
        stmts = []
        self.pular_newlines()
        while self.atual().tipo not in (TokenType.RBRACE, TokenType.EOF):
            no = self.parse_declaracao()
            if no:
                stmts.append(no)
            self.pular_newlines()
        self.consumir(TokenType.RBRACE)
        return BlockNode(statements=stmts)

    # ── Expressões (com precedência) ────────────────────────────────────────

    def parse_expression(self) -> NoAST:
        """Ponto de entrada para análise de expressões (comparação ou aritmética)."""
        return self.parse_comparison()

    def parse_comparison(self) -> NoAST:
        """comparison: additive (('>' | '<' | '>=' | '<=' | '==' | '!=') additive)?"""
        node = self.parse_additive()
        _cmp_ops = {
            TokenType.GT: ">", TokenType.LT: "<",
            TokenType.GTE: ">=", TokenType.LTE: "<=",
            TokenType.EQ: "==", TokenType.NEQ: "!=",
        }
        if self.atual().tipo in _cmp_ops:
            op = _cmp_ops[self.avancar().tipo]
            right = self.parse_additive()
            node = BinaryOpNode(op=op, left=node, right=right)
        return node

    def parse_additive(self) -> NoAST:
        """additive: multiplicative (('+' | '-') multiplicative)*"""
        node = self.parse_multiplicative()
        while self.atual().tipo in (TokenType.PLUS, TokenType.MINUS):
            op = self.avancar().valor  # '+' or '-'
            right = self.parse_multiplicative()
            node = BinaryOpNode(op=op, left=node, right=right)
        return node

    def parse_multiplicative(self) -> NoAST:
        """multiplicative: primary (('*' | '/') primary)*"""
        node = self.parse_primary()
        while self.atual().tipo in (TokenType.STAR, TokenType.SLASH):
            op = self.avancar().valor  # '*' or '/'
            right = self.parse_primary()
            node = BinaryOpNode(op=op, left=node, right=right)
        return node

    def parse_primary(self) -> NoAST:
        """primary: NUMBER | STRING | IDENTIFIER ['(' args ')'] | '(' expression ')'"""
        t = self.atual()
        if t.tipo == TokenType.NUMBER:
            self.avancar()
            try:
                val: Any = int(t.valor)
            except ValueError:
                val = float(t.valor)
            return Literal(valor=val, linha=t.linha)
        elif t.tipo == TokenType.STRING:
            self.avancar()
            return Literal(valor=t.valor, linha=t.linha)
        elif t.tipo == TokenType.IDENTIFIER:
            self.avancar()
            if self.atual().tipo == TokenType.LPAREN:
                # function call: func(arg1, arg2, ...)
                self.avancar()  # consume '('
                args = []
                if self.atual().tipo != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    while self.atual().tipo == TokenType.COMMA:
                        self.avancar()
                        args.append(self.parse_expression())
                self.consumir(TokenType.RPAREN)
                return CallNode(func=t.valor, args=args, linha=t.linha)
            return Identificador(nome=t.valor, linha=t.linha)
        elif t.tipo == TokenType.LPAREN:
            self.avancar()
            node = self.parse_expression()
            self.consumir(TokenType.RPAREN)
            return node
        elif t.tipo == TokenType.MINUS:
            # unary minus
            self.avancar()
            operand = self.parse_primary()
            return BinaryOpNode(op="-", left=Literal(valor=0), right=operand)
        else:
            self.erro("Expressão esperada (número, string, identificador ou '(')")

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
            # Consome anotação de tipo (ignorada no MVP)
            self.avancar()
            while self.atual().tipo not in (TokenType.LBRACE, TokenType.NEWLINE, TokenType.EOF):
                self.avancar()
        self.consumir(TokenType.LBRACE)
        self.pular_newlines()
        corpo = []
        while self.atual().tipo != TokenType.RBRACE:
            no = self.parse_declaracao()
            if no: corpo.append(no)
            self.pular_newlines()
        self.consumir(TokenType.RBRACE)
        return FuncaoDecl(nome=nome, parametros=params, corpo=corpo, linha=linha)

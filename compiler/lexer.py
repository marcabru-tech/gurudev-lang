"""GuruDev Lexer v0.1-MVP"""
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List

class TokenType(Enum):
    NUMBER = auto(); STRING = auto(); IDENTIFIER = auto()
    DEF = auto(); TAG = auto(); BIND = auto(); MAP = auto()
    CLAVE = auto(); HERMENEUTICA = auto(); DISPATCH = auto()
    CASE = auto(); DEFAULT = auto(); LOAD = auto()
    DISPLAY = auto(); EVALUATE = auto(); TRANSCODE = auto()
    EMOTE = auto(); IN = auto(); CONTEXT = auto()
    ASSIGN = auto(); ARROW = auto()
    LPAREN = auto(); RPAREN = auto()
    LBRACE = auto(); RBRACE = auto()
    LBRACKET = auto(); RBRACKET = auto()
    COLON = auto(); COMMA = auto(); SEMICOLON = auto()
    NEWLINE = auto(); EOF = auto(); INVALID = auto()

@dataclass
class Token:
    tipo: TokenType
    valor: str
    linha: int
    coluna: int

class Lexer:
    PALAVRAS = {
        'def': TokenType.DEF, 'tag': TokenType.TAG,
        'bind': TokenType.BIND, 'map': TokenType.MAP,
        'clave': TokenType.CLAVE, 'hermeneutica': TokenType.HERMENEUTICA,
        'dispatch': TokenType.DISPATCH, 'case': TokenType.CASE,
        'default': TokenType.DEFAULT, 'load': TokenType.LOAD,
        'display': TokenType.DISPLAY, 'evaluate': TokenType.EVALUATE,
        'transcode': TokenType.TRANSCODE, 'emote': TokenType.EMOTE,
        'in': TokenType.IN, 'context': TokenType.CONTEXT,
    }

    def __init__(self, codigo: str):
        self.codigo = codigo
        self.pos = 0; self.linha = 1; self.coluna = 1
        self.tokens: List[Token] = []

    def peek(self, offset=0) -> str:
        p = self.pos + offset
        return self.codigo[p] if p < len(self.codigo) else '\0'

    def avancar(self):
        if self.peek() == '\n':
            self.linha += 1; self.coluna = 1
        else:
            self.coluna += 1
        self.pos += 1

    def pular_espacos(self):
        while self.peek() in ' \t\r':
            self.avancar()

    def pular_comentario(self):
        if self.peek() == '#':
            while self.peek() not in ('\n', '\0'):
                self.avancar()

    def ler_numero(self) -> Token:
        l, c = self.linha, self.coluna; s = ''
        while self.peek().isdigit() or self.peek() == '.':
            s += self.peek(); self.avancar()
        return Token(TokenType.NUMBER, s, l, c)

    def ler_string(self) -> Token:
        l, c = self.linha, self.coluna
        self.avancar(); s = ''
        while self.peek() != '"' and self.peek() != '\0':
            if self.peek() == '\\':
                self.avancar()
                s += {'n': '\n', 't': '\t'}.get(self.peek(), self.peek())
            else:
                s += self.peek()
            self.avancar()
        if self.peek() != '"':
            raise SyntaxError(f"String não terminada na linha {l}")
        self.avancar()
        return Token(TokenType.STRING, s, l, c)

    def ler_identificador(self) -> Token:
        l, c = self.linha, self.coluna; s = ''
        while self.peek().isalnum() or self.peek() == '_':
            s += self.peek(); self.avancar()
        tipo = self.PALAVRAS.get(s.lower(), TokenType.IDENTIFIER)
        return Token(tipo, s, l, c)

    def tokenizar(self) -> List[Token]:
        while self.pos < len(self.codigo):
            self.pular_espacos(); self.pular_comentario(); self.pular_espacos()
            if self.pos >= len(self.codigo):
                break
            ch = self.peek(); l, c = self.linha, self.coluna
            if   ch == '\n':  self.tokens.append(Token(TokenType.NEWLINE, '\\n', l, c)); self.avancar()
            elif ch == '"':   self.tokens.append(self.ler_string())
            elif ch.isdigit():self.tokens.append(self.ler_numero())
            elif ch.isalpha() or ch == '_': self.tokens.append(self.ler_identificador())
            elif ch == '=' :  self.tokens.append(Token(TokenType.ASSIGN,   '=',  l, c)); self.avancar()
            elif ch == '-' and self.peek(1) == '>':
                self.tokens.append(Token(TokenType.ARROW, '->', l, c)); self.avancar(); self.avancar()
            elif ch == '(':   self.tokens.append(Token(TokenType.LPAREN,   '(',  l, c)); self.avancar()
            elif ch == ')':   self.tokens.append(Token(TokenType.RPAREN,   ')',  l, c)); self.avancar()
            elif ch == '{':   self.tokens.append(Token(TokenType.LBRACE,   '{',  l, c)); self.avancar()
            elif ch == '}':   self.tokens.append(Token(TokenType.RBRACE,   '}',  l, c)); self.avancar()
            elif ch == '[':   self.tokens.append(Token(TokenType.LBRACKET, '[',  l, c)); self.avancar()
            elif ch == ']':   self.tokens.append(Token(TokenType.RBRACKET, ']',  l, c)); self.avancar()
            elif ch == ':':   self.tokens.append(Token(TokenType.COLON,    ':',  l, c)); self.avancar()
            elif ch == ',':   self.tokens.append(Token(TokenType.COMMA,    ',',  l, c)); self.avancar()
            elif ch == ';':   self.tokens.append(Token(TokenType.SEMICOLON,';',  l, c)); self.avancar()
            else:
                raise SyntaxError(f"Caractere inesperado '{ch}' na linha {l}, coluna {c}")
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.linha, self.coluna))
        return self.tokens

"""GuruDev Lexer v0.2 - Análise léxica robusta com recuperação de erros."""
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Iterator
import sys
import os

# Adicionando o diretório raiz ao path para importar gurudev.exceptions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from gurudev.exceptions import LexerError
except ImportError:
    # Fallback caso o pacote ainda não esteja instalado
    class LexerError(Exception):
        def __init__(self, char, line, column, **kwargs):
            super().__init__(f"Caractere inesperado '{char}' na linha {line}, coluna {column}")

class TokenType(Enum):
    # Literais
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords
    DEF = auto()
    TAG = auto()
    BIND = auto()
    MAP = auto()
    CLAVE = auto()
    HERMENEUTICA = auto()
    DISPATCH = auto()
    CASE = auto()
    DEFAULT = auto()
    LOAD = auto()
    DISPLAY = auto()
    EVALUATE = auto()
    TRANSCODE = auto()
    EMOTE = auto()
    IN = auto()
    CONTEXT = auto()
    
    # Operadores
    ASSIGN = auto()
    ARROW = auto()
    
    # Delimitadores
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COLON = auto()
    COMMA = auto()
    SEMICOLON = auto()
    
    # Especiais
    NEWLINE = auto()
    EOF = auto()
    INVALID = auto()

@dataclass(frozen=True)
class Token:
    """Token imutável da linguagem GuruDev."""
    tipo: TokenType
    valor: str
    linha: int
    coluna: int

    def __repr__(self) -> str:
        return f"Token({self.tipo.name}, '{self.valor}', {self.linha}:{self.coluna})"

class Lexer:
    """Analisador léxico para código-fonte GuruDev."""
    PALAVRAS_CHAVE: dict[str, TokenType] = {
        'def': TokenType.DEF,
        'tag': TokenType.TAG,
        'bind': TokenType.BIND,
        'map': TokenType.MAP,
        'clave': TokenType.CLAVE,
        'hermeneutica': TokenType.HERMENEUTICA,
        'dispatch': TokenType.DISPATCH,
        'case': TokenType.CASE,
        'default': TokenType.DEFAULT,
        'load': TokenType.LOAD,
        'display': TokenType.DISPLAY,
        'evaluate': TokenType.EVALUATE,
        'transcode': TokenType.TRANSCODE,
        'emote': TokenType.EMOTE,
        'in': TokenType.IN,
        'context': TokenType.CONTEXT,
    }

    ESCAPES: dict[str, str] = {
        'n': '\n',
        't': '\t',
        'r': '\r',
        '\\': '\\',
        '"': '"',
        "'": "'",
    }

    def __init__(self, codigo: str, filename: str = "<input>"):
        self.codigo = codigo
        self.filename = filename
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        self.tokens: List[Token] = []
        self.erros: List[LexerError] = []

    @property
    def atual(self) -> str:
        """Retorna caractere atual ou '\0' se fim."""
        return self.codigo[self.pos] if self.pos < len(self.codigo) else '\0'

    @property
    def proximo(self) -> str:
        """Retorna próximo caractere ou '\0' se fim."""
        return self.codigo[self.pos + 1] if self.pos + 1 < len(self.codigo) else '\0'

    def avancar(self) -> str:
        """Avança para o próximo caractere."""
        ch = self.atual
        if ch == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        self.pos += 1
        return ch

    def pular_espacos(self) -> None:
        """Pula espaços e tabs."""
        while self.atual in ' \t\r':
            self.avancar()

    def pular_comentario(self) -> None:
        """Pula comentários de linha (#)."""
        if self.atual == '#':
            while self.atual not in ('\n', '\0'):
                self.avancar()

    def pular_whitespace(self) -> None:
        """Pula todos os caracteres de espaço, incluindo comentários."""
        while True:
            self.pular_espacos()
            if self.atual == '#':
                self.pular_comentario()
            else:
                break

    def ler_numero(self) -> Token:
        """Lê um número (inteiro ou float)."""
        linha, coluna = self.linha, self.coluna
        numero = ''
        tem_ponto = False
        while self.atual.isdigit() or (self.atual == '.' and not tem_ponto):
            if self.atual == '.':
                tem_ponto = True
            numero += self.avancar()
        
        # Validação: não pode terminar com ponto
        if numero.endswith('.'):
            self.erros.append(LexerError(
                char='.',
                line=linha,
                column=coluna + len(numero) - 1,
                suggestion="Número não pode terminar com ponto decimal."
            ))
        return Token(TokenType.NUMBER, numero, linha, coluna)

    def ler_string(self) -> Token:
        """Lê uma string entre aspas duplas com suporte a escapes."""
        linha, coluna = self.linha, self.coluna
        self.avancar() # consome aspas de abertura
        conteudo = ''
        while self.atual != '"' and self.atual != '\0':
            if self.atual == '\\':
                self.avancar()
                escape_char = self.avancar()
                conteudo += self.ESCAPES.get(escape_char, escape_char)
            else:
                conteudo += self.avancar()
        
        if self.atual != '"':
            raise LexerError(
                char='\0',
                line=linha,
                column=coluna,
                suggestion="Adicione aspas de fechamento para a string."
            )
        self.avancar() # consome aspas de fechamento
        return Token(TokenType.STRING, conteudo, linha, coluna)

    def ler_identificador(self) -> Token:
        """Lê um identificador ou palavra-chave."""
        linha, coluna = self.linha, self.coluna
        ident = ''
        while self.atual.isalnum() or self.atual == '_':
            ident += self.avancar()
        tipo = self.PALAVRAS_CHAVE.get(ident.lower(), TokenType.IDENTIFIER)
        return Token(tipo, ident, linha, coluna)

    def tokenizar(self) -> List[Token]:
        """Executa a tokenização completa do código-fonte."""
        while self.pos < len(self.codigo):
            self.pular_whitespace()
            if self.pos >= len(self.codigo):
                break
            
            ch = self.atual
            linha, coluna = self.linha, self.coluna
            
            # Nova linha
            if ch == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', linha, coluna))
                self.avancar()
            # String
            elif ch == '"':
                self.tokens.append(self.ler_string())
            # Número
            elif ch.isdigit():
                self.tokens.append(self.ler_numero())
            # Identificador
            elif ch.isalpha() or ch == '_':
                self.tokens.append(self.ler_identificador())
            # Operadores e delimitadores
            elif ch == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', linha, coluna))
                self.avancar()
            elif ch == '-' and self.proximo == '>':
                self.tokens.append(Token(TokenType.ARROW, '->', linha, coluna))
                self.avancar()
                self.avancar()
            elif ch == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', linha, coluna))
                self.avancar()
            elif ch == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', linha, coluna))
                self.avancar()
            elif ch == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', linha, coluna))
                self.avancar()
            elif ch == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', linha, coluna))
                self.avancar()
            elif ch == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', linha, coluna))
                self.avancar()
            elif ch == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', linha, coluna))
                self.avancar()
            elif ch == ':':
                self.tokens.append(Token(TokenType.COLON, ':', linha, coluna))
                self.avancar()
            elif ch == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', linha, coluna))
                self.avancar()
            elif ch == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', linha, coluna))
                self.avancar()
            # Caractere inválido
            else:
                self.erros.append(LexerError(
                    char=ch,
                    line=linha,
                    column=coluna
                ))
                self.avancar()
        
        # Token EOF
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.linha, self.coluna))
        
        # Se houver erros, levanta o primeiro
        if self.erros:
            raise self.erros[0]
        return self.tokens

    def __iter__(self) -> Iterator[Token]:
        """Permite iterar sobre os tokens."""
        return iter(self.tokens)

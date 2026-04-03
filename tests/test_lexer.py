"""
test_lexer.py — Testes focados no analisador léxico GuruDev.
"""
import pytest
from compiler.lexer import Lexer, Token, TokenType


# ── Helpers ──────────────────────────────────────────────────────────────────

def tokenize(code: str):
    return Lexer(code).tokenizar()


def tipos(tokens):
    return [t.tipo for t in tokens if t.tipo != TokenType.EOF]


def valores(tokens):
    return [t.valor for t in tokens if t.tipo not in (TokenType.EOF, TokenType.NEWLINE)]


# ── Keywords ─────────────────────────────────────────────────────────────────

class TestKeywords:
    def test_keyword_def(self):
        assert TokenType.DEF in tipos(tokenize("def"))

    def test_keyword_bind(self):
        assert TokenType.BIND in tipos(tokenize("bind"))

    def test_keyword_tag(self):
        assert TokenType.TAG in tipos(tokenize("tag"))

    def test_keyword_load(self):
        assert TokenType.LOAD in tipos(tokenize("load"))

    def test_keyword_dispatch(self):
        assert TokenType.DISPATCH in tipos(tokenize("dispatch"))

    def test_keyword_case(self):
        assert TokenType.CASE in tipos(tokenize("case"))

    def test_keyword_default(self):
        assert TokenType.DEFAULT in tipos(tokenize("default"))

    def test_keyword_display(self):
        assert TokenType.DISPLAY in tipos(tokenize("display"))

    def test_keyword_evaluate(self):
        assert TokenType.EVALUATE in tipos(tokenize("evaluate"))

    def test_keyword_in(self):
        assert TokenType.IN in tipos(tokenize("in"))

    def test_keyword_context(self):
        assert TokenType.CONTEXT in tipos(tokenize("context"))

    def test_keyword_case_insensitive(self):
        assert TokenType.BIND in tipos(tokenize("BIND"))

    def test_alias_mostre(self):
        toks = tokenize("mostre")
        assert toks[0].tipo == TokenType.DISPLAY
        assert toks[0].valor == "mostre"


# ── Literais ─────────────────────────────────────────────────────────────────

class TestLiterals:
    def test_integer(self):
        toks = tokenize("42")
        assert toks[0].tipo == TokenType.NUMBER
        assert toks[0].valor == "42"

    def test_float(self):
        toks = tokenize("3.14")
        assert toks[0].tipo == TokenType.NUMBER
        assert toks[0].valor == "3.14"

    def test_string_double_quote(self):
        toks = tokenize('"hello world"')
        assert toks[0].tipo == TokenType.STRING
        assert toks[0].valor == "hello world"

    def test_string_with_escape(self):
        toks = tokenize(r'"line1\nline2"')
        assert toks[0].tipo == TokenType.STRING
        assert "\n" in toks[0].valor

    def test_identifier(self):
        toks = tokenize("formula_energia")
        assert toks[0].tipo == TokenType.IDENTIFIER
        assert toks[0].valor == "formula_energia"


# ── Delimitadores ─────────────────────────────────────────────────────────────

class TestDelimiters:
    def test_braces(self):
        toks = tokenize("{ }")
        t = tipos(toks)
        assert TokenType.LBRACE in t
        assert TokenType.RBRACE in t

    def test_parens(self):
        toks = tokenize("( )")
        t = tipos(toks)
        assert TokenType.LPAREN in t
        assert TokenType.RPAREN in t

    def test_colon(self):
        assert TokenType.COLON in tipos(tokenize(":"))

    def test_comma(self):
        assert TokenType.COMMA in tipos(tokenize(","))

    def test_assign(self):
        assert TokenType.ASSIGN in tipos(tokenize("="))


# ── Comentários ───────────────────────────────────────────────────────────────

class TestComments:
    def test_hash_comment_skipped(self):
        toks = tokenize("# this is a comment\nbind")
        uteis = [t for t in toks if t.tipo not in (TokenType.NEWLINE, TokenType.EOF)]
        assert uteis[0].tipo == TokenType.BIND

    def test_double_slash_comment_skipped(self):
        toks = tokenize("// comment\nbind")
        uteis = [t for t in toks if t.tipo not in (TokenType.NEWLINE, TokenType.EOF)]
        assert uteis[0].tipo == TokenType.BIND

    def test_inline_hash_comment(self):
        toks = tokenize("bind # inline comment")
        uteis = [t for t in toks if t.tipo not in (TokenType.NEWLINE, TokenType.EOF)]
        assert len(uteis) == 1
        assert uteis[0].tipo == TokenType.BIND


# ── Posição / metadata ────────────────────────────────────────────────────────

class TestTokenMetadata:
    def test_token_linha(self):
        toks = tokenize("bind\nclave")
        bind_tok = next(t for t in toks if t.tipo == TokenType.BIND)
        clave_tok = next(t for t in toks if t.tipo == TokenType.CLAVE)
        assert bind_tok.linha == 1
        assert clave_tok.linha == 2

    def test_eof_always_present(self):
        toks = tokenize("")
        assert toks[-1].tipo == TokenType.EOF

    def test_token_repr(self):
        toks = tokenize("bind")
        assert "BIND" in repr(toks[0])


# ── Sequências completas ──────────────────────────────────────────────────────

class TestFullSequences:
    def test_bind_clave_assign(self):
        toks = tokenize("bind clave = ciencia")
        t = [tok for tok in toks if tok.tipo != TokenType.EOF]
        assert t[0].tipo == TokenType.BIND
        assert t[1].tipo == TokenType.CLAVE
        assert t[2].tipo == TokenType.ASSIGN
        assert t[3].tipo == TokenType.IDENTIFIER

    def test_dispatch_block(self):
        codigo = "dispatch hermeneutica x { case 1: display in context }"
        toks = tokenize(codigo)
        t = tipos(toks)
        assert TokenType.DISPATCH in t
        assert TokenType.HERMENEUTICA in t
        assert TokenType.CASE in t
        assert TokenType.DISPLAY in t
        assert TokenType.IN in t
        assert TokenType.CONTEXT in t

    def test_numero_seguido_de_colon(self):
        toks = tokenize("1:")
        assert toks[0].tipo == TokenType.NUMBER
        assert toks[1].tipo == TokenType.COLON

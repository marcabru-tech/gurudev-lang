
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from compiler.lexer import Lexer, TokenType

def test_lexer_alias_mostre():
    codigo = 'mostre "teste"'
    tokens = Lexer(codigo).tokenizar()
    # [DISPLAY, STRING, EOF]
    assert tokens[0].tipo == TokenType.DISPLAY
    assert tokens[0].valor == 'mostre'

def test_lexer_comentario_barra_dupla():
    codigo = '// comentario\nmostre "oi"'
    tokens = Lexer(codigo).tokenizar()
    # O comentário é pulado, mas o \n gera um token NEWLINE se estiver na lógica do loop principal
    # Vamos verificar se o primeiro token útil é DISPLAY
    uteis = [t for t in tokens if t.tipo not in (TokenType.NEWLINE, TokenType.EOF)]
    assert uteis[0].tipo == TokenType.DISPLAY
    assert uteis[0].valor == 'mostre'

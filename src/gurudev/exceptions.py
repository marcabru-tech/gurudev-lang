"""Exceções customizadas do GuruDev."""

class GuruDevError(Exception):
    """Exceção base para todos os erros do GuruDev."""
    def __init__(self, message: str, line: int = 0, column: int = 0,
                 file: str = "", suggestion: str = ""):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column
        self.file = file
        self.suggestion = suggestion

    def __str__(self) -> str:
        parts = [self.message]
        if self.file:
            parts.append(f"em {self.file}")
        if self.line:
            loc = f"linha {self.line}"
            if self.column:
                loc += f", coluna {self.column}"
            parts.append(loc)
        if self.suggestion:
            parts.append(f"\n💡 Dica: {self.suggestion}")
        return " ".join(parts)

class LexerError(GuruDevError):
    """Erro durante a análise léxica."""
    def __init__(self, char: str, line: int, column: int, **kwargs):
        super().__init__(
            message=f"Caractere inesperado '{char}'",
            line=line,
            column=column,
            suggestion="Verifique se o caractere é válido na linguagem GuruDev.",
            **kwargs
        )

class ParserError(GuruDevError):
    """Erro durante a análise sintática."""
    def __init__(self, expected: str, found: str, line: int, **kwargs):
        super().__init__(
            message=f"Esperado {expected}, encontrado '{found}'",
            line=line,
            suggestion=f"Verifique a sintaxe. Esperado: {expected}",
            **kwargs
        )

class SemanticError(GuruDevError):
    """Erro durante a análise semântica."""
    pass

class GuruRuntimeError(GuruDevError):
    """Erro durante a execução no GuruDVM."""
    pass

class HermeneuticsError(GuruRuntimeError):
    """Erro específico de nível hermenêutico inválido."""
    def __init__(self, nivel: int, **kwargs):
        super().__init__(
            message=f"Nível hermenêutico inválido: {nivel}",
            suggestion="O nível hermenêutico deve estar entre 1 e 7.",
            **kwargs
        )

class ResourceNotFoundError(GuruRuntimeError):
    """Recurso não encontrado durante LOAD."""
    def __init__(self, resource_name: str, **kwargs):
        super().__init__(
            message=f"Recurso não encontrado: '{resource_name}'",
            suggestion="Verifique se o recurso foi carregado com carregar_recurso().",
            **kwargs
        )

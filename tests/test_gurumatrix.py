"""
tests/test_gurumatrix.py — GuruMatrix v0.2 cell coverage and validation.

Verifica:
  - CELLS cobre exactamente 100 células (10×10)
  - Cada célula em CELLS tem os campos obrigatórios
  - Sem células fantasma (toda referência tem definição)
  - Validação de acesso por nome (SemanticError em nomes inválidos)
  - get_by_name levanta SemanticError para ontologia/domínio inexistentes
  - get_by_name_safe retorna None sem levantar exceção
  - validate_cell_reference funciona
  - GuruMatrix inicializa todas as 100 células
"""
from __future__ import annotations

import pytest

from gurudev.exceptions import SemanticError
from gurumatrix.cells import CELLS, cell_meta
from gurumatrix.core import Dominio, GuruMatrix, Ontologia


# ── CELLS dict ────────────────────────────────────────────────────────────────

class TestCellsRegistry:
    def test_cells_tem_100_entradas(self):
        assert len(CELLS) == 100

    def test_cells_cobre_todos_ontologias(self):
        onts = {m["ontologia"] for m in CELLS.values()}
        assert onts == {o.name for o in Ontologia}

    def test_cells_cobre_todos_dominios(self):
        doms = {m["dominio"] for m in CELLS.values()}
        assert doms == {d.name for d in Dominio}

    def test_cells_campos_obrigatorios(self):
        required = {"name", "ontologia", "dominio", "handler", "stub", "description"}
        for name, meta in CELLS.items():
            assert required <= meta.keys(), f"Célula '{name}' falta campos: {required - meta.keys()}"

    def test_cells_name_igual_chave(self):
        for key, meta in CELLS.items():
            assert meta["name"] == key

    def test_cells_stub_eh_bool(self):
        for name, meta in CELLS.items():
            assert isinstance(meta["stub"], bool), f"'{name}': stub deve ser bool"

    def test_cells_description_nao_vazia(self):
        for name, meta in CELLS.items():
            assert isinstance(meta["description"], str) and meta["description"].strip(), \
                f"'{name}': description deve ser string não vazia"

    def test_cells_handler_callable_ou_none(self):
        for name, meta in CELLS.items():
            h = meta["handler"]
            assert h is None or callable(h), f"'{name}': handler deve ser callable ou None"

    def test_stub_handler_retorna_dict(self):
        meta = CELLS["ACAO_CIENCIA"]
        resultado = meta["handler"]()
        assert isinstance(resultado, dict)
        assert resultado["status"] == "stub"
        assert resultado["cell"] == "ACAO_CIENCIA"

    def test_sem_celulas_fantasma(self):
        """Toda célula em CELLS deve ter coordenada válida na GuruMatrix."""
        matrix = GuruMatrix()
        for name in CELLS:
            ont_name, dom_name = name.split("_", 1)
            celula = matrix.get_by_name_safe(ont_name, dom_name)
            assert celula is not None, f"Célula fantasma detectada: '{name}'"

    def test_cell_meta_funcao(self):
        meta = cell_meta(Ontologia.ACAO, Dominio.CIENCIA)
        assert meta["name"] == "ACAO_CIENCIA"
        assert "description" in meta


# ── GuruMatrix init e acessos ─────────────────────────────────────────────────

class TestGuruMatrixInit:
    def test_matrix_tem_100_celulas(self):
        matrix = GuruMatrix()
        assert len(matrix.celulas) == 100

    def test_todas_celulas_inicializadas(self):
        matrix = GuruMatrix()
        for ont in Ontologia:
            for dom in Dominio:
                celula = matrix.get(ont, dom)
                assert celula is not None
                assert celula.x == ont
                assert celula.y == dom

    def test_celula_nome_correto(self):
        matrix = GuruMatrix()
        celula = matrix.get(Ontologia.ACAO, Dominio.CIENCIA)
        assert celula.nome == "ACAO_CIENCIA"

    def test_celula_coordenada_correta(self):
        matrix = GuruMatrix()
        celula = matrix.get(Ontologia.SUBSTANCIA, Dominio.TECNOLOGIA)
        assert celula.coordenada == (Ontologia.SUBSTANCIA.value, Dominio.TECNOLOGIA.value)


# ── Validação de acesso ────────────────────────────────────────────────────────

class TestValidacao:
    def test_get_by_name_valido(self):
        matrix = GuruMatrix()
        celula = matrix.get_by_name("ACAO", "CIENCIA")
        assert celula.nome == "ACAO_CIENCIA"

    def test_get_by_name_invalido_ontologia_levanta_semantic_error(self):
        matrix = GuruMatrix()
        with pytest.raises(SemanticError) as exc_info:
            matrix.get_by_name("FANTASMA", "CIENCIA")
        assert "FANTASMA" in str(exc_info.value)

    def test_get_by_name_invalido_dominio_levanta_semantic_error(self):
        matrix = GuruMatrix()
        with pytest.raises(SemanticError) as exc_info:
            matrix.get_by_name("ACAO", "INEXISTENTE")
        assert "INEXISTENTE" in str(exc_info.value)

    def test_get_by_name_safe_invalido_retorna_none(self):
        matrix = GuruMatrix()
        resultado = matrix.get_by_name_safe("FANTASMA", "CIENCIA")
        assert resultado is None

    def test_get_by_name_safe_invalido_dominio_retorna_none(self):
        matrix = GuruMatrix()
        resultado = matrix.get_by_name_safe("ACAO", "FANTASMA")
        assert resultado is None

    def test_get_by_name_case_insensitive(self):
        matrix = GuruMatrix()
        celula = matrix.get_by_name("acao", "ciencia")
        assert celula.nome == "ACAO_CIENCIA"

    def test_validate_cell_reference_valida(self):
        matrix = GuruMatrix()
        assert matrix.validate_cell_reference("ACAO_CIENCIA") is True

    def test_validate_cell_reference_invalida_levanta_semantic_error(self):
        matrix = GuruMatrix()
        with pytest.raises(SemanticError):
            matrix.validate_cell_reference("FANTASMA_INEXISTENTE")

    def test_validate_cell_reference_formato_errado(self):
        matrix = GuruMatrix()
        with pytest.raises(SemanticError) as exc_info:
            matrix.validate_cell_reference("SEMUNDERSCORE")
        assert "Formato esperado" in str(exc_info.value)

    def test_semantic_error_tem_dica(self):
        matrix = GuruMatrix()
        with pytest.raises(SemanticError) as exc_info:
            matrix.get_by_name("INVALIDO", "CIENCIA")
        erro = exc_info.value
        assert "Dica" in str(erro) or erro.suggestion


# ── Sem regressão em células populadas ───────────────────────────────────────

class TestPopularMinimo:
    def test_popular_minimo_executa_sem_erro(self):
        matrix = GuruMatrix()
        celula = matrix.get(Ontologia.ACAO, Dominio.CIENCIA)
        assert len(celula.objetos) > 0

    def test_buscar_homologos(self):
        matrix = GuruMatrix()
        homologos = matrix.buscar_homologos(Ontologia.ACAO, Dominio.CIENCIA)
        assert isinstance(homologos, list)

    def test_buscar_similitudes(self):
        matrix = GuruMatrix()
        similitudes = matrix.buscar_similitudes(Dominio.CIENCIA, Ontologia.ACAO)
        assert isinstance(similitudes, list)

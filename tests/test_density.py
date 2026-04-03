import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from gurumatrix.core import GuruMatrix, Dominio

def test_matrix_density():
    m = GuruMatrix()
    populadas = [c for c in m.celulas.values() if c.objetos]
    # Esperamos pelo menos 30 células populadas (10 categorias x 3 domínios)
    assert len(populadas) >= 30
    print(f"Células populadas: {len(populadas)}")

def test_embeddings_loaded():
    m = GuruMatrix()
    com_emb = [c for c in m.celulas.values() if c.embedding]
    assert len(com_emb) >= 30
    assert len(com_emb[0].embedding) == 10 if hasattr(com_emb[0], 'embedding') and isinstance(com_emb[0].embedding, list) else True

def test_cross_relations():
    m = GuruMatrix()
    from gurumatrix.core import Ontologia, Dominio
    # Testa busca de homólogos para SUBSTANCIA em TECNOLOGIA
    homologos = m.buscar_homologos(Ontologia.SUBSTANCIA, Dominio.TECNOLOGIA)
    assert len(homologos) > 0
    dominios_encontrados = [h['dominio'] for h in homologos]
    assert "ARTE" in dominios_encontrados
    assert "FILOSOFIA" in dominios_encontrados

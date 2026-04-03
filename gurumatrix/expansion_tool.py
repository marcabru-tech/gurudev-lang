"""
GuruMatrix Expansion Tool v0.1
Ferramenta para popular a Matrix com objetos e relações semânticas via LLM.
"""
import json
from typing import List, Dict, Any
from openai import OpenAI
from gurumatrix.core import Ontologia, Dominio, RelacaoSemantica

client = OpenAI()

PROMPT_SISTEMA = """
Você é o Oráculo da GuruMatrix, uma estrutura ontológica de 10x10 baseada nas Categorias de Aristóteles (X) e Domínios do Conhecimento Humano (Y).
Sua tarefa é identificar 3 a 5 objetos fundamentais para uma coordenada específica (Ontologia, Dominio) e as relações semânticas que eles mantêm.

As Ontologias são: SUBSTANCIA, QUANTIDADE, QUALIDADE, RELACAO, LUGAR, TEMPO, SITUACAO, CONDICAO, ACAO, PAIXAO.
Os Domínios são: ARTE, CIENCIA, FILOSOFIA, TRADICAO_ESPIRITUAL, TECNOLOGIA, LINGUAGEM, MATEMATICA, MEDICINA_BIOLOGIA, DIREITO_ETICA, EDUCACAO.

Responda APENAS em JSON no formato:
{
  "objetos": ["objeto1", "objeto2", "objeto3"],
  "relacoes": ["similitude", "homologia", "equivalencia"],
  "instrucoes": ["DISPLAY", "EVALUATE"]
}
"""

def sugerir_conteudo(ontologia: str, dominio: str) -> Dict[str, Any]:
    prompt_usuario = f"Sugira objetos e relações para a célula: Ontologia={ontologia}, Domínio={dominio}."
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": prompt_usuario}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def expandir_matrix(matrix_core, dominios_alvo: List[str] = None):
    """Popula a matrix com sugestões da LLM."""
    for ont in Ontologia:
        for dom in Dominio:
            if dominios_alvo and dom.name not in dominios_alvo:
                continue
            
            print(f"Expandindo: {ont.name} x {dom.name}...")
            try:
                sugestao = sugerir_conteudo(ont.name, dom.name)
                celula = matrix_core.get(ont, dom)
                
                for obj in sugestao.get("objetos", []):
                    celula.adicionar_objeto(obj)
                
                # Mapeia strings para Enums de RelacaoSemantica
                for rel_str in sugestao.get("relacoes", []):
                    try:
                        rel_enum = RelacaoSemantica(rel_str.lower())
                        if rel_enum not in celula.relacoes_ativas:
                            celula.relacoes_ativas.append(rel_enum)
                    except ValueError:
                        continue
                
                celula.instrucoes_preferenciais.extend(sugestao.get("instrucoes", []))
                
            except Exception as e:
                print(f"Erro ao expandir {ont.name}x{dom.name}: {e}")

if __name__ == "__main__":
    # Teste rápido para um domínio
    from gurumatrix.core import GuruMatrix
    m = GuruMatrix()
    expandir_matrix(m, ["TECNOLOGIA"])
    print(m)

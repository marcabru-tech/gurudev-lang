import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
from openai import OpenAI
from gurumatrix.core import GuruMatrix

client = OpenAI()

def gerar_embedding(texto: str) -> list:
    # Usando gpt-4.1-mini para simular embeddings via representação textual (mock para o sandbox)
    # Em um ambiente real com API key de produção, usaria text-embedding-3-small
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": f"Gere um vetor de 10 floats (separados por vírgula) que represente semanticamente este texto: {texto}. Retorne APENAS os números separados por vírgula, sem texto adicional."}]
    )
    vec_str = response.choices[0].message.content.strip()
    # Limpeza básica para garantir que pegamos apenas os números
    import re
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", vec_str)
    return [float(x) for x in nums[:10]]

def main():
    m = GuruMatrix()
    embeddings_data = {}
    
    print("Gerando embeddings para as células populadas...")
    for coord, celula in m.celulas.items():
        if celula.objetos:
            # Cria uma descrição textual da célula para o embedding
            descricao = f"Célula ontológica de {celula.x.name} no domínio de {celula.y.name}. Objetos: {', '.join(celula.objetos)}."
            print(f"Processando {celula.nome}...")
            try:
                emb = gerar_embedding(descricao)
                embeddings_data[celula.nome] = emb
            except Exception as e:
                print(f"Erro em {celula.nome}: {e}")
                
    output_path = Path("/home/ubuntu/gurudev-repo/gurumatrix/embeddings_v0.2.json")
    with open(output_path, "w") as f:
        json.dump(embeddings_data, f)
        
    print(f"Embeddings salvos em {output_path}")

if __name__ == "__main__":
    main()

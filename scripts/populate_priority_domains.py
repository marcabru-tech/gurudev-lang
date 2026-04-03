import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import json
from gurumatrix.core import GuruMatrix
from gurumatrix.expansion_tool import expandir_matrix

def main():
    m = GuruMatrix()
    dominios_prioritarios = ["FILOSOFIA", "TECNOLOGIA", "ARTE"]
    
    print(f"Iniciando expansão para os domínios: {dominios_prioritarios}")
    expandir_matrix(m, dominios_prioritarios)
    
    # Exportar os dados populados para persistência
    dados_matrix = {}
    for coord, celula in m.celulas.items():
        if celula.objetos:
            dados_matrix[f"{celula.x.name}_{celula.y.name}"] = {
                "objetos": celula.objetos,
                "relacoes": [r.value for r in celula.relacoes_ativas],
                "instrucoes": celula.instrucoes_preferenciais
            }
            
    output_path = Path("/home/ubuntu/gurudev-repo/gurumatrix/data_v0.2.json")
    with open(output_path, "w") as f:
        json.dump(dados_matrix, f, indent=4, ensure_ascii=False)
    
    print(f"Expansão concluída! Dados salvos em {output_path}")

if __name__ == "__main__":
    main()

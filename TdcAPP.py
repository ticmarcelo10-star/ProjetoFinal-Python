import json
import os

FICHEIRO_DADOS = "tdc.json"

# ==========================================
# 1. GESTÃO DE DADOS (JSON)
# ==========================================

def carregar_dados():
    """Lê a informação do ficheiro JSON. Se não existir, cria a estrutura base."""
    if not os.path.exists(FICHEIRO_DADOS):
        dados_iniciais = {"atuacoes": [], "financas": [], "multimedia": []}
        guardar_dados(dados_iniciais)
        return dados_iniciais
    
    with open(FICHEIRO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_dados(dados):
    """Guarda o estado atual no ficheiro JSON."""
    with open(FICHEIRO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


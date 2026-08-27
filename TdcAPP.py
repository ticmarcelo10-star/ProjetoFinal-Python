import json
import os

FICHEIRO_DADOS = "tdc.json"

# ==========================================
# 1. GESTÃO DE DADOS (JSON)
# ==========================================

def carregar_dados():
    """Lê a informação do ficheiro JSON. Se não existir, cria a estrutura base com contas padrão."""
    if not os.path.exists(FICHEIRO_DADOS):
        dados_iniciais = {
            "utilizadores": [
                {"id": 1, "username": "admin", "password": "admtdc26", "perfil": "admin"},
                {"id": 2, "username": "membro", "password": "trocadalho26", "perfil": "membro"}
            ],
            "atuacoes": [],
            "financas": [],
            "multimedia": []
        }
        guardar_dados(dados_iniciais)
        return dados_iniciais
    
    with open(FICHEIRO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_dados(dados):
    """Guarda o estado atual no ficheiro JSON."""
    with open(FICHEIRO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# ==========================================
# 2. LOGIN E AUTENTICAÇÃO 
# ==========================================

def fazer_login(dados):
    """Gere a autenticação com repetição em caso de credenciais incorretas."""
    while True:
        print("\n==================================")
        print("      BEM-VINDO À TROCAPP         ")
        print("==================================")
        print("1. Entrar com conta (Admin / Membro)")
        print("2. Entrar como Visitante")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            username_input = input("Utilizador: ").strip().lower()
            password_input = input("Palavra-passe: ").strip()
            
            utilizadores = dados.get("utilizadores", [])
            
            # Procurar se existe algum utilizador que coincida com os dados inseridos
            login_sucesso = False
            for u in utilizadores:
                if u["username"].lower() == username_input and u["password"] == password_input:
                    print(f"\n✓ Login efetuado com sucesso como {u['perfil'].upper()}!")
                    return u["perfil"]  # Devolve o perfil e sai do ciclo
            
            # Se percorreu a lista e não encontrou correspondência
            print("\n❌ Credenciais incorretas! Tente novamente.")
            
        elif opcao == "2":
            print("\nSessão iniciada como VISITANTE.")
            return "visitante"
            
        elif opcao == "0":
            return None  # Indica que o utilizador quis sair do programa
            
        else:
            print("\n❌ Opção inválida. Tente novamente.")
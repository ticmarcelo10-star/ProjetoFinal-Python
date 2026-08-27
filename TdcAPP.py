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

# ==========================================
# 3. MÓDULO DE ATUAÇÕES
# ==========================================

def listar_atuacoes(dados):
    """Lista as atuações registadas (com opção de filtrar por agenda)."""
    print("\n--- LISTA DE ATUAÇÕES ---")
    atuacoes = dados.get("atuacoes", [])
    if not atuacoes:
        print("Nenhuma atuação registada.")
        return
    
    for a in atuacoes:
        print(f"[{a['id']}] {a['data']} às {a['hora']} | {a['tipo']} em {a['local']} (Agenda: {a['agenda']})")

def adicionar_atuacao(dados):
    """Adiciona uma nova atuação."""
    print("\n--- ADICIONAR NOVA ATUAÇÃO ---")
    data = input("Data (DD-MM-AAAA): ")
    hora = input("Hora (HH:MM): ")
    local = input("Local: ")
    tipo = input("Tipo (ex: Arruada, Procissão): ")
    agenda = input("Agenda (publica / interna): ").lower()
    
    atuacoes = dados.get("atuacoes", [])
    novo_id = max([a["id"] for a in atuacoes], default=0) + 1
    
    nova = {
        "id": novo_id,
        "data": data,
        "hora": hora,
        "local": local,
        "tipo": tipo,
        "agenda": agenda if agenda in ["publica", "interna"] else "publica",
        "estado": "ativa"
    }
    
    dados["atuacoes"].append(nova)
    guardar_dados(dados)
    print("✓ Atuação adicionada com sucesso!")

def editar_atuacao(dados):
    """Permite editar os detalhes de uma atuação existente procurando pelo seu ID."""
    listar_atuacoes(dados)
    atuacoes = dados.get("atuacoes", [])
    if not atuacoes:
        return
        
    try:
        id_procurado = int(input("\nDigite o ID da atuação que deseja editar: "))
    except ValueError:
        print("❌ ID inválido. Deve inserir um número.")
        return

    # Procurar a atuação pelo ID
    atuacao_encontrada = None
    for a in atuacoes:
        if a["id"] == id_procurado:
            atuacao_encontrada = a
            break

    if not atuacao_encontrada:
        print("❌ Atuação não encontrada.")
        return

    print(f"\n--- A EDITAR ATUAÇÃO [{atuacao_encontrada['id']}] ---")
    print("(Pressione ENTER sem escrever nada se quiser manter o valor atual)")

    nova_data = input(f"Nova Data (atual: {atuacao_encontrada['data']}): ").strip()
    nova_hora = input(f"Nova Hora (atual: {atuacao_encontrada['hora']}): ").strip()
    novo_local = input(f"Novo Local (atual: {atuacao_encontrada['local']}): ").strip()
    novo_tipo = input(f"Novo Tipo (atual: {atuacao_encontrada['tipo']}): ").strip()
    nova_agenda = input(f"Nova Agenda (publica/interna) (atual: {atuacao_encontrada['agenda']}): ").strip().lower()

    # Atualizar apenas os campos que o utilizador preencheu
    if nova_data:
        atuacao_encontrada["data"] = nova_data
    if nova_hora:
        atuacao_encontrada["hora"] = nova_hora
    if novo_local:
        atuacao_encontrada["local"] = novo_local
    if novo_tipo:
        atuacao_encontrada["tipo"] = novo_tipo
    if nova_agenda in ["publica", "interna"]:
        atuacao_encontrada["agenda"] = nova_agenda

    guardar_dados(dados)
    print("✓ Atuação atualizada com sucesso!")


def remover_atuacao(dados):
    """Remove uma atuação dos dados pelo seu ID."""
    listar_atuacoes(dados)
    atuacoes = dados.get("atuacoes", [])
    if not atuacoes:
        return

    try:
        id_procurado = int(input("\nDigite o ID da atuação que deseja remover: "))
    except ValueError:
        print("❌ ID inválido. Deve inserir um número.")
        return

    # Verificar se a atuação existe
    atuacao_existente = any(a["id"] == id_procurado for a in atuacoes)
    if not atuacao_existente:
        print("❌ Atuação não encontrada.")
        return

    confirmacao = input(f"Tem a certeza que deseja remover a atuação [{id_procurado}]? (s/n): ").strip().lower()
    if confirmacao == "s":
        # Filtra a lista mantendo apenas os elementos com ID diferente
        dados["atuacoes"] = [a for a in atuacoes if a["id"] != id_procurado]
        guardar_dados(dados)
        print("✓ Atuação removida com sucesso!")
    else:
        print("Operação cancelada.")
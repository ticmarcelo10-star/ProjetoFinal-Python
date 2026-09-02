import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "chave_secreta_tdcapp_bombos"
FICHEIRO_DADOS = "tdc.json"

# ==========================================
# LEITURA E ESCRITA DO JSON
# ==========================================

def carregar_dados():
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
    with open(FICHEIRO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# ==========================================
# AUTENTICAÇÃO
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        opcao = request.form.get("opcao")
        
        if opcao == "visitante":
            session["perfil"] = "visitante"
            session["username"] = "Visitante"
            return redirect(url_for("atuacoes"))
            
        username_input = request.form.get("username", "").strip().lower()
        password_input = request.form.get("password", "").strip()
        
        dados = carregar_dados()
        for u in dados.get("utilizadores", []):
            if u["username"].lower() == username_input and u["password"] == password_input:
                session["perfil"] = u["perfil"]
                session["username"] = u["username"]
                return redirect(url_for("atuacoes"))
        
        flash("Credenciais incorretas! Tente novamente.")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ==========================================
# ATUAÇÕES
# ==========================================

@app.route("/")
@app.route("/atuacoes")
def atuacoes():
    if "perfil" not in session:
        return redirect(url_for("login"))
        
    dados = carregar_dados()
    lista = dados.get("atuacoes", [])
    
    if session.get("perfil") == "visitante":
        lista = [a for a in lista if a.get("agenda") == "publica"]
        
    return render_template("index.html", atuacoes=lista, perfil=session.get("perfil"))

@app.route("/atuacoes/adicionar", methods=["POST"])
def adicionar_atuacao():
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    atuacoes_lista = dados.get("atuacoes", [])
    novo_id = max([a["id"] for a in atuacoes_lista], default=0) + 1
    
    nova = {
        "id": novo_id,
        "data": request.form.get("data"),
        "hora": request.form.get("hora"),
        "local": request.form.get("local"),
        "tipo": request.form.get("tipo"),
        "agenda": request.form.get("agenda", "publica"),
        "estado": "ativa"
    }
    
    dados["atuacoes"].append(nova)
    guardar_dados(dados)
    return redirect(url_for("atuacoes"))

@app.route("/atuacoes/editar/<int:id_atuacao>", methods=["GET", "POST"])
def editar_atuacao(id_atuacao):
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    
    # Procura a atuação pelo ID
    atuacao_encontrada = None
    for a in dados.get("atuacoes", []):
        if a["id"] == id_atuacao:
            atuacao_encontrada = a
            break

    if request.method == "POST":
        if atuacao_encontrada:
            atuacao_encontrada["data"] = request.form.get("data")
            atuacao_encontrada["hora"] = request.form.get("hora")
            atuacao_encontrada["local"] = request.form.get("local")
            atuacao_encontrada["tipo"] = request.form.get("tipo")
            atuacao_encontrada["agenda"] = request.form.get("agenda")
            atuacao_encontrada["estado"] = request.form.get("estado")
            guardar_dados(dados)
        return redirect(url_for("atuacoes"))
        
    # Se for GET, abre a página com os dados
    return render_template("editar_atuacao.html", atuacao=atuacao_encontrada, perfil=session.get("perfil"))


@app.route("/atuacoes/estado/<int:id_atuacao>/<novo_estado>")
def alterar_estado_atuacao(id_atuacao, novo_estado):
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    for a in dados.get("atuacoes", []):
        if a["id"] == id_atuacao:
            a["estado"] = novo_estado
            break
            
    guardar_dados(dados)
    return redirect(url_for("atuacoes"))

@app.route("/atuacoes/remover/<int:id_atuacao>")
def remover_atuacao(id_atuacao):
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    dados["atuacoes"] = [a for a in dados.get("atuacoes", []) if a["id"] != id_atuacao]
    guardar_dados(dados)
    return redirect(url_for("atuacoes"))

# ==========================================
# FINANÇAS
# ==========================================

@app.route("/financas", methods=["GET", "POST"])
def financas():
    if session.get("perfil") not in ["admin", "membro"]:
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    
    if request.method == "POST" and session.get("perfil") == "admin":
        movimentos = dados.get("financas", [])
        novo_id = max([m["id"] for m in movimentos], default=0) + 1
        
        novo_movimento = {
            "id": novo_id,
            "tipo": request.form.get("tipo"),
            "descricao": request.form.get("descricao"),
            "valor": float(request.form.get("valor", 0)),
            "data": request.form.get("data")
        }
        
        dados["financas"].append(novo_movimento)
        guardar_dados(dados)
        return redirect(url_for("financas"))
        
    financas_lista = dados.get("financas", [])
    total_receitas = sum(m["valor"] for m in financas_lista if m["tipo"] == "receita")
    total_despesas = sum(m["valor"] for m in financas_lista if m["tipo"] == "despesa")
    saldo = total_receitas - total_despesas
    
    return render_template(
        "financas.html", 
        financas=financas_lista, 
        total_receitas=total_receitas, 
        total_despesas=total_despesas, 
        saldo=saldo,
        perfil=session.get("perfil")
    )

@app.route("/financas/remover/<int:id_movimento>")
def remover_financa(id_movimento):
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    dados["financas"] = [m for m in dados.get("financas", []) if m["id"] != id_movimento]
    guardar_dados(dados)
    return redirect(url_for("financas"))

@app.route("/financas/editar/<int:id_financa>", methods=["GET", "POST"])
def editar_financa(id_financa):
    # Restrição de acesso (apenas Admin ou Membro, conforme as regras da app)
    if session.get("perfil") not in ["admin", "membro"]:
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    
    # Procura a transação/movimento pelo ID
    financa_encontrada = None
    for f in dados.get("financas", []):
        if f["id"] == id_financa:
            financa_encontrada = f
            break

    if not financa_encontrada:
        return "Movimento não encontrado", 404

    if request.method == "POST":
        financa_encontrada["tipo"] = request.form.get("tipo", financa_encontrada["tipo"])
        financa_encontrada["descricao"] = request.form.get("descricao", financa_encontrada["descricao"])
        
        # Converte o valor para float para garantir cálculos corretos no saldo
        try:
            financa_encontrada["valor"] = float(request.form.get("valor", financa_encontrada["valor"]))
        except ValueError:
            pass
            
        financa_encontrada["data"] = request.form.get("data", financa_encontrada["data"])
        
        guardar_dados(dados)
        return redirect(url_for("financas"))
        
    return render_template("editar_financa.html", financa=financa_encontrada, perfil=session.get("perfil"))

# ==========================================
# MULTIMÉDIA
# ==========================================

@app.route("/multimedia", methods=["GET", "POST"])
def multimedia():
    if "perfil" not in session:
        return redirect(url_for("login"))
        
    dados = carregar_dados()
    
    if request.method == "POST" and session.get("perfil") in ["admin", "membro"]:
        media_lista = dados.get("multimedia", [])
        novo_id = max([m["id"] for m in media_lista], default=0) + 1
        
        novo_item = {
            "id": novo_id,
            "titulo": request.form.get("titulo"),
            "link": request.form.get("link"),
            "tipo": request.form.get("tipo")
        }
        
        dados["multimedia"].append(novo_item)
        guardar_dados(dados)
        return redirect(url_for("multimedia"))
        
    return render_template("multimedia.html", media=dados.get("multimedia", []), perfil=session.get("perfil"))

@app.route("/multimedia/remover/<int:id_media>")
def remover_multimedia(id_media):
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    dados["multimedia"] = [m for m in dados.get("multimedia", []) if m["id"] != id_media]
    guardar_dados(dados)
    return redirect(url_for("multimedia"))

# ==========================================
# UTILIZADORES
# ==========================================

@app.route("/utilizadores", methods=["GET", "POST"])
def utilizadores():
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    
    if request.method == "POST":
        users = dados.get("utilizadores", [])
        novo_id = max([u["id"] for u in users], default=0) + 1
        
        novo_user = {
            "id": novo_id,
            "username": request.form.get("username").strip().lower(),
            "password": request.form.get("password").strip(),
            "perfil": request.form.get("perfil")
        }
        
        dados["utilizadores"].append(novo_user)
        guardar_dados(dados)
        return redirect(url_for("utilizadores"))
        
    return render_template("utilizadores.html", utilizadores=dados.get("utilizadores", []), perfil=session.get("perfil"))

@app.route("/utilizadores/remover/<int:id_user>")
def remover_utilizador(id_user):
    if session.get("perfil") != "admin":
        return "Acesso Negado", 403
        
    dados = carregar_dados()
    dados["utilizadores"] = [u for u in dados.get("utilizadores", []) if u["id"] != id_user]
    guardar_dados(dados)
    return redirect(url_for("utilizadores"))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
# 🥁 TdCApp - Sistema de Gestão de Grupo de Bombos Trocadalho do Carilho

O **TdCApp** é uma aplicação web desenvolvida em Python com o *framework* Flask, criada para centralizar a gestão de atuações, controlo financeiro, partilha de multimédia e gestão de utilizadores de um grupo cultural/musical.

---

## 🎯 1. Identificação do Problema e Público-Alvo

### O Problema
O grupo de bombos Trocadalho do Carilho necessita de um local centralizado para organizar as suas atuações, informações financeiras e conteúdos multimédia. A TdCApp pretende reunir esta informação numa única aplicação web, facilitando a consulta e a gestão dos dados do grupo. 

### Público-Alvo
A aplicação adapta a sua interface e funcionalidades com base em três perfis de acesso (RBAC):
* **Administrador:** Responsável pela gestão total do grupo (atuações, movimentos financeiros e gestão de utilizadores).
* **Membro:** Membros do grupo de bombos. Acede à agenda interna, consulta o relatório financeiro e os conteúdos na galeria multimédia.
* **Visitante:** Destinado ao fãs do grupo. Acede à agenda pública e aos conteúdos na galeria multimédia.

---

## 🚀 2. Descrição do MVP e Extensões Implementadas

* **MVP (Produto Mínimo Viável):**
  * Autenticação de utilizadores com sessão persistente.
  * Leitura e escrita automatizada de dados em ficheiro JSON.
  * Listagem e criação de atuações da agenda.

* **Extensões Implementadas:**
  * **Controlo de Acessos (RBAC):** Restrições de segurança por rota com respostas HTTP `403 Acesso Negado`.
  * **Agenda Diferenciada:** Separação entre eventos de agenda pública e privada.
  * **Gestão Financeira:** Registo de receitas/despesas com cálculo automático do saldo acumulado.
  * **Galeria Multimédia:** Partilha e gestão de links de fotos e vídeos de atuações.
  * **Painel de Utilizadores:** Gestão de membros e permissões por parte do Administrador.

---

## 💾 3. Estrutura dos Dados (`tdc.json`)

A aplicação utiliza o ficheiro `tdc.json` para garantir a persistência dos dados. Caso o ficheiro não exista na primeira execução, a aplicação cria-o automaticamente com o seguinte esquema:

```json
{
    "utilizadores": [
        {
            "id": 1,
            "username": "admin",
            "password": "...",
            "perfil": "admin"
        }
    ],
    "atuacoes": [
        {
            "id": 1,
            "data": "2026-09-15",
            "hora": "21:00",
            "local": "Praça Central",
            "tipo": "Arruada",
            "agenda": "publica",
            "estado": "ativa"
        }
    ],
    "financas": [
        {
            "id": 1,
            "tipo": "receita",
            "descricao": "Cachet Atuação",
            "valor": 150.0,
            "data": "2026-09-15"
        }
    ],
    "multimedia": [
        {
            "id": 1,
            "titulo": "Atuação de Verão",
            "link": "https://...",
            "tipo": "foto"
        }
    ]
}
```
---

## ⚙️ 4. Instruções de Execução e Utilização

### Pré-requisitos
* Python 3.8 ou superior instalado.
* Biblioteca Flask instalada (`pip install flask`).

---

### Passo a Passo para Executar

#### Estrutura de Pastas do Projeto
Certifica-te de que a estrutura do projeto está organizada da seguinte forma:

```plaintext
TdCApp/
├── TdcApp.py
├── tdc.json (gerado automaticamente no arranque caso não exista)
└── templates/
    ├── base.html
    ├── editar_atuacao.html
    ├── editar_financa.html
    ├── login.html
    ├── index.html
    ├── financas.html
    ├── multimedia.html
    └── utilizadores.html
```

#### Iniciar o Servidor
Abre o terminal na raiz do projeto e executa:

```bash
python app.py
```

O servidor ficará ativo em `http://127.0.0.1:5000`.

#### Aceder à Aplicação
Navega no browser até ao endereço de login:  
👉 `http://127.0.0.1:5000/login`

---

### Credenciais de Acesso Predefinidas

* **Administrador:** Username: `admin` | Password: *****
* **Membro:** Username: `membro` | Password: *****
* **Visitante:** Clica no botão "Entrar como Visitante" no ecrã de login (sem password).

---

## 🛠️ 5. Principais Funções do Programa

O ficheiro principal `TdCApp.py` organiza-se nos seguintes módulos e funções:

### Módulo de Persistência (JSON)
* `carregar_dados()`: Lê o ficheiro `tdc.json` e inicializa a estrutura por omissão caso o ficheiro não exista.
* `guardar_dados(dados)`: Escreve as alterações efetuadas diretamente no ficheiro `tdc.json`.

### Módulo de Autenticação
* `login()` (`/login` — GET/POST): Valida as credenciais do utilizador ou regista a sessão como visitante (`session['perfil']`).
* `logout()` (`/logout` — GET): Destrói a sessão atual e redireciona para a página de login.

### Módulo de Gestão de Atuações (Agenda)
* `atuacoes()` (`/atuacoes` — GET): Apresenta a lista de eventos. Aplica um filtro para ocultar eventos privados caso o perfil seja visitante.
* `adicionar_atuacao()` (`/atuacoes/adicionar` — POST): Permite a criação de um novo evento (Administrador).
* `editar_atuacao()` (`/atuacoes/editar/<id>` — GET/POST): Permite a edição de um evento já criado (Administrador).
* `alterar_estado_atuacao(id_atuacao, novo_estado)` (`/atuacoes/estado/...` — GET): Atualiza o estado da atuação para "ativa" ou "cancelada" (Administrador).
* `remover_atuacao(id_atuacao)` (`/atuacoes/remover/<id>` — GET): Elimina uma atuação (Administrador).

### Módulo Financeiro
* `financas()` (`/financas` — GET/POST): Apresenta o histórico de receitas/despesas, calcula o saldo total acumulado e permite registar novos movimentos (Administrador).
* `remover_financa()` (`/financas/remover/<id>` — GET/POST): Remove um movimento financeiro (Administrador).
* `editar_financa()` (`/financas/editar/<id>` — GET/POST): Edita um movimento financeiro (Administrador).

### Módulo Multimédia
* `multimedia()` (`/multimedia` — GET/POST): Apresenta fotos e vídeos das atuações.
                                             Permite ao adicionar hiperligações para fotos e vídeos das atuações. (Administrador)
* `remover_multimedia()` (`/multimedia/remover/<id>` — GET): Remove uma hiperligação de foto ou vídeo já criada. (Administrador)

### Módulo Utilizadores
* `utilizadores()` (`/utilizadores` — GET/POST): Permite ao Administrador criar e gerir as contas de acesso da aplicação.
* `remover_utilizador()` (`/utilizadores/remover/<id>` — GET): Permite ao Administrador remover as contas de acesso da aplicação.

## 🏗️ 6. Decomposição Inicial da Solução

A aplicação foi decomposta numa arquitetura modular baseada em rotas HTTP e funções de suporte no `TdCApp.py`. A lógica segue o fluxo de leitura/escrita no ficheiro `tdc.json`, controlo de sessão e filtragem de vistas com base no perfil do utilizador.

### Tabela de Funções e Rotas

| Função / Rota Flask | Método HTTP | Descrição / Responsabilidade | Permissões |
| :--- | :--- | :--- | :--- |
| `carregar_dados()` | N/A | Lê o ficheiro `tdc.json`. Se não existir, cria-o automaticamente com dados iniciais. | Interno |
| `guardar_dados(dados)` | N/A | Escreve a estrutura atualizada de dicionários/listas no ficheiro `tdc.json`. | Interno |
| `login()` (`/login`) | GET / POST | Autentica utilizadores, inicia a sessão (`session['perfil']`) ou permite acesso como visitante. | Público |
| `logout()` (`/logout`) | GET | Limpa os dados de sessão e redireciona para a página de login. | Autenticado |
| `atuacoes()` (`/atuacoes`) | GET | Apresenta a lista de eventos. Filtra apenas eventos de agenda pública se for visitante. | Admin / Membro / Visitante |
| `adicionar_atuacao()` (`/atuacoes/adicionar`) | POST | Regista uma nova atuação no sistema e grava no JSON. | Admin |
| `editar_atuacao()` (`/atuacoes/editar/<id>`) | GET / POST | Permite a edição de um evento já criado . | Admin |
| `alterar_estado_atuacao()` (`/atuacoes/estado/...`) | GET | Altera o estado de uma atuação (ex: ativa/cancelada). | Admin |
| `remover_atuacao()` (`/atuacoes/remover/<id>`) | GET | Remove uma atuação pelo ID e atualiza o JSON. | Admin |
| `financas()` (`/financas`) | GET / POST | Apresenta o histórico financeiro, calcula o saldo total e permite registar movimentos. | Admin / Membro |
| `remover_financa()` (`/financas/remover/<id>`) | GET | Remover um movimento financeiro. | Admin |
| `editar_financa()` (`/financas/editar/<id>`) | GET / POST | Editar um movimento financeiro. | Admin |
| `multimedia()` (`/multimedia`) | GET / POST | Apresenta a galeria e permite adicionar hiperligações para fotos ou vídeos. | Admin / Membro / Visitante |
| `remover_multimedia()` (`/multimedia/remover/<id>`) | GET | Permite ao Administrador remover as contas de acesso da aplicação.  | Admin |
| `utilizadores()` (`/utilizadores`) | GET / POST | Permite criar novas contas de utilizador com perfis definidos (`admin` ou `membro`). | Admin |
| `remover_utilizador()` (`/utilizadores/remover/<id>`) | GET | Permite ao Administrador remover as contas de acesso da aplicação. | Admin |

### Pseudocódigo do Fluxo de Permissões (RBAC)
```text
INÍCIO RotaProtegida(requisicao, perfil_necessario)
    SE perfil_atual NÃO ESTÁ NA SESSÃO ENTÃO
        REDIRECIONAR PARA "/login"
    FIM SE

    SE perfil_atual NÃO TEM PERMISSÃO PARA perfil_necessario ENTÃO
        RETORNAR RESPOSTA HTTP 403 ("Acesso Negado")
    SENÃO
        EXECUTAR OPERAÇÃO E ATUALIZAR tdc.json
        RETORNAR PAGINA HTML
    FIM SE
FIM
```
---
---

## 🧪 7. Casos de Teste

Para validar a aplicação, foram executados três casos de teste principais, cobrindo uma entrada inválida, uma condição-limite de segurança e um fluxo de entrada válida.

### ❌ Caso de Teste 1: Entrada Inválida
* **ID:** CT-01
* **Objetivo:** Validar o comportamento do sistema perante credenciais de login incorretas.
* **Ação/Entrada:** No formulário de login (`/login`), inserir `username: "admin"` e `password: "palavrapasseerrada"`.
* **Resultado Esperado:** Bloqueio do acesso, permanência na página de login e exibição da mensagem de erro *"Credenciais incorretas! Tente novamente."*.
* **Resultado Obtido:** Passou (o utilizador não conseguiu autenticar-se e a mensagem foi exibida).

---

### 🚫 Caso de Teste 2: Condição-Limite (Segurança RBAC)
* **ID:** CT-02
* **Objetivo:** Verificar a proteção de rotas restritas contra acessos não autorizados.
* **Ação/Entrada:** Autenticar como perfil `visitante` e tentar aceder diretamente pelo navegador ao URL restrito `http://127.0.0.1:5000/financas`.
* **Resultado Esperado:** Bloqueio imediato do pedido pelo servidor com a resposta de erro **HTTP 403 (Acesso Negado)**.
* **Resultado Obtido:** Passou (o servidor interrompeu o pedido e apresentou a mensagem "Acesso Negado").

---

### ✅ Caso de Teste 3: Entrada Válida
* **ID:** CT-03
* **Objetivo:** Confirmar a criação de um evento e a sua persistência no ficheiro `tdc.json`.
* **Ação/Entrada:** Autenticar como `admin`, preencher o formulário em `/atuacoes` com a data *"2026-10-01"*, hora *"21:00"*, local *"Praça Central"*, tipo *"Arruada"* e submeter.
* **Resultado Esperado:** Inserção do novo registo na tabela da página web e atualização imediata do ficheiro `tdc.json`.
* **Resultado Obtido:** Passou (a atuação passou a figurar na lista do site e ficou gravada no JSON).
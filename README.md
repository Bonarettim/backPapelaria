# 📚 API de Controle de Vendas e Comissões — Papelaria

Este é um projeto de API robusto desenvolvido em Django e Django REST Framework (DRF) para o gerenciamento de vendas, clientes, produtos e o cálculo automatizado e dinâmico de comissões de vendedores de uma papelaria. 

A arquitetura do sistema segue as melhores práticas de mercado, isolando regras de negócio em uma camada dedicada de **Services**, utilizando **PostgreSQL** como banco de dados e garantindo a padronização do código através do **Ruff** (PEP 8, PEP 257).

---

## 🚀 Tecnologias Utilizadas & Pré-requisitos

O ecossistema do projeto foi construído utilizando as seguintes versões e ferramentas:

* **Backend:** Python (v3.14+) / Django (v6.0+)
* **API REST:** Django REST Framework (DRF)
* **Banco de Dados:** PostgreSQL (v15+)
* **Ferramenta de Banco:** DBeaver (Para visualização e gerenciamento local)
* **Qualidade de Código & Linter:** Ruff (Aderência estrita à PEP 8 e PEP 257)
* **Ambiente de Desenvolvimento:** PyCharm / Mac OS

---

## 🏗️ Padrões de Arquitetura & Boas Práticas

O projeto foi projetado com foco em modularidade, legibilidade e fácil manutenção:

1. **Modularização por Apps:** O sistema é dividido de forma limpa em contextos bem definidos: `sellers`, `customers`, `products`, `sales` e `commissions`.
2. **Service Pattern (Camada de Serviço):** Para evitar o antipadrão de *Fat Views* (Views pesadas), toda a inteligência de banco, queries de agregação (`Count`, `Sum`, `Q`) e formatação do JSON para o relatório foram isoladas em arquivos `service.py`.
3. **Slim Views:** As views atuam puramente como orquestradoras do tráfego e do protocolo HTTP.
4. **Qualidade de Código Contínua:** Linting e formatação automatizados com o Ruff para garantir conformidade contínua com os padrões oficiais do Python.

---

## 🗄️ Estrutura do Banco de Dados (PostgreSQL)

O mapeamento objeto-relacional (ORM) do Django gerencia e sincroniza automaticamente as tabelas estruturadas no PostgreSQL. As principais tabelas de negócio visíveis no DBeaver são:

* `customers` — Cadastro unificado de clientes.
* `sellers` — Cadastro unificado de vendedores.
* `products_product` — Catálogo de produtos da papelaria (preço unitário, percentual padrão de comissão).
* `sales_sale` — Cabeçalho da venda (número da nota, cliente, vendedor, data).
* `sales_saleitem` — Itens que compõem a venda (produto, quantidade e o valor final de comissão calculado).
* `commission_rules` & `sales_daycommissionrule` — Definições dinâmicas de bônus ou comissões por faixas e datas.

---

## ⚙️ Como Instalar e Rodar o Projeto Localmente

Siga o passo a passo abaixo para rodar o projeto no seu ambiente:

### 1. Clonar o Repositório
```bash
git clone [https://github.com/Bonarettim/backPapelaria.git](https://github.com/Bonarettim/backPapelaria.git)
cd backPapelaria 
```

### 2. Configurar o Ambiente Virtual (venv)

python -m venv venv
source venv/bin/activate

### 3. Instalar as Dependências

pip install -r requirements.txt

### 4. Configurar as Variáveis do Banco no settings.py
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'papelaria_db',
        'USER': 'postgres',
        'PASSWORD': 'SUA_SENHA_DO_POSTGRES',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Executar as Migrations (Criar tabelas no PostgreSQL)

python manage.py migrate

### 6. Iniciar o Servidor de Desenvolvimento

python manage.py runserver


## 👨‍💻 Autor

Matheus Bonaretti Simões
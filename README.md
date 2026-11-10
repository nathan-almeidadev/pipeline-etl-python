# Pipeline ETL com Python

Pipeline de Engenharia de Dados que extrai dados fictícios de usuários e
produtos, enriquece os usuários com informações de endereço da API ViaCEP,
normaliza os arquivos para Parquet e disponibiliza os dados em PostgreSQL para
consultas analíticas.

O projeto utiliza uma organização em camadas inspirada na **Medallion
Architecture**:

```text
Bronze (dados de origem) -> Silver (dados normalizados) -> Gold (consultas enriquecidas)
```

## Objetivos

- Ler dados de usuários em CSV e produtos em JSON.
- Consultar a API ViaCEP a partir dos CEPs dos usuários.
- Armazenar os dados de origem e os dados enriquecidos.
- Remover duplicidades e normalizar os dados em arquivos Parquet.
- Carregar a camada Silver em tabelas PostgreSQL.
- Disponibilizar consultas SQL para combinar usuários e informações de CEP.

## Tecnologias

- Python
- Pandas
- Requests
- PyArrow e Parquet
- PostgreSQL 16
- Psycopg2
- Docker e Docker Compose
- Jupyter Notebook

## Arquitetura e fluxo

![Fluxograma ETL](docs/architecture/etl-flow.png)

O fluxo principal é composto pelas seguintes etapas:

1. **Extração:** os arquivos `users.csv` e `products.json` são lidos da camada
   Bronze.
2. **Enriquecimento:** os CEPs dos usuários são consultados na API ViaCEP. Os
   resultados válidos são salvos em `cep_info.csv`.
3. **Normalização:** os arquivos CSV e JSON da Bronze são convertidos para
   Parquet, com remoção de duplicidades e conversão de listas para texto quando
   necessário.
4. **Carga:** os arquivos Parquet da Silver são carregados em tabelas
   PostgreSQL.
5. **Consultas Gold:** os arquivos SQL prontos combinam usuários e endereços e
   disponibilizam visões de contato e localização.

## Estrutura do projeto

```text
.
├── data/
│   ├── 01-bronze_raw/          # Fontes de entrada e resposta da ViaCEP
│   ├── 02-silver_validated/    # Dados normalizados em Parquet
│   └── 03-gold_enriched/      # Consultas SQL para análise
├── data_view/
│   └── dt_view.ipynb           # Exploração e visualização dos dados
├── docs/architecture/
│   ├── etl-flow.drawio         # Diagrama editável
│   └── etl-flow.png            # Diagrama exportado
├── src/
│   ├── get_data.py             # Consulta e grava dados da ViaCEP
│   ├── normalize_data.py       # Bronze -> Silver
│   ├── db.py                   # Conexão e operações no PostgreSQL
│   └── populate_db.py          # Silver -> PostgreSQL
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Pré-requisitos

- Python 3.10 ou superior
- Docker e Docker Compose
- Acesso à internet para consultar a API ViaCEP

## Instalação

Clone o repositório, crie um ambiente virtual e instale as dependências:

```bash
git clone https://github.com/nathan-almeidadev/pipeline-etl-python.git
cd pipeline-etl-python

python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows

pip install -r requirements.txt
```

## Execução

### 1. Iniciar o PostgreSQL

```bash
docker compose up -d db
```

O banco fica disponível em `localhost:5432` com as configurações definidas no
`docker-compose.yml`:

| Configuração | Valor |
|---|---|
| Banco | `db_etl_viacep` |
| Usuário | `postgres` |
| Senha | `viacep_etl` |
| Porta | `5432` |

Esses valores são apropriados para o ambiente local de demonstração. Em
produção, devem ser substituídos por variáveis de ambiente ou um gerenciador
de segredos.

### 2. Gerar os dados enriquecidos de CEP

Execute a partir da raiz do projeto:

```bash
python src/get_data.py
```

O script lê os CEPs de `data/01-bronze_raw/users.csv`, consulta a ViaCEP e
atualiza `data/01-bronze_raw/cep_info.csv`. CEPs inválidos ou não encontrados
são ignorados.

### 3. Normalizar os dados para Silver

```bash
python src/normalize_data.py
```

O comando processa os arquivos da Bronze e gera:

- `data/02-silver_validated/users.parquet`
- `data/02-silver_validated/products.parquet`
- `data/02-silver_validated/cep_info.parquet`

### 4. Carregar os dados no PostgreSQL

```bash
python src/populate_db.py
```

O script cria as tabelas `users`, `products` e `cep_info` caso ainda não
existam e insere os registros dos arquivos Parquet.

### 5. Executar consultas Gold

Com as tabelas carregadas, as consultas em
`data/03-gold_enriched/` podem ser executadas em qualquer cliente PostgreSQL:

- `users.sql`: consulta todos os usuários.
- `products.sql`: consulta todos os produtos.
- `users_cep_info.sql`: relaciona usuários às informações completas de endereço.
- `users_contact_info.sql`: consolida dados de contato e localização.

Para encerrar o banco:

```bash
docker compose down
```

Para remover também os dados persistidos no volume local:

```bash
docker compose down -v
```

## Camadas de dados

### Bronze

Contém os dados de origem, sem o tratamento principal do pipeline:

- `users.csv`: dados cadastrais e de contato dos usuários.
- `products.json`: catálogo de produtos, incluindo listas de tags.
- `cep_info.csv`: resposta tabular da consulta à ViaCEP.

### Silver

Contém os dados convertidos para Parquet, com duplicidades removidas e colunas
com listas convertidas para texto quando necessário. O formato Parquet facilita
o armazenamento colunar e a leitura posterior.

### Gold

Contém consultas SQL orientadas ao consumo analítico. As consultas fazem `JOIN`
entre `users` e `cep_info` pelo campo `cep`, permitindo analisar localização,
contato, estado, região e código IBGE.

## Dados e limitações conhecidas

Os dados do projeto são fictícios e servem para estudo e demonstração. A
consulta à ViaCEP depende de conectividade externa e o carregamento atual usa
as credenciais locais definidas no Docker Compose e no script de carga. Para
um ambiente de produção, recomenda-se parametrizar credenciais, adicionar
tratamento de timeout/retries na API, validar esquemas e tornar a carga
idempotente.

## Status

### Implementado

- [x] Extração de usuários em CSV.
- [x] Extração de produtos em JSON.
- [x] Enriquecimento de CEPs com a ViaCEP.
- [x] Normalização e remoção de duplicidades.
- [x] Geração de arquivos Parquet na camada Silver.
- [x] Configuração do PostgreSQL com Docker Compose.
- [x] Carga dos arquivos Silver em tabelas PostgreSQL.
- [x] Consultas SQL para a camada Gold.
- [x] Notebook para exploração dos dados.

### Evoluções recomendadas

- [ ] Adicionar testes automatizados.
- [ ] Usar variáveis de ambiente para configurações e credenciais.
- [ ] Implementar logging estruturado, timeout e retries para a API.
- [ ] Criar validações de esquema e métricas de qualidade.
- [ ] Automatizar o pipeline com um orquestrador.
- [ ] Criar dashboards e consultas analíticas adicionais.

## Autor

Nathan Luiz Almeida Vieira

Projeto desenvolvido para estudo e prática de Engenharia de Dados.

# Demoblaze Site - Projeto de API e Frontend

Este repositório contém uma aplicação web baseada em FastAPI com um frontend integrado. O objetivo do projeto é replicar localmente algumas funcionalidades do site Demoblaze, permitindo experimentos com uma arquitetura simples de API e frontend.

# Estrutura do Projeto
```
.
├── api
│   ├── Dockerfile
│   ├── main.py
│   ├── __pycache__
│   └── requirements.txt
├── docker-compose.yml
└── frontend
    ├── Dockerfile
    ├── nginx.conf
    └── static
        ├── bm.png
        ├── cart.html
        ├── config.json
        ├── css/
        ├── imgs/
        ├── js/
        ├── index.html
        └── produtos/
```

## Componentes Principais

* `api/`: Contém o backend implementado em FastAPI.
* `frontend/`: Contém o frontend estático e a configuração do servidor Nginx.
* `docker-compose.yml`: Define os serviços necessários (API, frontend e banco de dados) para execução com Docker Compose.
* `requirements.txt`: Lista de dependências Python necessárias para o backend.

# Requisitos

* Docker e Docker Compose instalados no sistema.
* Python 3.9 (opcional, caso você deseje executar a API fora do Docker).
* Banco de dados PostgreSQL (já configurado dentro do docker-compose.yml).

# Configuração do Ambiente

1. Clone o repositório:

```
git clone https://github.com/seu-usuario/demoblaze_site.git
cd demoblaze_site
```

2. Certifique-se de que o Docker está instalado e funcionando:

```
docker --version
docker-compose --version
```

# Inicialização do Projeto

1. Subir os Contêineres

Execute o seguinte comando para construir e iniciar os serviços:

```
docker-compose up --build
```

Isso iniciará:

* Banco de dados PostgreSQL
* Backend FastAPI
* Frontend Nginx

2. Acessar a Aplicação

* API: Acesse a API FastAPI em: http://localhost:8000.
* Frontend: O frontend estará disponível em: http://localhost:8000.

# Acesso ao Banco de Dados

Para acessar o banco de dados PostgreSQL via terminal:

```
docker exec -it demoblaze_site-db-1 psql -U demoblaze_user -d demoblaze
```
# Acesso as APIs

Para acessar o Swagger:

```
http://localhost:8000/docs#/default/ask_question_api_ask_question__post
```

teste de pipeline
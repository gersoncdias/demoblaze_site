Demoblaze Site - Projeto de API e Frontend

Este projeto contém uma aplicação web baseada em FastAPI com um frontend integrado. O objetivo do projeto é replicar algumas funcionalidades do site Demoblaze localmente.
Sumário

    Estrutura do Projeto
    Requisitos
    Configuração do Ambiente
    Inicialização do Projeto
    Acesso ao Banco de Dados
    Consultas e Operações no Banco de Dados
    Rotas da API

Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

arduino

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
        ├── css
        ├── imgs
        ├── js
        ├── index.html
        └── produtos

    api/: Contém o backend implementado em FastAPI.
    frontend/: Contém o frontend, arquivos estáticos, e a configuração do Nginx.
    docker-compose.yml: Define os serviços para execução com Docker Compose.
    requirements.txt: Lista de dependências Python para a API.

Requisitos

    Docker e Docker Compose instalados no sistema.
    Python 3.9 (caso você queira executar a API fora do Docker).
    PostgreSQL para banco de dados (embutido no Docker Compose).

Configuração do Ambiente

Clone o repositório:

bash

git clone https://seu-repositorio.git
cd demoblaze_site

Inicialização do Projeto
1. Subindo os Contêineres

Para iniciar os serviços, utilize:

bash

docker-compose up --build

Isso iniciará o banco de dados, a API e o frontend.
2. Acesso à Aplicação

    API: A API FastAPI estará disponível em http://127.0.0.1:8000.
    Frontend: O frontend estará disponível em http://127.0.0.1:8080.

Acesso ao Banco de Dados
Acesso ao Container do Banco de Dados

Para acessar o banco de dados via terminal:

bash

docker exec -it demoblaze_site-db-1 psql -U demoblaze_user -d demoblaze

Consultas e Operações no Banco de Dados
Listar todas as tabelas:

sql

\dt

Descrição de uma tabela:

sql

\d users

Inserir um novo usuário:

sql

INSERT INTO users (username, password) VALUES ('username', 'senha_codificada_em_base64');

Selecionar todos os usuários:

sql

SELECT * FROM users;

Deletar um usuário por ID:

sql

DELETE FROM users WHERE id = <id_do_usuario>;

Criação da Tabela users

Caso precise recriar a tabela users:

sql

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

Rotas da API
/signup - POST

Cria um novo usuário. Exemplo de payload:

json

{
  "username": "seu_username",
  "password": "senha_codificada_em_base64"
}

/login - POST

Realiza o login de um usuário. Exemplo de payload:

json

{
  "username": "seu_username",
  "password": "senha_codificada_em_base64"
}

Retorna um token de autenticação.
/users - GET

Retorna uma lista de todos os usuários cadastrados.
/delete_user/{user_id} - DELETE

Deleta um usuário específico pelo id.
/prod.html - GET

Retorna a página de produto estática correspondente ao idp_ fornecido.
Principais Comandos
Construir e Iniciar os Contêineres:

bash

docker-compose up --build

Acessar o Banco de Dados:

bash

docker exec -it demoblaze_site-db-1 psql -U demoblaze_user -d demoblaze

Parar os Contêineres:

bash

docker-compose down
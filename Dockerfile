# Usando uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta que a aplicação usa
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Usando a imagem base do Nginx
FROM nginx:alpine

# Copia os arquivos estáticos para o diretório padrão do Nginx
COPY ./static /usr/share/nginx/html

# Copia a configuração personalizada do Nginx
COPY nginx.conf /etc/nginx/nginx.conf

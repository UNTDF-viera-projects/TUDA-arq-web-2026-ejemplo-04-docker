FROM nginx:1.30.4-trixie

COPY ./dist /usr/share/nginx/html

# Documenta el puerto 80 del contenedor
EXPOSE 80

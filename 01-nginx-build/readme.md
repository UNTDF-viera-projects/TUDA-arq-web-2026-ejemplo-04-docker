# 01 - Nginx Build

## Descripción

Este es un ejemplo de como construir un contenedor de Nginx. En este caso, se construye un contenedor de Nginx y se copia el contenido de la carpeta `01-nginx-build` al contenedor, en el document root de Nginx.

Cada vez que se hace un cambio en el archivo `index.html`, se debe reconstruir el contenedor para que se actualice el contenido del contenedor.

Es importante notar que gracias a el `.dockerignore`, se ignoran los archivos `Dockerfile` y `readme.md` del build, al momento de hacer el `COPY . /usr/share/nginx/html/` en el `Dockerfile`.

## Comandos

Para construir el contenedor:
```bash
docker build -t untdf-nginx-build .
```

Para ejecutar el contenedor:
```bash
docker run -d -p 8080:80 untdf-nginx-build
```

Para ver los contenedores en ejecución:
```bash
docker ps
```
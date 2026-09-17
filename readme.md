# Ejercicios con Docker — Arquitecturas Web

Este repositorio contiene una serie de ejercicios prácticos para aprender a usar Docker en distintos escenarios de desarrollo web: desde servir archivos estáticos con Nginx hasta levantar una aplicación completa con backend, frontend y base de datos usando Docker Compose.

Cada carpeta es un ejercicio independiente con su propio `readme.md` y comandos.

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado y funcionando.
- (Opcional) `pnpm` si querés correr los proyectos Vite fuera de Docker, aunque todos los ejercicios están pensados para correr **dentro de contenedores**.

## Estructura

| Carpeta | Tema | ¿Qué práctica? |
| --- | --- | --- |
| [01-nginx-build](01-nginx-build) | Nginx con build | Copiar archivos estáticos dentro de una imagen. |
| [02-nginx-volume](02-nginx-volume) | Nginx con volumen | Usar un *bind mount* para desarrollar sin reconstruir. |
| [03-vite-dev-prod](03-vite-dev-prod) | Vite: desarrollo vs. producción | Dos Dockerfiles: uno para dev (volumen + hot reload) y otro para prod (multi-stage build + Nginx). |
| [04-network](04-network) | Red Docker manual | Levantar Django + PostgreSQL sin Compose, conectados por una red Docker. |
| [05-back-front-manual](05-back-front-manual) | Backend + frontend + DB a mano | Tres contenedores (Postgres, Django, Vite) levantados manualmente con `docker network`, `docker build` y `docker run`. |
| [06-back-front-compose](06-back-front-compose) | Docker Compose | Levantar todo el stack back + front + DB con un solo `docker compose up`. |
| [07-django-prod](07-django-prod) | Django en producción | Dockerfile de producción: código copiado en la imagen + **Gunicorn** (sin `runserver` ni volumen). |

## Recomendación de orden

Los ejercicios están pensados para hacerse en orden, porque cada uno introduce un concepto que el siguiente usa:

1. **01-nginx-build**: entender cómo se construye una imagen y cómo `COPY` funciona.
2. **02-nginx-volume**: entender la diferencia entre copiar archivos y montarlos con un volumen.
3. **03-vite-dev-prod**: combinar lo anterior con una app moderna (Vite + React) y ver el patrón de *multi-stage build*.
4. **04-network**: agregar comunicación entre contenedores usando redes Docker.
5. **05-back-front-manual**: escalar a tres contenedores interconectados sin Compose.
6. **06-back-front-compose**: automatizar todo con Docker Compose.
7. **07-django-prod**: el paralelo de producción en el backend (Gunicorn + código en la imagen), como el `prod.Dockerfile` de Vite.

## Convenciones usadas en los ejercicios

- Los nombres de imágenes y contenedores empiezan con `untdf-` para identificarlos fácilmente.
- Los puertos publicados al host suelen ser:
  - `8080` para Nginx o producción.
  - `5173` para el servidor de desarrollo de Vite.
  - `8000` para Django.
- Los ejemplos de comandos con `"${PWD}:/app"` funcionan en **bash/zsh (macOS, Linux, WSL, Git Bash)** y en **PowerShell (Windows)**.

## Cómo usar este repo

1. Clonar o descargar el repositorio.
2. Entrar a la carpeta del ejercicio que quieras practicar.
3. Leer el `readme.md` de esa carpeta.
4. Correr los comandos que aparecen allí.
5. Al terminar, detener y eliminar los contenedores para no dejar recursos colgados.

> Cada ejercicio incluye los comandos de limpieza al final de su propio `readme.md`.

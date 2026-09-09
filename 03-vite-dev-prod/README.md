# 03 - Vite: desarrollo vs producción

## Descripción

En `01-nginx-build` los archivos HTML se **copian dentro de la imagen**. En `02-nginx-volume` se **montan con un volumen**. En ambos casos el contenido ya era estático: Nginx podía servirlo tal cual.

Acá la app es de **Vite + React**. Eso cambia las reglas:

- En **desarrollo** no hay una página lista para copiar. Vite corre un servidor (puerto 5173) que transpila el código al vuelo y recarga el navegador cuando guardás un archivo.
- En **producción** Vite **compila** todo a HTML, JS y CSS estáticos en la carpeta `dist/`. A partir de ahí el problema es el mismo que en el ejercicio 01: Nginx sirve esos archivos.

Por eso hay **dos Dockerfiles**:

| | Desarrollo (`Dockerfile`) | Producción (`prod.Dockerfile`) |
| --- | --- | --- |
| Imagen base | `node` (hace falta el toolchain) | termina en `nginx` (solo sirve archivos) |
| Contenido | bind mount de esta carpeta sobre `/app` | el source entra en el `docker build`, se compila adentro, y a Nginx solo llega `dist/` |
| Puerto | 5173 | 80 (en el host: 8080) |
| Un cambio en el código | recargás el navegador y ya está | hay que reconstruir la imagen |

El compile corre **dentro de Docker** (`pnpm build` en el `prod.Dockerfile`). No hace falta tener Node en tu máquina, ni generar `dist/` a mano.

## Desarrollo

El `Dockerfile` no copia el proyecto: solo deja Node + pnpm, igual que en el ejercicio 02 el Dockerfile no copiaba el HTML. El código lo aporta el volumen.

`${PWD}` es el directorio de trabajo actual. Con las comillas, la misma forma sirve en **bash/zsh (macOS, Linux, Git Bash, WSL)** y en **PowerShell (Windows)**.

## Producción

El `prod.Dockerfile` tiene **dos etapas** (`FROM` … `AS build` y después otro `FROM`):

1. Parte de Node, copia el source, instala dependencias y corre `pnpm build`. Ahí nace `dist/`.
2. Parte de Nginx y hace `COPY --from=build` de `/app/dist` al document root. Es el mismo destino que en el ejercicio 01 (`/usr/share/nginx/html`).

La imagen que termina corriendo es solo Nginx + archivos estáticos. Node, pnpm y `node_modules` quedaron en la etapa de build y no se copian.

Por eso un cambio en el source **no se ve** hasta volver a construir: el contenido quedó congelado en la imagen, como en el ejercicio 01.

## Comandos

### Desarrollo

Para construir la imagen:

```bash
docker build -t untdf-vite-dev .
```

Para instalar dependencias (quedan en esta carpeta, gracias al volumen). Alcanza con hacerlo una vez, o cuando cambie `package.json`:

```bash
docker run --rm -v "${PWD}:/app" untdf-vite-dev pnpm install
```

Para ejecutar el servidor de desarrollo montando **esta carpeta** en `/app`:

```bash
docker run -d --name untdf-vite-dev -p 5173:5173 -v "${PWD}:/app" untdf-vite-dev
```

Abrí [http://localhost:5173](http://localhost:5173), cambiá algo en `src/App.tsx`, guardá y recargá: deberías ver el cambio sin reconstruir la imagen.

### Producción

Para construir la imagen (`-f` indica que el Dockerfile no se llama `Dockerfile`):

```bash
docker build -f prod.Dockerfile -t untdf-vite-prod .
```

Ese único comando copia el source, compila y arma la imagen de Nginx. No hay un `pnpm build` aparte.

Para ejecutar el contenedor de producción:

```bash
docker run -d --name untdf-vite-prod -p 8080:80 untdf-vite-prod
```

Abrí [http://localhost:8080](http://localhost:8080). Ahí ya no hay hot reload: un cambio en el source no se ve hasta reconstruir.

### Otros

Para ver los contenedores en ejecución:

```bash
docker ps
```

Para detener y borrar estos contenedores:

```bash
docker rm -f untdf-vite-dev untdf-vite-prod
```

# 02 - Nginx Volume

## Descripción

En el ejercicio `01-nginx-build` los archivos se **copian dentro de la imagen** en el momento del `docker build`. Por eso, cada cambio en `index.html` obliga a reconstruir el contenedor.

Acá el enfoque es otro: **montar un volumen** (bind mount) de la carpeta actual del host sobre el document root de Nginx (`/usr/share/nginx/html`). El contenedor no lleva una copia “congelada” de la página: sirve los archivos que están en tu disco.

Consecuencias prácticas:

- Si editás `index.html` en tu máquina, al recargar el navegador ya se ve el cambio. No hace falta volver a construir la imagen.
- El volumen **pisa** lo que Nginx trae por defecto en esa carpeta. Lo que importa en runtime es el contenido de este directorio.
- El Dockerfile de este ejemplo no copia archivos: solo parte de la imagen oficial de Nginx. El contenido lo aporta el volumen.

## Qué es el bind mount

Un *bind mount* une una ruta del host con una ruta del contenedor. En este caso:

| Host (tu máquina) | Contenedor |
| --- | --- |
| la carpeta desde la que corrés el comando (`${PWD}`) | `/usr/share/nginx/html` |

`${PWD}` es el directorio de trabajo actual. Con las comillas, la misma forma sirve en **bash/zsh (macOS, Linux, Git Bash, WSL)** y en **PowerShell (Windows)**. Si la ruta tiene espacios, las comillas evitan que el shell la parta en varios argumentos.

> En el Símbolo del sistema de Windows (`cmd.exe`) `${PWD}` no existe: ahí habría que usar `%CD%`. Con Docker Desktop lo habitual es PowerShell, donde sí funciona la línea de abajo.

## Comandos

Para construir la imagen (opcional; también podrías usar `nginx:1.30.4-trixie` directo):

```bash
docker build -t untdf-nginx-volume .
```

Para ejecutar el contenedor montando **esta carpeta** como document root (Windows, macOS y Linux):

```bash
docker run -d --name untdf-nginx-volume -p 8080:80 -v "${PWD}:/usr/share/nginx/html" untdf-nginx-volume
```

`-v "${PWD}:/usr/share/nginx/html"` lee: “tomá el directorio actual del host y montalo en el document root de Nginx”.

Abrí [http://localhost:8080](http://localhost:8080), cambiá el texto de `index.html`, guardá y recargá: deberías ver la nueva versión sin reconstruir.

Para ver los contenedores en ejecución:

```bash
docker ps
```

Para detener y borrar este contenedor:

```bash
docker rm -f untdf-nginx-volume
```

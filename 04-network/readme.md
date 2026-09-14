# 04 - Red Docker: Django + PostgreSQL (sin Compose)

## Descripción

Hasta el ejercicio 03 cada contenedor vivía solo. Acá hay **dos**, y tienen que hablarse:

| Carpeta / imagen | Rol | ¿Publica puerto al host? |
| --- | --- | --- |
| `postgres:17` | Base PostgreSQL | **No** |
| `backend/` | Django 5.2 + `runserver` | Sí (`8000`) |

La idea de este ejercicio es **no usar Compose**. Cada pieza se crea con `docker network` / `docker build` / `docker run`, con sus flags, en un orden preciso. Si te olvidás `--network` o un `-e`, Django no encuentra la base. Eso es el punto.

```
navegador  --:8000-->  untdf-django  --red untdf-net-->  untdf-db
                         (publicado)                      (Postgres, sin -p)
```

El navegador **no** está en esa red. Django sí. Por eso Django habla con Postgres por el hostname `untdf-db` (el **nombre del contenedor**). Desde tu máquina ese nombre no existe: no hace falta publicar el 5432.

Hay que levantar **primero la red, después la DB, después Django**. Django puede arrancar si Postgres todavía no acepta conexiones, pero la view va a responder 503 hasta que la base esté lista.

No hay tablas ni `migrate`: la view de `/` hace un `SELECT` a Postgres y muestra el resultado. Alcanza para comprobar que la red funciona. En el ejercicio 05 aparece el frontend, las migraciones y un tercer contenedor.

`${PWD}` es el directorio de trabajo actual. Con las comillas, la misma forma sirve en **bash/zsh (macOS, Linux, Git Bash, WSL)** y en **PowerShell (Windows)**. El `docker run` de Django hay que ejecutarlo **desde esta carpeta** (`04-network`), para que el volumen apunte a `backend/`.

## Comandos

Desde esta carpeta (`04-network`).

### 1. Crear la red

Una sola vez. En una red definida por vos, Docker resuelve el nombre de cada contenedor como hostname. En la red `bridge` por defecto eso **no** pasa.

```bash
docker network create untdf-net
```

### 2. Crear la DB

Postgres **no** publica puerto: solo lo alcanza quien esté en `untdf-net`. Las variables `POSTGRES_*` crean el usuario, la clave y la base al primer arranque. El volumen `untdf-net-pgdata` guarda los datos aunque borres el contenedor.

```bash
docker run -d --name untdf-db --network untdf-net \
  -e POSTGRES_USER=untdf \
  -e POSTGRES_PASSWORD=untdf \
  -e POSTGRES_DB=untdf \
  -v untdf-net-pgdata:/var/lib/postgresql/data \
  postgres:17
```

Postgres tarda unos segundos en aceptar conexiones. Puedes revisar si ya está listo con:

```bash
docker logs untdf-db
```


### 3. Crear Django

Construir la imagen (instala Django y `psycopg` adentro; el código se monta después):

```bash
docker build -t untdf-django-dev ./backend
```

Levantar el `runserver` **en la misma red**, con `POSTGRES_HOST=untdf-db` (el nombre del otro contenedor, no `localhost`):

```bash
docker run -d --name untdf-django --network untdf-net \
  -p 8000:8000 \
  -v "${PWD}/backend:/app" \
  -e POSTGRES_HOST=untdf-db \
  -e POSTGRES_DB=untdf \
  -e POSTGRES_USER=untdf \
  -e POSTGRES_PASSWORD=untdf \
  untdf-django-dev
```

Abrí [http://localhost:8000](http://localhost:8000). Deberías ver un JSON con `"ok": true`, el nombre de la base y la versión de PostgreSQL.

Un cambio en `backend/config/views.py` se ve sin reconstruir la imagen: el código se monta con `-v`.

## Qué pasa si la red no está

Si levantás Django **sin** `--network untdf-net`, o con `POSTGRES_HOST=localhost`, la view responde **503**: Django busca Postgres adentro de su propio contenedor. El `-p 8000:8000` no ayuda: publica Django hacia tu máquina, no a Postgres hacia Django.

Para ver el mismo JSON desde **otro contenedor** de la red (sin pasar por el host):

```bash
docker run --rm --network untdf-net curlimages/curl:8.16.0 \
  -sS http://untdf-django:8000/
```

## Otros

Para ver los contenedores en ejecución:

```bash
docker ps
```

Para detener y borrar estos contenedores, la red y el volumen de Postgres:

```bash
docker rm -f untdf-django untdf-db
docker network rm untdf-net
docker volume rm untdf-net-pgdata
```

Si ya tenés un contenedor `untdf-db` del ejercicio 05, borralo antes: el nombre tiene que estar libre.

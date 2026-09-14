# 05 - Backend, frontend y DB a mano (sin Compose)

## Descripción

En el ejercicio 04 había **dos** contenedores y una red. Acá hay **tres**, y ya no son dos Nginx estáticos:

| Carpeta / imagen | Rol | ¿Publica puerto al host? |
| --- | --- | --- |
| `postgres:17` | Base PostgreSQL (`ciudades`) | **No** |
| `backend/` | Django 5.2 + `runserver` (API JSON) | **No** |
| `frontend/` | Vite en modo desarrollo (tabla) | Sí (`5173`) |

La idea de este ejercicio es **no usar Compose**. Cada pieza se crea con `docker network` / `docker build` / `docker run`, con sus flags, en un orden preciso. Además hay que **entrar a cada carpeta**: el `Dockerfile` de Django vive en `backend/`, el de Vite en `frontend/`, y Postgres no tiene carpeta propia. Si corrés `docker build .` desde el lugar incorrecto, construís otra cosa (o nada). Eso es el punto: a mano es tedioso y fácil de equivocarse.

```
navegador  --:5173-->  untdf-front  --red untdf-app-->  untdf-api  --misma red-->  untdf-db
                         (Vite, publicado)              (Django, sin -p)           (Postgres, sin -p)
```

El navegador **no** está en esa red. El JS pide `/api/ciudades/` (mismo origen, puerto 5173). Vite, que sí ve al otro contenedor, proxifica `/api` hacia `http://untdf-api:8000`. Django habla con Postgres por el hostname `untdf-db`.

Hay que levantar **primero la red, después la DB, después la API, después el front**. Django no arranca si Postgres todavía no acepta conexiones. Vite puede arrancar sin Django, pero el `fetch` falla.

`${PWD}` es el directorio de trabajo actual. Con las comillas, la misma forma sirve en **bash/zsh (macOS, Linux, Git Bash, WSL)** y en **PowerShell (Windows)**. El volumen monta **esta carpeta** (`backend/` o `frontend/`) sobre `/app`: por eso hay que estar parados adentro antes del `docker run`.

## Comandos

### 1. Crear la red

Desde `05-back-front-manual` (o desde cualquier lado: la red no depende de una carpeta). Una sola vez:

```bash
docker network create untdf-app
```

### 2. Crear la DB

Sigue sin haber una carpeta de Postgres: se usa la imagen oficial. **No** publica puerto: solo lo alcanza quien esté en `untdf-app`. Las variables `POSTGRES_*` crean el usuario, la clave y la base al primer arranque. El volumen `untdf-pgdata` guarda los datos aunque borres el contenedor.

```bash
docker run -d --name untdf-db --network untdf-app \
  -e POSTGRES_USER=untdf \
  -e POSTGRES_PASSWORD=untdf \
  -e POSTGRES_DB=ciudades \
  -v untdf-pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:17
```

Postgres tarda unos segundos en aceptar conexiones. Si corrés el `migrate` ya, Django va a fallar. Puedes revisar con `docker logs untdf-db` o esperar a que el contenedor diga `database system is ready to accept connections`. Otra forma es usar `pg_isready` (viene en la imagen oficial)

```bash
docker run --rm --network untdf-app postgres:17 pg_isready -h untdf-db -U untdf -d ciudades
``` 


### 3. Crear la API (Django)

Entrá a la carpeta del backend. El `Dockerfile` y el código están acá; `docker build .` usa **este** contexto:

```bash
cd backend
```

Construir la imagen (instala Django y `psycopg` adentro; el código se monta después):

```bash
docker build -t untdf-api-dev .
```

Migrar (crea la tabla `ciudades` y carga Ushuaia, Río Grande y Tolhuin). Es un contenedor **de un solo uso** (`--rm`): mismas variables y misma red que el que va a quedar corriendo. Si te equivocás un `-e` acá y no en el `run` de abajo, uno funciona y el otro no.

```bash
docker run --rm --name untdf-api-migrate --network untdf-app \
  -v "${PWD}:/app" \
  -e POSTGRES_HOST=untdf-db \
  -e POSTGRES_DB=ciudades \
  -e POSTGRES_USER=untdf \
  -e POSTGRES_PASSWORD=untdf \
  -p 8000:8000 \
  untdf-api-dev python manage.py migrate
```

Levantar el `runserver` (**sin** `-p`):

```bash
docker run -d --name untdf-api --network untdf-app \
  -v "${PWD}:/app" \
  -e POSTGRES_HOST=untdf-db \
  -e POSTGRES_DB=ciudades \
  -e POSTGRES_USER=untdf \
  -e POSTGRES_PASSWORD=untdf \
  -p 8000:8000 \
  untdf-api-dev
```

Pueden obtener la api con `curl` (o Postman, o el navegador) desde **otro contenedor** en la misma red:

```bash
curl http://localhost:8000/api/ciudades/
```

### 4. Crear el front (Vite)

Salí del backend y entrá al frontend. Otro `Dockerfile`, otro contexto, otro volumen:

```bash
cd ../frontend
```

Construir la imagen:

```bash
docker build -t untdf-front-dev .
```

Instalar dependencias (quedan en esta carpeta, gracias al volumen). Alcanza con hacerlo una vez, o cuando cambie `package.json`:

```bash
docker run --rm -v "${PWD}:/app" untdf-front-dev pnpm install
```

Levantar Vite (esta sí se publica). Tiene que estar en `untdf-app` para que el proxy llegue a `untdf-api`:

```bash
docker run -d --name untdf-front --network untdf-app \
  -p 5173:5173 \
  -v "${PWD}:/app" \
  untdf-front-dev
```

Abrí [http://localhost:5173](http://localhost:5173). Deberías ver una tabla con Ushuaia, Río Grande y Tolhuin.

Un cambio en `src/App.tsx` (estando en `frontend/`) o en `ciudades/views.py` (estando en `backend/`) se ve sin reconstruir la imagen: cada contenedor monta **su** carpeta con `-v`.

## Otros

Para ver los contenedores en ejecución (da igual en qué carpeta estés):

```bash
docker ps
```

Para detener y borrar estos contenedores, la red y el volumen de Postgres:

```bash
docker rm -f untdf-front untdf-api untdf-db
docker network rm untdf-app
docker volume rm untdf-pgdata
```

Si borramos los contenedores pero **no** el volumen, la base ya tiene las migraciones: no hace falta volver a `migrate` (salvo que hayamos cambiado las migraciones).

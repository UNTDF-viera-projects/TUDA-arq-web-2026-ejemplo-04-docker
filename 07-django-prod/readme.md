# 07 - Django en producción con Gunicorn

## Descripción

En los ejercicios 04, 05 y 06 Django corre con **`runserver`** y el código se **monta con un volumen** (`-v`). Eso está bien para desarrollar: guardás un archivo y el cambio se ve sin reconstruir la imagen.

En producción no se usa `runserver`. Django se sirve con un servidor WSGI como **Gunicorn**, y el código **entra en el `docker build`** (queda copiado dentro de la imagen), igual que en el `prod.Dockerfile` de Vite del ejercicio 03.

| | Desarrollo (ejercicios 04–06) | Producción (este ejercicio) |
| --- | --- | --- |
| Servidor | `manage.py runserver` | **Gunicorn** |
| Código | bind mount (`-v …:/app`) | `COPY` en el Dockerfile |
| Un cambio en el código | se ve al instante | hay que **reconstruir** la imagen |
| `DEBUG` | suele ser `True` | **`False`** |

Este ejemplo es **aislado**: no hay Postgres ni Compose. Solo Django + Gunicorn, para ver el patrón de producción sin mezclarlo con redes ni frontend.

## Qué hace el Dockerfile

1. Parte de `python:3.12-slim`.
2. Copia `requirements.txt` e instala Django + Gunicorn.
3. Copia el resto del proyecto dentro de `/app`.
4. Arranca con:

```text
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

`config.wsgi:application` es el mismo entrypoint WSGI que Django genera en `config/wsgi.py`. Gunicorn es quien escucha el puerto; Django responde las requests.

## Comandos

Desde esta carpeta (`07-django-prod`).

### Construir la imagen

```bash
docker build -t untdf-django-prod .
```

Ese comando copia el source e instala las dependencias. No hace falta un `pip install` aparte en tu máquina.

### Ejecutar el contenedor

```bash
docker run -d --name untdf-django-prod -p 8000:8000 untdf-django-prod
```

Abrí [http://localhost:8000](http://localhost:8000). Deberías ver un JSON con `"ok": true` y `"debug": false`.

Un cambio en `config/views.py` **no se ve** hasta reconstruir: el código quedó congelado en la imagen, como el `dist/` de Vite en el ejercicio 03.

### Opcional: secret y hosts

En un entorno real pasarías variables de entorno:

```bash
docker run -d --name untdf-django-prod -p 8000:8000 \
  -e DJANGO_SECRET_KEY=una-clave-secreta \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1 \
  untdf-django-prod
```

## Otros

Para ver los contenedores en ejecución:

```bash
docker ps
```

Para detener y borrar este contenedor:

```bash
docker rm -f untdf-django-prod
```

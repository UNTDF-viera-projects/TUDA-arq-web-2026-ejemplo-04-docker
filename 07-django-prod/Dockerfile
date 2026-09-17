# #######################
# Django en producción: el código se COPIA dentro de la imagen
# (como en 03-vite-dev-prod / prod.Dockerfile) y se sirve con Gunicorn.
# No hay volumen ni runserver.
# #######################
FROM python:3.12.11-slim

ENV PYTHONUNBUFFERED=1
# DEBUG=False por defecto (ver config/settings.py)
ENV DJANGO_DEBUG=0

WORKDIR /app

# Primero las dependencias: si no cambian requirements.txt, Docker reusa esta capa.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código de la app. Queda "congelado" en la imagen.
COPY . .

EXPOSE 8000

# Gunicorn habla WSGI: config.wsgi:application es el entrypoint de Django.
# --bind 0.0.0.0:8000 escucha en todas las interfaces del contenedor.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

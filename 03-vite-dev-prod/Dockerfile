FROM node:24.20.0-slim

RUN corepack enable pnpm

# Carpeta de trabajo dentro del contenedor. Al iniciar "sesión" en el contenedor, va a estar parado en esta carpeta.
WORKDIR /app

# El código de la app no se copia acá: se monta en runtime con -v
# sobre /app (ver README.md).

EXPOSE 5173

# Comando por defecto al iniciar el contenedor.
# Equivale
CMD ["pnpm", "dev"]
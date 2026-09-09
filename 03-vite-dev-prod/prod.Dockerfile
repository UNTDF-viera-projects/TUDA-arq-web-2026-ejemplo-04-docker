# #######################
# Etapa 1: Vite necesita Node para compilar. Esta etapa no queda en la imagen final.
# #######################
FROM node:24.20.0-slim AS build

RUN corepack enable pnpm

# esto equive a
# 1. mkdir /app
# 2. cd /app
WORKDIR /app

# Copiamos el contenido del proyecto al contenedor en la carpeta /app (workidir)
COPY . .

RUN pnpm install
# genero la carpeta dist/
RUN pnpm build

# #######################
# Etapa 2: igual que el ejercicio 01, Nginx sirve archivos estáticos.
# COPY --from=build trae solo dist/, no Node ni node_modules.
# #######################
FROM nginx:1.30.4-trixie

COPY --from=build /app/dist /usr/share/nginx/html

# Documenta el puerto 80 del contenedor
EXPOSE 80

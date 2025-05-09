## crea un docker file para empaquetar esta web statica
FROM nginx:stable-alpine
# Copia el contenido de la carpeta dist a la carpeta /usr/share/nginx/html
WORKDIR /usr/share/nginx/html
COPY index.html ./
COPY entrypoint.sh ./

ENTRYPOINT [ "./entrypoint.sh" ]
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
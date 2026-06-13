FROM nginx:1.25-alpine

# Elimina la config por defecto de nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia la configuración personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia los archivos estáticos del frontend
COPY . /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

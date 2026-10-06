# Imagen base oficial de Python (versión liviana)
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el código fuente
COPY app.py .

# Puerto que utiliza la aplicación
EXPOSE 8080

# Comando que se ejecuta al iniciar el contenedor
CMD ["python", "app.py"]

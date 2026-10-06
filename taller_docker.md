# Taller Docker: crear, actualizar y ejecutar contenedores

## 1. Objetivo

Construir una imagen Docker para una aplicación HTTP en Python, ejecutarla en un contenedor, actualizarla, inspeccionarla y parametrizarla mediante una variable de entorno.

## 2. Respuestas a los conceptos y preguntas

### ¿Qué es una imagen?

Es una plantilla inmutable que contiene el código, dependencias y configuración para crear contenedores. En este taller, mi-servidor:v1 y mi-servidor:v2 son imágenes con etiquetas diferentes.

### ¿Qué es un contenedor?

Es una instancia ejecutable de una imagen. servidor1 ejecuta una imagen concreta y puede detenerse o eliminarse sin eliminar necesariamente la imagen.

### ¿Qué es un Dockerfile?

Es un archivo de texto con instrucciones para construir una imagen. En este caso define la imagen base de Python, el directorio de trabajo, el archivo que se copia, el puerto y el comando de inicio.

### ¿Qué es un registro?

Es un repositorio de imágenes. Docker Hub es el registro público predeterminado; de allí se obtiene, por ejemplo, python:3.11-slim.

### ¿Cuál es el flujo general?

~~~
Dockerfile → docker build → imagen → docker run → contenedor
~~~

### ¿Qué hacen -d, -p y --name?

- -d: ejecuta el contenedor en segundo plano.
- -p 8080:8080: conecta el puerto 8080 del host con el puerto 8080 del contenedor (HOST:CONTENEDOR).
- --name servidor1: asigna un nombre legible al contenedor.

### ¿Cuál es la diferencia entre docker stop y docker rm?

docker stop detiene el proceso de forma controlada. docker rm elimina el contenedor detenido. La imagen no se elimina con docker rm.

### ¿Por qué Docker puede reutilizar capas?

Cada instrucción del Dockerfile genera una capa. Si una instrucción y sus entradas no cambiaron, Docker usa la capa almacenada en caché y reconstruye únicamente desde el primer cambio.

### ¿Qué demuestra la variable de entorno?

Demuestra que una misma imagen puede recibir configuraciones distintas al iniciarse. La imagen permanece igual y el mensaje se define en tiempo de ejecución con -e MENSAJE=....

## 3. Prerrequisitos

El tutorial original está escrito para Ubuntu. En Windows se puede realizar con Docker Desktop y PowerShell.

Comprobar Docker:

~~~bash
docker --version
docker info
~~~

En Ubuntu, si Docker aún no está instalado:

~~~bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
~~~

## 4. Archivos del proyecto

~~~
taller_docker/
├── app.py
├── Dockerfile
└── taller_docker.md
~~~

app.py implementa un servidor HTTP en el puerto 8080. Su mensaje predeterminado corresponde a la versión actualizada y admite la variable MENSAJE.

Dockerfile usa python:3.11-slim, copia la aplicación al directorio /app y la inicia con python app.py.

## 5. Desarrollo del taller

### Paso 1: crear el proyecto

En Ubuntu:

~~~bash
mkdir -p ~/taller-docker
cd ~/taller-docker
~~~

En PowerShell:

~~~powershell
New-Item -ItemType Directory -Force taller-docker
Set-Location taller-docker
~~~

En esta entrega los archivos ya se encuentran en la carpeta del taller.

### Paso 2 y 3: crear la aplicación y el Dockerfile

Los archivos entregados son equivalentes a los solicitados en el tutorial. El código final conserva el comportamiento de la versión 2.0 y agrega la configuración opcional:

~~~python
MENSAJE = os.getenv("MENSAJE", "Hola desde Docker — versión 2.0 (actualizada)")
~~~

### Paso 4: construir la primera imagen

Para reproducir exactamente la versión 1.0, cambie temporalmente el valor predeterminado de MENSAJE en app.py a:

~~~python
MENSAJE = os.getenv("MENSAJE", "Hola desde Docker — versión 1.0")
~~~

Después ejecute:

~~~bash
docker build -t mi-servidor:v1 .
docker images mi-servidor
~~~

La opción -t asigna nombre y etiqueta; el punto indica que el contexto de construcción es la carpeta actual.

### Paso 5: ejecutar el contenedor

~~~bash
docker run -d -p 8080:8080 --name servidor1 mi-servidor:v1
~~~

### Paso 6: probar la aplicación

~~~bash
curl http://localhost:8080
~~~

Resultado esperado:

~~~
Hola desde Docker — versión 1.0
~~~

También se puede abrir http://localhost:8080 en un navegador.

### Paso 7: inspeccionar el contenedor

~~~bash
docker ps
docker logs servidor1
docker stats servidor1
~~~

docker stats actualiza los datos hasta que se cancele con Ctrl+C.

### Paso 8: actualizar el código

Cambie el mensaje predeterminado de app.py a:

~~~python
MENSAJE = os.getenv("MENSAJE", "Hola desde Docker — versión 2.0 (actualizada)")
~~~

### Paso 9: detener y eliminar el contenedor anterior

~~~bash
docker stop servidor1
docker rm servidor1
~~~

### Paso 10: construir la nueva imagen

~~~bash
docker build -t mi-servidor:v2 .
~~~

Docker reutilizará las capas que no cambiaron (FROM, WORKDIR y EXPOSE) y reconstruirá desde COPY, porque cambió app.py.

### Paso 11: ejecutar y probar la versión actualizada

~~~bash
docker run -d -p 8080:8080 --name servidor2 mi-servidor:v2
curl http://localhost:8080
docker images mi-servidor
~~~

Resultado esperado:

~~~
Hola desde Docker — versión 2.0 (actualizada)
~~~

## 6. Shell interactivo

Con servidor2 ejecutándose:

~~~bash
docker exec -it servidor2 bash
ls /app
cat /app/app.py
ps aux
exit
~~~

También se puede lanzar un contenedor temporal:

~~~bash
docker run -it --rm python:3.11-slim bash
~~~

La opción --rm elimina automáticamente ese contenedor al salir del shell.

## 7. Reto adicional: configuración por variable de entorno

El archivo app.py entregado ya contiene esta solución. Después de modificar el código, es necesario reconstruir la imagen; de lo contrario, Docker ejecutaría la versión antigua almacenada en la etiqueta anterior.

~~~bash
docker build -t mi-servidor:v3 .
docker run -d -p 8080:8080 \
  -e MENSAJE="Distribuido y contenerizado" \
  --name servidor3 mi-servidor:v3
curl http://localhost:8080
~~~

Resultado esperado:

~~~
Distribuido y contenerizado
~~~

En PowerShell, el comando equivalente en una sola línea es:

~~~powershell
docker run -d -p 8080:8080 -e "MENSAJE=Distribuido y contenerizado" --name servidor3 mi-servidor:v3
~~~

## 8. Limpieza

Si se ejecutó el reto:

~~~bash
docker stop servidor3
docker rm servidor3
~~~

Para la versión normal:

~~~bash
docker stop servidor2
docker rm servidor2
~~~

Eliminar las imágenes creadas:

~~~bash
docker rmi mi-servidor:v1 mi-servidor:v2 mi-servidor:v3
~~~

Limpiar recursos sin uso:

~~~bash
docker system prune -f
~~~

Este último comando elimina contenedores detenidos, imágenes sin uso y caché de construcción; debe usarse con cuidado.

## 9. Verificación realizada

- Docker CLI detectado: Docker version 28.1.1.
- La aplicación y el Dockerfile fueron creados en esta carpeta.
- La aplicación usa el puerto 8080 y permite configurar MENSAJE.
- La validación de docker build, docker run y curl queda pendiente de iniciar Docker Desktop, porque el motor no estaba disponible durante la ejecución:

~~~
error during connect: open //./pipe/dockerDesktopLinuxEngine:
El sistema no puede encontrar el archivo especificado.
~~~

Para terminar la validación, iniciar Docker Desktop y ejecutar los comandos de las secciones 5 a 8.


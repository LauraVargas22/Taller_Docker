# Taller Docker

Aplicación HTTP sencilla desarrollada para el taller de Docker de la asignatura **Sistemas Distribuidos — UIS**.

La aplicación se ejecuta en el puerto 8080, se empaqueta en una imagen Docker y permite cambiar el mensaje mediante la variable de entorno MENSAJE.

## Archivos

~~~
taller_docker/
├── app.py
├── Dockerfile
├── README.md
└── taller_docker.md
~~~

- app.py: servidor HTTP escrito en Python.
- Dockerfile: instrucciones para construir la imagen.
- taller_docker.md: desarrollo completo del taller, respuestas y explicación de cada paso.

## Requisitos

- Docker Desktop en Windows, macOS o Linux.
- Docker Engine activo.

Verificar la instalación:

~~~bash
docker --version
docker info
~~~

## Construir la imagen

Desde la carpeta del proyecto:

~~~bash
docker build -t mi-servidor:v2 .
~~~

## Ejecutar el contenedor

~~~bash
docker run -d -p 8080:8080 --name servidor2 mi-servidor:v2
~~~

Probar la aplicación:

~~~bash
curl http://localhost:8080
~~~

Respuesta esperada:

~~~
Hola desde Docker — versión 2.0 (actualizada)
~~~

También puede abrirse en el navegador: http://localhost:8080

## Usar una variable de entorno

Construir y ejecutar una versión parametrizada:

~~~bash
docker build -t mi-servidor:v3 .
docker run -d -p 8080:8080 \
  -e MENSAJE="Distribuido y contenerizado" \
  --name servidor3 mi-servidor:v3
~~~

En PowerShell:

~~~powershell
docker run -d -p 8080:8080 -e "MENSAJE=Distribuido y contenerizado" --name servidor3 mi-servidor:v3
~~~

## Inspección

~~~bash
docker ps
docker logs servidor2
docker exec -it servidor2 bash
~~~

Dentro del contenedor:

~~~bash
ls /app
cat /app/app.py
exit
~~~

## Detener y limpiar

~~~bash
docker stop servidor2
docker rm servidor2
docker rmi mi-servidor:v1 mi-servidor:v2 mi-servidor:v3
~~~

## Documentación completa

Consulte [taller_docker.md](taller_docker.md) para ver:

- respuestas a los conceptos del taller;
- construcción de las versiones v1 y v2;
- explicación de los comandos Docker;
- reto de configuración por variable de entorno;
- verificación y limpieza del entorno.


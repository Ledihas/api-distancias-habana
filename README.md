# API de Distancias - La Habana 🚗

## Descripción
API REST que proporciona las distancias por carretera entre diferentes municipios de La Habana y otras localidades de Cuba. Utiliza procesamiento de lenguaje natural (NLP) a través de Wit.ai para interpretar las consultas de los usuarios y calcular desvíos en las rutas.

## Características ✨
- Consulta de distancias entre municipios de La Habana
- Procesamiento de lenguaje natural para consultas en formato libre
- Soporte para nombres de ubicaciones en mayúsculas y minúsculas
- Respuestas en formato JSON con distancias en kilómetros
- Base de datos con más de 80 ubicaciones en La Habana
- Cálculo automático de distancias usando coordenadas GPS
- Incremento del 30% en la distancia base para compensar rutas indirectas
- Cálculo de desvíos con incremento del 40% en la distancia
- Soporte para coordenadas GPS directas en formato latitud,longitud

## Tecnologías Utilizadas 🛠️
- Python 3.12
- Flask
- Wit.ai para NLP
- Requests para llamadas HTTP
- Python-dotenv para variables de entorno
- Gunicorn (para producción)

## Instalación 📦

1. Clona el repositorio:
```bash
git clone https://github.com/Ledihas/api-distancias-habana.git
```

2. Instala las dependencias:
```bash
cd api-distancias-habana
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita el archivo .env con tu token de Wit.ai
```

## Uso 🚀

### Ejecutar localmente
```bash
python app/app.py
```

### Endpoints

#### GET /
- Verifica si el servicio está activo
- Respuesta: "El servicio está vivo!"


#### GET /enviar
- Parámetros:
  - string1: Lugar de origen
  - string2: Lugar de destino
- Ejemplo de respuesta exitosa:
```json
{
    "distancia": 12.34,
    "coordenadas1": [23.123456, -82.123456],
    "coordenadas2": [23.123456, -82.123456]
}
```

#### GET /desviacion
- Parámetros:
  - string1: Coordenadas de origen (formato: "latitud,longitud")
  - string2: Coordenadas de destino (formato: "latitud,longitud")
  - string3: Lugar del desvío
- Ejemplo de respuesta exitosa:
```json
{
    "distancia": 15.45
}
```



## Estructura del Proyecto 📁
```
api-distancias-habana/
├── app/
│   ├── app.py         # Aplicación principal Flask
│   └── direcciones.py # Base de datos de coordenadas
├── requirements.txt   # Dependencias del proyecto
├── wsgi.py           # Punto de entrada para Gunicorn
├── .env              # Variables de entorno
└── README.md         # Documentación
```

## Variables de Entorno 🔐
- `WIT_AI_TOKEN`: Token de autenticación para Wit.ai
- `PORT`: Puerto para el servidor (por defecto: 5000)

## Base de Datos de Ubicaciones 🗺️
El proyecto incluye una extensa base de datos de coordenadas GPS para:
- 15 municipios de La Habana
- Más de 80 barrios y localidades
- Soporte para nombres alternativos de ubicaciones
- Coordenadas precisas en formato (latitud, longitud)

## Contribuir 🤝
Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## Licencia 📄
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor ✒️
- Ledihas - [Ledihas](https://github.com/Ledihas)

## Ejemplos de Uso 🚀

### Consultar Distancia

**Solicitud:**
```bash
GET /enviar?string1=La%20Lisa&string2=Alamar
```

**Respuesta:**
```json
{
    "distancia": 12.34,
    "coordenadas1": [23.123456, -82.123456],
    "coordenadas2": [23.654321, -82.654321]
}
```

### Manejo de Errores

- **Error 400**: Coordenadas incompletas o inválidas.
- **Error 500**: Problema interno del servidor.

## Contribuir 🤝

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer. Asegúrate de seguir las pautas de estilo y de incluir pruebas para cualquier nueva funcionalidad.

## Licencia 📄

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Estado del Proyecto

Este proyecto está actualmente en desarrollo y se están planificando nuevas características para mejorar la funcionalidad.

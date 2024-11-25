# API de Distancias - La Habana 🚗

## Descripción
API REST que proporciona las distancias por carretera entre diferentes municipios de La Habana y otras localidades de Cuba. Utiliza procesamiento de lenguaje natural (NLP) a través de Wit.ai para interpretar las consultas de los usuarios.

## Características ✨
- Consulta de distancias entre municipios de La Habana
- Consulta de distancias entre La Habana y otras ciudades de Cuba
- Procesamiento de lenguaje natural para consultas en formato libre
- Respuestas en formato JSON

## Tecnologías Utilizadas 🛠️
- Python 3.9
- Flask
- Wit.ai
- Gunicorn
- Docker (opcional)

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
```


# Edita el archivo .env con tu token de Wit.ai


### Ejecutar localmente
```bash

python app/app.py
```



## Estructura del Proyecto 📁

```

distancias-habana-api/
├── app/
│ └── app.py
├── requirements.txt
├── wsgi.py
├── .env
└── README.md
```


## API Endpoints 🛣️

### GET /
- Verifica si el servicio está activo
- Respuesta: "El servicio está vivo!"

### GET /enviar
- Parámetros:
  - string1: Lugar de origen
  - string2: Lugar de destino
- Respuesta: Distancia en kilómetros entre los lugares especificados

## Despliegue 🌐
El proyecto está configurado para ser desplegado en Render.com. Ver la [documentación de despliegue](https://render.com/docs) para más detalles.

## Variables de Entorno 🔐
- `WIT_AI_TOKEN`: Token de autenticación para Wit.ai
- `PORT`: Puerto para el servidor (por defecto: 5000)

## Contribuir 🤝
Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## Licencia 📄
Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor ✒️
- Ledihas - [Ledihas](https://github.com/Ledihas)

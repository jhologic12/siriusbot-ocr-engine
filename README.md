# SiriusBot OCR Engine

Microservicio de procesamiento inteligente de imágenes para extracción de información mediante OCR, desarrollado como parte de la plataforma **SiriusBot**.

El servicio recibe imágenes de documentos como facturas, recibos y documentos administrativos, ejecuta validaciones de seguridad, validación de imagen, preprocesamiento, análisis de calidad y extracción de texto mediante OCR.

El resultado se entrega mediante una API REST con respuestas JSON estandarizadas, manejo centralizado de errores, métricas y trazabilidad mediante Request ID.

---

## Estado del proyecto

**Estado:** En desarrollo activo 🚧

El proyecto cuenta actualmente con:

* API REST funcional con FastAPI
* Pipeline completo de procesamiento OCR
* Validaciones de seguridad de archivos e imágenes
* Preprocesamiento de imágenes
* Análisis de calidad
* Protección contra tiempos de procesamiento excesivos
* Manejo estandarizado de errores
* Logging estructurado
* Métricas internas
* Telemetría
* Request ID para trazabilidad
* Tests unitarios e integración
* GitHub Actions para CI
* Dockerización

### Calidad actual

```text
Tests:       84 passed
Cobertura:   84%
CI:          GitHub Actions
Estado:      main estable
```

---

# Características principales

* API REST desarrollada con **FastAPI**
* Python 3.12
* Procesamiento de imágenes con **Pillow**
* Motor OCR basado en Tesseract
* Validación de archivos de entrada
* Validación de contenido de imágenes
* Detección de imágenes inválidas o corruptas
* Validación de dimensiones de imágenes
* Límite de tamaño de archivos
* Preprocesamiento de imágenes
* Análisis de calidad de imagen
* Pipeline de procesamiento configurable
* Respuestas JSON estandarizadas
* Serialización consistente mediante aliases `camelCase`
* Manejo centralizado de excepciones
* Logging estructurado
* Métricas internas de procesamiento
* Telemetría
* Request ID para trazabilidad
* Protección contra timeout de procesamiento OCR
* Contenerización con Docker
* Pruebas unitarias
* Pruebas de integración de API
* Cobertura de código con Pytest
* Integración continua mediante GitHub Actions

---

# Arquitectura del servicio

```text
                         Cliente
                            |
                            | POST /api/v1/ocr
                            v
                  +---------------------+
                  |       FastAPI       |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Observability       |
                  | Middleware          |
                  |                     |
                  | Request ID          |
                  | Logging             |
                  | Métricas            |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Request Security    |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | File Security       |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Image Validation    |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Image Security      |
                  | Dimensions / Size   |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Preprocessor        |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Quality Analysis    |
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | OCR Engine          |
                  | + Timeout Protection|
                  +---------------------+
                            |
                            v
                  +---------------------+
                  | Response Builder    |
                  +---------------------+
                            |
                            v
                     JSON Response
```

---

# Tecnologías utilizadas

## Backend

* Python 3.12
* FastAPI
* Uvicorn
* Pydantic

## Procesamiento de imágenes

* Pillow
* Tesseract OCR

## Testing

* Pytest
* pytest-cov
* FastAPI TestClient
* AnyIO

## Calidad y desarrollo

* Git
* GitHub
* GitHub Actions

## Infraestructura

* Docker
* Docker Compose
* Linux / WSL

---

# Estructura del proyecto

```text
ocr-engine/
│
├── app.py
├── config.py
├── Dockerfile
├── requirements.txt
├── pytest.ini
│
├── models/
│   ├── request_models.py
│   └── response_models.py
│
├── services/
│   ├── ocr.py
│   ├── ocr_pipeline.py
│   ├── file_security.py
│   ├── image_security.py
│   ├── validator.py
│   ├── preprocessor.py
│   ├── quality.py
│   └── response_builder.py
│
├── utils/
│   ├── constants.py
│   ├── exceptions.py
│   ├── error_handlers.py
│   ├── middleware.py
│   ├── telemetry.py
│   ├── metrics.py
│   ├── logger.py
│   ├── request_context.py
│   └── request_security.py
│
└── tests/
    ├── test_app.py
    ├── test_ocr.py
    ├── test_validator.py
    ├── test_health.py
    ├── test_metrics.py
    ├── test_middleware.py
    └── ...
```

---

# Instalación local

## Clonar repositorio

```bash
git clone https://github.com/jhologic12/siriusbot-ocr-engine.git

cd siriusbot-ocr-engine
```

## Crear entorno virtual

Linux / WSL:

```bash
python3 -m venv .venv
```

Activar:

```bash
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\activate
```

## Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

---

# Ejecutar aplicación

Iniciar el servidor:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Servicio disponible en:

```text
http://localhost:8000
```

---

# API

La API utiliza el prefijo:

```text
/api/v1
```

## Health Check

```http
GET /api/v1/health
```

Ejemplo:

```bash
curl http://localhost:8000/api/v1/health
```

Respuesta:

```json
{
    "status": "healthy",
    "service": "siriusbot-ocr-engine"
}
```

---

## Readiness

```http
GET /api/v1/ready
```

Ejemplo:

```bash
curl http://localhost:8000/api/v1/ready
```

Respuesta:

```json
{
    "status": "ready"
}
```

---

## Métricas

```http
GET /api/v1/metrics
```

Este endpoint permite consultar métricas internas del servicio, incluyendo:

* Peticiones recibidas
* Peticiones exitosas
* Peticiones fallidas
* Procesamientos OCR exitosos
* Procesamientos OCR fallidos
* Tiempo total de peticiones
* Tiempo total de procesamiento
* Tiempo promedio de procesamiento
* Uptime del servicio
* Métricas de error personalizadas

Ejemplo:

```bash
curl http://localhost:8000/api/v1/metrics
```

---

# Procesamiento OCR

## Endpoint

```http
POST /api/v1/ocr
```

El endpoint recibe una imagen mediante `multipart/form-data`.

Ejemplo:

```bash
curl -X POST \
  -F "file=@factura.jpg" \
  http://localhost:8000/api/v1/ocr
```

---

# Respuesta OCR

Ejemplo de respuesta exitosa:

```json
{
    "success": true,
    "validation": {
        "valid": true,
        "errors": [],
        "warnings": [],
        "metadata": {
            "format": "JPEG",
            "mode": "RGB",
            "width": 1000,
            "height": 1000,
            "pixels": 1000000,
            "sizeBytes": 16503
        }
    },
    "quality": {
        "status": "GOOD",
        "canProcess": true,
        "width": 1200,
        "height": 1200,
        "pixels": 1440000,
        "brightness": 128.5,
        "contrast": 45.2,
        "warnings": []
    },
    "processing": {
        "processed": true,
        "originalSize": 16503,
        "newSize": 8721,
        "width": 1200,
        "height": 1200
    },
    "ocr": {
        "text": "Factura número 12345",
        "confidence": 0.94
    },
    "message": "Proceso completado",
    "error": null
}
```

> Los valores de la respuesta dependen de la imagen procesada.

---

# Validaciones y seguridad

El Engine incorpora diferentes capas de validación antes de ejecutar OCR.

### Seguridad del archivo

* Validación del tipo de archivo
* Validación del contenido
* Restricción de tamaño
* Validación del nombre del archivo

### Seguridad de imagen

* Validación de imagen válida
* Detección de imágenes corruptas
* Validación de dimensiones
* Protección contra imágenes excesivamente grandes

### Calidad

El sistema analiza características como:

* Brillo
* Contraste
* Dimensiones
* Cantidad de píxeles
* Advertencias de calidad

Cuando la imagen no cumple las condiciones necesarias, el pipeline puede rechazar el procesamiento.

---

# Manejo de errores

El servicio utiliza excepciones y respuestas estandarizadas.

Ejemplo:

```json
{
    "success": false,
    "error": {
        "code": "INVALID_IMAGE",
        "message": "Imagen inválida"
    }
}
```

Algunos códigos utilizados:

```text
INVALID_IMAGE
FILE_SECURITY_ERROR
IMAGE_SECURITY_ERROR
LOW_IMAGE_QUALITY
OCR_PROCESSING_ERROR
OCR_TIMEOUT
OCR_EXCEPTION
```

Los errores controlados son transformados por handlers globales en respuestas HTTP consistentes.

---

# Observabilidad

El servicio incorpora una capa básica de observabilidad.

## Request ID

Cada petición recibe un identificador único:

```text
X-Request-ID
```

Ejemplo:

```text
X-Request-ID: 05d4f0b2-cc53-4b10-b0cb-7379c4f29826
```

Esto permite relacionar una petición HTTP con los logs generados durante su procesamiento.

## Logging

Se registran eventos como:

```text
request_started
request_completed
request_failed
```

Incluyendo información como:

* Request ID
* Método HTTP
* Ruta
* Código de respuesta
* Duración de la petición

---

# Métricas

El Engine mantiene métricas internas para observar el comportamiento del servicio.

Métricas principales:

```text
requests_total
requests_success
requests_failed

ocr_success
ocr_failed

total_request_time
total_processing_time

uptime_seconds
average_processing_time
```

También permite registrar métricas personalizadas relacionadas con errores y procesamiento.

---

# Protección contra timeout

El procesamiento OCR cuenta con protección frente a ejecuciones que excedan el tiempo máximo configurado.

Cuando se supera el límite establecido, el servicio puede generar:

```text
OCR_TIMEOUT
```

y responder con HTTP:

```text
504 Gateway Timeout
```

El objetivo es evitar que una operación OCR problemática bloquee indefinidamente el procesamiento de una petición.

---

# Testing

El proyecto cuenta con una suite automatizada de pruebas unitarias y de integración.

Ejecutar todas las pruebas:

```bash
python -m pytest -q
```

Ejecutar con información detallada:

```bash
python -m pytest -v
```

Ejecutar un archivo específico:

```bash
python -m pytest tests/test_app.py -v
```

## Estado actual

```text
84 passed
84% coverage
```

Las pruebas cubren diferentes componentes del sistema:

* API
* Health checks
* Readiness
* Endpoint OCR
* Integración de endpoints
* Validación de archivos
* Validación de imágenes
* Preprocesamiento
* Análisis de calidad
* OCR
* Excepciones
* Middleware
* Request ID
* Logging
* Telemetría
* Métricas
* Manejo de errores

---

# Integración continua

El repositorio utiliza **GitHub Actions** para ejecutar automáticamente las validaciones del proyecto.

Flujo de trabajo:

```text
Feature Branch
      |
      v
    Commit
      |
      v
     Push
      |
      v
 Pull Request
      |
      v
GitHub Actions
      |
      +---- Tests
      |
      +---- Coverage
      |
      +---- Validaciones
      |
      v
    Merge
      |
      v
    main
```

Las funcionalidades se desarrollan mediante ramas independientes y posteriormente se integran mediante Pull Requests.

---

# Docker

## Construir imagen

```bash
docker build -t siriusbot-ocr-engine .
```

## Ejecutar contenedor

```bash
docker run -p 8000:8000 siriusbot-ocr-engine
```

El servicio estará disponible en:

```text
http://localhost:8000
```

---

# Flujo de desarrollo

El proyecto utiliza Git Flow basado en ramas de funcionalidades.

Ejemplo:

```bash
git switch main

git pull --ff-only origin main

git switch -c feature/nueva-funcionalidad
```

Después de implementar y probar:

```bash
git add .

git commit -m "feat: nueva funcionalidad"

git push -u origin feature/nueva-funcionalidad
```

Posteriormente se crea un Pull Request hacia `main`.

El merge se realiza después de comprobar las pruebas y validaciones de CI.

---

# Roadmap

## Fase 1 — Base del microservicio ✅

* API REST
* Endpoint OCR
* Pipeline de procesamiento
* Validación de imágenes
* Preprocesamiento
* Análisis de calidad
* Motor OCR
* Respuestas estandarizadas
* Dockerización
* Testing automatizado

## Fase 1.5 — Seguridad de entrada ✅

* Validación de archivos
* Validación de contenido
* Límite de tamaño
* Validación de dimensiones
* Protección de imágenes excesivamente grandes
* Validación de solicitudes

## Fase 1.6 — Resiliencia ✅

* Protección contra timeout OCR
* Manejo centralizado de excepciones
* Respuestas HTTP estandarizadas

## Fase 1.7 — Observabilidad ✅

* Logging estructurado
* Request ID
* Middleware global
* Telemetría
* Métricas internas
* Endpoint `/api/v1/metrics`

## Fase 1.8 — Integración y calidad ✅

* Tests unitarios
* Tests de integración
* Cobertura automatizada
* GitHub Actions
* Validación mediante Pull Requests

## Próximas fases 🚧

* Clasificación automática de documentos
* Extracción estructurada de facturas
* Extracción de campos específicos
* Integración con SiriusBot
* Persistencia de resultados
* Modelos de IA para comprensión documental
* API de autenticación
* Rate limiting
* Observabilidad avanzada
* Métricas compatibles con sistemas externos
* Despliegue en infraestructura cloud

---

# Proyecto relacionado

Este microservicio forma parte del ecosistema **SiriusBot**.

SiriusBot tiene como objetivo proporcionar una plataforma de automatización para la gestión inmobiliaria mediante agentes conversacionales, procesamiento documental, OCR y servicios de inteligencia artificial.

El OCR Engine está diseñado como un microservicio independiente para permitir su evolución, despliegue y escalamiento de manera desacoplada.

---

# Autor

**Jhon Alexander Ospino Figueroa**

Software Engineer

GitHub:

https://github.com/jhologic12

---

# Licencia

Proyecto privado / desarrollo personal.

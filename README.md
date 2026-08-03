# SiriusBot OCR Engine

Microservicio de procesamiento inteligente de imágenes para extracción de información OCR desarrollado para la plataforma **SiriusBot**.

Este servicio recibe imágenes de documentos (facturas, recibos y documentos administrativos), realiza validación, preprocesamiento, análisis de calidad y extracción de texto mediante OCR, entregando una respuesta estructurada para ser consumida por otros servicios.

---

##  Características principales

- API REST desarrollada con **FastAPI**
- Procesamiento de imágenes con **Pillow**
- Motor OCR para extracción de texto
- Validación de archivos de entrada
- Detección de imágenes corruptas
- Análisis de calidad de imagen
- Pipeline de procesamiento configurable
- Respuestas estandarizadas en JSON
- Manejo centralizado de errores
- Logging estructurado
- Métricas básicas de procesamiento
- Request ID para trazabilidad
- Contenerización con Docker
- Suite completa de pruebas automatizadas con Pytest

---

# Arquitectura del servicio

```
                    Cliente
                       |
                       |
                  POST /ocr
                       |
                       v
              +----------------+
              |    FastAPI     |
              +----------------+
                       |
                       v
              Validación imagen
                       |
                       v
              Preprocesamiento
                       |
                       v
              Análisis calidad
                       |
                       v
                 OCR Engine
                       |
                       v
              Respuesta JSON
```

---

# Tecnologías utilizadas

## Backend

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic

## Procesamiento de imágenes

- Pillow
- OCR Engine

## Testing

- Pytest
- FastAPI TestClient

## Infraestructura

- Docker
- Docker Compose

---

# Estructura del proyecto

```
ocr-engine/
│
├── app.py                    # API principal FastAPI
├── config.py                 # Configuración del servicio
├── Dockerfile                # Imagen Docker
├── requirements.txt          # Dependencias Python
├── pytest.ini                # Configuración pruebas
│
├── models/
│   ├── request_models.py
│   ├── response_models.py
│   └── response_builder.py
│
├── services/
│   ├── ocr.py                # Motor OCR
│   ├── validator.py          # Validación imágenes
│   ├── preprocessor.py       # Preparación imagen
│   ├── quality.py            # Análisis calidad
│   └── response_builder.py
│
├── utils/
│   ├── exceptions.py
│   ├── error_handlers.py
│   ├── middleware.py
│   ├── telemetry.py
│   ├── metrics.py
│   └── logger.py
│
└── tests/
    ├── test_app.py
    ├── test_ocr.py
    ├── test_validator.py
    └── ...
```

---

# Instalación local

## Clonar repositorio

```bash
git clone https://github.com/jhologic12/siriusbot-ocr-engine.git

cd siriusbot-ocr-engine
```

---

## Crear entorno virtual

```bash
python -m venv venv
```

Activar:

Linux / WSL:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecutar aplicación

Iniciar servidor:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Servicio disponible:

```
http://localhost:8000
```

---

# Endpoint principal

## Procesar imagen OCR

### POST

```
/ocr
```

Ejemplo:

```bash
curl -X POST \
-F "file=@factura.jpg" \
http://localhost:8000/ocr
```

---

# Respuesta exitosa

Ejemplo:

```json
{
    "success": true,
    "message": "OCR procesado correctamente",
    "ocr": {
        "text": "Factura número 12345"
    },
    "processing": {
        "processed": true
    }
}
```

---

# Validaciones implementadas

El servicio valida:

- Tipo de archivo permitido
- Imagen corrupta
- Dimensiones mínimas
- Calidad de imagen
- Capacidad de procesamiento OCR

Ejemplo error:

```json
{
    "success": false,
    "error": {
        "code": "INVALID_IMAGE",
        "message": "Imagen inválida"
    }
}
```

---

# Testing

Ejecutar pruebas:

```bash
pytest tests -v
```

Estado actual:

```
55 passed
```

Cobertura:

- API
- OCR
- Validadores
- Preprocesamiento
- Calidad
- Excepciones
- Middleware
- Telemetría
- Métricas

---

# Docker

Construir imagen:

```bash
docker build -t siriusbot-ocr-engine .
```

Ejecutar:

```bash
docker run -p 8000:8000 siriusbot-ocr-engine
```

---

# Roadmap

## Fase 1 - Base del microservicio ✅

- API OCR
- Validación imágenes
- Pipeline procesamiento
- Testing completo
- Dockerización

## Fase 1.8 - Seguridad de entrada 🚧

Próximas mejoras:

- Validación MIME real
- Límite tamaño archivos
- Protección contra payloads maliciosos
- Sanitización nombres archivos
- Timeouts procesamiento
- Rate limiting

## Futuras fases

- Clasificación automática documentos
- Extracción estructurada de facturas
- Integración con SiriusBot
- Modelos IA para comprensión documental
- Persistencia de resultados

---

# Proyecto relacionado

Este microservicio forma parte del ecosistema:

**SiriusBot**

Plataforma inteligente para automatización de gestión inmobiliaria mediante agentes conversacionales, OCR y servicios de IA.

---

# Autor

**Jhon Alexander Ospino Figueroa**

Software Engineer

GitHub:
https://github.com/jhologic12

---

# Licencia

Proyecto privado / desarrollo personal.
# Estimación de Tiempos de Producción - MVP

Sistema MVP para procesar estudios de tiempos en maquilas textiles y generar estimaciones de capacidad productiva.

## 🎯 Descripción

Esta aplicación Django procesa archivos Excel con datos de estudios de tiempo (time-study) y calcula métricas estandarizadas de producción por operación. El sistema NO agrupa operaciones por operador, preservando cada operación como una línea independiente para análisis detallado.

## ✨ Características

- **API REST** para procesamiento programático de archivos
- **Interfaz web simple** con drag & drop para cargar archivos
- **Validación robusta** de formato y datos
- **Cálculos determinísticos** basados en estándares industriales:
  - Tiempo promedio observado
  - Tiempo estándar (con suplemento)
  - Unidades por hora objetivo
  - Unidades por día objetivo
- **Manejo de errores** con mensajes claros
- **Salida en Excel** con formato profesional

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd estimate_production_times
```

### 2. Activar el entorno virtual

```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias (si no están instaladas)

```bash
pip install django djangorestframework pandas openpyxl
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

## 📊 Formato del Archivo Excel

El archivo Excel debe contener las siguientes columnas obligatorias:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| **Operador** | Nombre del operador | Juan Pérez |
| **Operación** | Nombre/descripción de la operación | Coser manga izquierda |
| **Máquina** | Tipo de máquina utilizada | Overlock |
| **Tiempo 1, Tiempo 2, ...** | Mediciones cronométricas en segundos | 45.2, 46.1, 44.8 |
| **Suplemento** | Porcentaje de suplemento/tolerancia | 15 |

### Ejemplo de estructura:

```
Operador       | Operación              | Máquina          | Tiempo 1 | Tiempo 2 | Tiempo 3 | Suplemento
---------------|------------------------|------------------|----------|----------|----------|------------
Juan Pérez     | Cortar tela            | Cortadora        | 45.2     | 46.1     | 44.8     | 15
María García   | Coser manga izquierda  | Overlock         | 62.5     | 63.2     | 61.9     | 20
```

### Generar archivo de ejemplo

```bash
python generate_sample.py
```

Esto creará `sample_time_study.xlsx` con datos de prueba.

## 🔧 Uso

### Opción 1: Interfaz Web

1. Abrir navegador en `http://127.0.0.1:8000/`
2. Arrastrar archivo Excel o hacer clic para seleccionar
3. Hacer clic en "Procesar Archivo"
4. El archivo procesado se descargará automáticamente

### Opción 2: API REST

**Endpoint:** `POST /api/process-time-study/`

**Headers:**
```
Content-Type: multipart/form-data
```

**Body:**
- `file`: Archivo Excel (.xlsx)

**Ejemplo con cURL:**

```bash
curl -X POST http://127.0.0.1:8000/api/process-time-study/ \
  -F "file=@sample_time_study.xlsx" \
  --output resultado.xlsx
```

**Ejemplo con Python:**

```python
import requests

url = 'http://127.0.0.1:8000/api/process-time-study/'
files = {'file': open('sample_time_study.xlsx', 'rb')}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open('resultado.xlsx', 'wb') as f:
        f.write(response.content)
    print("Archivo procesado exitosamente")
else:
    print(f"Error: {response.json()}")
```

## 📤 Formato de Salida

El archivo Excel generado contiene las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| **Operador** | Nombre del operador (preservado) |
| **Operación** | Nombre de la operación |
| **Máquina** | Tipo de máquina |
| **Tiempo Promedio (seg)** | Promedio de todas las mediciones |
| **Suplemento (%)** | Porcentaje de suplemento aplicado |
| **Tiempo Estándar (seg)** | Tiempo promedio × (1 + suplemento/100) |
| **Tiempo Estándar (min)** | Tiempo estándar en minutos |
| **Unidades/Hora** | 3600 / tiempo estándar (segundos) |
| **Unidades/Día** | Unidades/Hora × horas laborales por día |

## ⚙️ Configuración

Puedes modificar la configuración en `production_estimator/settings.py`:

```python
TIME_ESTIMATION_CONFIG = {
    'WORKING_HOURS_PER_DAY': 8,      # Horas laborales por día
    'MAX_FILE_SIZE_MB': 10,           # Tamaño máximo de archivo
    'ALLOWED_EXTENSIONS': ['.xlsx'],  # Extensiones permitidas
}
```

## 🔍 Validaciones y Errores

El sistema valida:

- ✅ Formato de archivo (.xlsx únicamente)
- ✅ Tamaño de archivo (máximo 10MB por defecto)
- ✅ Presencia de columnas obligatorias
- ✅ Presencia de al menos una columna de tiempo
- ✅ Valores numéricos en mediciones de tiempo
- ✅ Al menos una medición válida por operación

### Mensajes de error comunes:

| Error | Causa | Solución |
|-------|-------|----------|
| "Invalid file format" | Archivo no es .xlsx | Usar formato Excel .xlsx |
| "Missing required columns" | Faltan columnas obligatorias | Verificar nombres de columnas |
| "No time measurement columns found" | No hay columnas de tiempo | Agregar columnas "Tiempo 1", "Tiempo 2", etc. |
| "No valid time measurements" | Valores no numéricos en tiempos | Asegurar que tiempos sean números |

## 🏗️ Arquitectura

```
estimate_production_times/
├── production_estimator/      # Proyecto Django principal
│   ├── settings.py           # Configuración
│   └── urls.py               # URLs principales
├── time_estimator/           # Aplicación Django
│   ├── services.py           # Lógica de negocio (capa de servicios)
│   ├── views.py              # Vistas API y web
│   ├── serializers.py        # Serializadores REST
│   ├── urls.py               # URLs de la app
│   └── templates/            # Plantillas HTML
│       └── time_estimator/
│           └── upload.html   # Interfaz web
├── manage.py                 # Script de gestión Django
├── generate_sample.py        # Generador de archivo de ejemplo
└── README.md                 # Esta documentación
```

### Principios de diseño:

- **Separación de responsabilidades**: Lógica de negocio aislada en `services.py`
- **Manejo robusto de errores**: Excepciones personalizadas y validaciones múltiples
- **Configuración centralizada**: Variables de configuración en settings
- **API y UI desacopladas**: Misma lógica, diferentes interfaces
- **Sin estado**: Procesamiento determinístico sin almacenamiento

## 🧪 Pruebas

### Prueba rápida:

```bash
# Generar archivo de ejemplo
python generate_sample.py

# Iniciar servidor
python manage.py runserver

# Abrir navegador en http://127.0.0.1:8000/
# Cargar sample_time_study.xlsx
```

## 📝 Notas Importantes

### ¿Por qué NO se agrupan operaciones por operador?

Aunque un operador pueda realizar múltiples operaciones, el sistema mantiene cada operación como una fila independiente porque:

1. **Flexibilidad de análisis**: Permite análisis detallado por operación
2. **Trazabilidad**: Cada operación tiene su propio tiempo estándar y métricas
3. **Extensibilidad futura**: Facilita agregar balanceo de líneas, análisis de cuellos de botella, etc.
4. **Realismo operacional**: Las operaciones pueden redistribuirse entre operadores

### Limitaciones del MVP:

- ❌ No implementa machine learning
- ❌ No simula líneas de producción
- ❌ No optimiza balance de cargas
- ❌ No maneja secuencias de operaciones
- ✅ Solo cálculos determinísticos basados en datos de entrada

## 🔐 Consideraciones de Producción

Para desplegar en producción:

1. **Cambiar SECRET_KEY** en settings.py
2. **Establecer DEBUG = False**
3. **Configurar ALLOWED_HOSTS**
4. **Usar base de datos real** (PostgreSQL, MySQL)
5. **Configurar archivos estáticos** con whitenoise o servidor web
6. **Agregar autenticación** si es necesario
7. **Implementar logging** estructurado
8. **Configurar HTTPS** y certificados SSL

## 📧 Soporte

Para problemas o preguntas:
- Revisar los logs del servidor
- Verificar el formato del archivo Excel
- Consultar la sección de errores comunes

## 📄 Licencia

Este es un proyecto MVP para uso interno de la maquila.

---

**Versión:** 1.0.0  
**Última actualización:** Enero 2026

# AguaSur - Sistema de Gestión Comunitaria del Agua 💧

Sistema open source para optimizar la distribución y gestión del agua en comunidades con acceso limitado al recurso hídrico. Desarrollado para la Zona Sud de Cochabamba, Bolivia.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Problemática

La Zona Sud de Cochabamba enfrenta una crisis grave de agua:
- ❌ Escasez crónica de agua potable
- ❌ Acceso desigual al recurso
- ❌ Dependencia de cisternas y pipas de agua costosas
- ❌ Falta de coordinación comunitaria
- ❌ Riesgos sanitarios por agua no segura
- ❌ Ausencia de datos para toma de decisiones

## 💡 Solución: AguaSur

AguaSur es un sistema que **optimiza la gestión del recurso existente** mediante:

✅ **Registro de familias** y sus necesidades de agua  
✅ **Monitoreo en tiempo real** de cisternas (nivel, capacidad, ubicación)  
✅ **Predicción de consumo** y alertas tempranas  
✅ **Sistema de reportes** para problemas y solicitudes  
✅ **Dashboard con estadísticas** para la OTB  
✅ **Coordinación de compras comunitarias** de agua  
✅ **Mapa interactivo** de fuentes de agua disponibles  


## 🚀 Características Principales

### 📋 Gestión de Familias
- Registro de hogares con datos de consumo
- Cálculo automático de necesidades de agua
- Identificación de familias en situación crítica
- Contacto directo (Telegram/WhatsApp)

### 💧 Monitoreo de Cisternas
- Seguimiento de nivel de agua en tiempo real
- Alertas de nivel crítico (< 20%)
- Predicción de días de autonomía
- Priorización automática (escuelas, centros de salud)
- Geolocalización de cisternas

### 📊 Gestión de Llenados
- Registro de proveedores y costos
- Historial completo de llenados
- Cálculo de costo promedio por litro
- Optimización de gastos compartidos

### 🚨 Sistema de Reportes
- Reportes de emergencia (agua acabándose, contaminada)
- Niveles de urgencia (baja, media, alta, crítica)
- Seguimiento de estado (pendiente, en proceso, resuelto)
- Geolocalización de problemas

### 📈 Dashboard y Estadísticas
- Estadísticas en tiempo real
- Alertas automáticas
- Reportes para la OTB
- Indicadores de impacto

---

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

**Backend:**
- Python 3.12+
- FastAPI (API REST)
- Pydantic (Validación de datos)
- Uvicorn (Servidor ASGI)

**Base de Datos:**
- MongoDB Atlas (Cloud - Gratis)
- PyMongo (Driver)

**Arquitectura:**
- Clean Architecture (Arquitectura Onion)
- Separation of Concerns
- Dependency Injection

### Estructura del Proyecto
```
aguasur/
├── src/
│   ├── domain/              # Lógica de negocio pura
│   │   ├── entities/        # Familia, Cisterna, Llenado, Reporte
│   │   └── repositories/    # Interfaces (contratos)
│   ├── application/         # Casos de uso
│   │   └── use_cases/       # Lógica de aplicación
│   ├── infrastructure/      # Implementaciones técnicas
│   │   ├── database/        # Conexión MongoDB
│   │   └── repositories/    # Implementaciones MongoDB
│   └── api/                 # API REST
│       ├── routes/          # Endpoints
│       ├── dtos.py          # Modelos Pydantic
│       └── dependencies.py  # Inyección de dependencias
├── tests/                   # Pruebas
├── docs/                    # Documentación
├── main.py                  # Punto de entrada
└── requirements.txt         # Dependencias
```

---

## 📦 Instalación

### Requisitos Previos
- Python 3.12 o superior
- Cuenta en MongoDB Atlas (gratis)
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU-USUARIO/aguasur.git
cd aguasur
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar MongoDB Atlas

1. Crea una cuenta gratuita en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Crea un cluster gratuito (M0 - 512MB)
3. Configura acceso:
   - **Database Access:** Crea un usuario con contraseña
   - **Network Access:** Permite acceso desde cualquier IP (0.0.0.0/0)
4. Obtén tu connection string

### 5. Configurar variables de entorno

Crea un archivo `.env` en la raíz:
```env
MONGODB_URI=mongodb+srv://tu_usuario:tu_password@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=aguasur_db
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

### 6. Probar la conexión
```bash
python test_connection.py
```

### 7. Ejecutar la API
```bash
uvicorn main:app --reload
```

La API estará disponible en: **http://localhost:8000**

Documentación interactiva: **http://localhost:8000/docs**

---

## 📖 Uso de la API

### Registrar una Familia
```bash
curl -X POST "http://localhost:8000/api/v1/familias" \
  -H "Content-Type: application/json" \
  -d '{
    "direccion": "Av. Petrolera km 7",
    "num_personas": 5,
    "contacto": "+591 70123456",
    "capacidad_almacenamiento": 1000,
    "tiene_cisterna": true,
    "zona": "Villa Petrolera"
  }'
```

### Registrar una Cisterna
```bash
curl -X POST "http://localhost:8000/api/v1/cisternas" \
  -H "Content-Type: application/json" \
  -d '{
    "ubicacion": "Escuela Bolivia",
    "tipo": "escolar",
    "capacidad_total": 5000,
    "nivel_actual": 2000,
    "latitud": -17.4167,
    "longitud": -66.1667
  }'
```

### Obtener Dashboard
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard"
```

### Ver todas las cisternas con nivel crítico
```bash
curl -X GET "http://localhost:8000/api/v1/cisternas?nivel_critico=true"
```

### Crear un Reporte
```bash
curl -X POST "http://localhost:8000/api/v1/reportes" \
  -H "Content-Type: application/json" \
  -d '{
    "familia_id": "FAMILIA_ID_AQUI",
    "tipo": "agua_acabandose",
    "descripcion": "Cisterna familiar casi vacía, necesitamos agua urgente",
    "urgencia": "alta"
  }'
```

---

## 🎯 Impacto Real Medible

### Métricas del Sistema

El sistema permite medir:
- ✅ **X familias** registradas y usando el sistema
- ✅ **Y%** de reducción en días sin agua
- ✅ **Z bolivianos** ahorrados por compra comunitaria
- ✅ **W alertas tempranas** que evitaron emergencias
- ✅ **N cisternas** mapeadas y monitoreadas

### Casos de Éxito

**Optimización de distribución:**
- Antes: Familias sin agua por 5-7 días
- Con AguaSur: Alertas 2 días antes, llenado coordinado

**Ahorro en costos:**
- Antes: Bs. 150 por pipa individual
- Con AguaSur: Bs. 100 por pipa compartida (3-4 familias)

---

## 🤝 Contribuir

Este proyecto es open source y las contribuciones son bienvenidas.

### Cómo Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

### Áreas donde puedes ayudar

- 📱 App móvil (React Native / Flutter)
- 🗺️ Integración con mapas (Google Maps / OpenStreetMap)
- 🤖 Bot de Telegram para alertas
- 📊 Visualizaciones y gráficos
- 🧪 Pruebas automatizadas
- 📝 Documentación
- 🌐 Traducción a otros idiomas

---


## 👨‍💻 Autor

**Jhaziel Mamani** - Estudiante de Computer Science en UMSS y Jala University

- GitHub: Yazzz-0
- Email: jhaziel807@gmail.com


---

## 🎓 Contexto Académico

Este proyecto es parte de mi portafolio para:
- ✅ Demostrar habilidades de desarrollo full-stack
- ✅ Aplicación a PyCon US 2026 con beca de viaje
- ✅ Impacto social medible en mi comunidad
- ✅ Contribución al ecosistema open source de Python

"""
API Principal - AguaSur
Punto de entrada de la API REST con FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import familia_routes, cisterna_routes, llenado_routes, reporte_routes, dashboard_routes

# Crear instancia de FastAPI
app = FastAPI(
    title="AguaSur API",
    description="API para gestión comunitaria del agua en Zona Sud, Cochabamba",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS (para que pueda ser accedido desde web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(dashboard_routes.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(familia_routes.router, prefix="/api/v1/familias", tags=["Familias"])
app.include_router(cisterna_routes.router, prefix="/api/v1/cisternas", tags=["Cisternas"])
app.include_router(llenado_routes.router, prefix="/api/v1/llenados", tags=["Llenados"])
app.include_router(reporte_routes.router, prefix="/api/v1/reportes", tags=["Reportes"])

@app.get("/")
async def root():
    """Endpoint raíz de la API"""
    return {
        "mensaje": "Bienvenido a AguaSur API",
        "version": "1.0.0",
        "descripcion": "Sistema de gestión comunitaria del agua - Zona Sud, Cochabamba",
        "documentacion": "/docs",
        "endpoints": {
            "dashboard": "/api/v1/dashboard",
            "familias": "/api/v1/familias",
            "cisternas": "/api/v1/cisternas",
            "llenados": "/api/v1/llenados",
            "reportes": "/api/v1/reportes"
        }
    }

@app.get("/health")
async def health_check():
    """Verifica el estado de la API"""
    return {
        "status": "healthy",
        "message": "AguaSur API funcionando correctamente"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

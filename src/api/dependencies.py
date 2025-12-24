"""
Dependencias de la API
Configuración de inyección de dependencias.
"""

from src.infrastructure.database import get_database
from src.infrastructure.repositories import (
    MongoDBFamiliaRepository,
    MongoDBCisternaRepository,
    MongoDBLlenadoRepository,
    MongoDBReporteRepository
)
from src.application.use_cases import (
    RegistrarFamilia,
    RegistrarCisterna,
    RegistrarLlenado,
    CrearReporte,
    ObtenerDashboard
)


def get_familia_repository():
    """Obtiene repositorio de familias"""
    db = get_database()
    return MongoDBFamiliaRepository(db)


def get_cisterna_repository():
    """Obtiene repositorio de cisternas"""
    db = get_database()
    return MongoDBCisternaRepository(db)


def get_llenado_repository():
    """Obtiene repositorio de llenados"""
    db = get_database()
    return MongoDBLlenadoRepository(db)


def get_reporte_repository():
    """Obtiene repositorio de reportes"""
    db = get_database()
    return MongoDBReporteRepository(db)


def get_registrar_familia_usecase():
    """Obtiene caso de uso de registrar familia"""
    return RegistrarFamilia(get_familia_repository())


def get_registrar_cisterna_usecase():
    """Obtiene caso de uso de registrar cisterna"""
    return RegistrarCisterna(get_cisterna_repository(), get_familia_repository())


def get_registrar_llenado_usecase():
    """Obtiene caso de uso de registrar llenado"""
    return RegistrarLlenado(get_llenado_repository(), get_cisterna_repository())


def get_crear_reporte_usecase():
    """Obtiene caso de uso de crear reporte"""
    return CrearReporte(
        get_reporte_repository(),
        get_familia_repository(),
        get_cisterna_repository()
    )


def get_obtener_dashboard_usecase():
    """Obtiene caso de uso de dashboard"""
    return ObtenerDashboard(
        get_familia_repository(),
        get_cisterna_repository(),
        get_llenado_repository(),
        get_reporte_repository()
    )

"""
Routes de Dashboard
Endpoints para obtener estadísticas generales.
"""

from fastapi import APIRouter, Depends
from src.api.dependencies import get_obtener_dashboard_usecase
from src.application.use_cases import ObtenerDashboard

router = APIRouter()


@router.get("/dashboard")
async def obtener_dashboard(
    usecase: ObtenerDashboard = Depends(get_obtener_dashboard_usecase)
):
    """
    Obtiene estadísticas generales del sistema.
    
    Retorna:
    - Estadísticas de familias
    - Estadísticas de cisternas
    - Estadísticas de llenados
    - Estadísticas de reportes
    - Alertas activas
    """
    try:
        dashboard = usecase.ejecutar()
        return {
            "success": True,
            "data": dashboard
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

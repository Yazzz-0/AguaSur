"""
Routes de Reportes
Endpoints para gestionar reportes de problemas.
"""

from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import get_reporte_repository, get_crear_reporte_usecase
from src.api.dtos import ReporteCreate
from src.infrastructure.repositories import MongoDBReporteRepository
from src.application.use_cases import CrearReporte
from src.domain.entities.reporte import EstadoReporte, Urgencia

router = APIRouter()


@router.post("/", response_model=dict)
async def crear_reporte(
    reporte: ReporteCreate,
    usecase: CrearReporte = Depends(get_crear_reporte_usecase)
):
    """Crea un nuevo reporte de problema"""
    try:
        reporte_guardado = usecase.ejecutar(
            familia_id=reporte.familia_id,
            tipo=reporte.tipo,
            descripcion=reporte.descripcion,
            urgencia=reporte.urgencia,
            cisterna_id=reporte.cisterna_id,
            latitud=reporte.latitud,
            longitud=reporte.longitud
        )
        
        return {
            "success": True,
            "message": "Reporte creado exitosamente",
            "data": {
                "id": reporte_guardado.id,
                "familia_id": reporte_guardado.familia_id,
                "tipo": reporte_guardado.tipo.value,
                "descripcion": reporte_guardado.descripcion,
                "urgencia": reporte_guardado.urgencia.value,
                "estado": reporte_guardado.estado.value,
                "fecha_reporte": reporte_guardado.fecha_reporte.isoformat()
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def obtener_reportes(
    estado: str = None,
    urgencia: str = None,
    pendientes: bool = False,
    urgentes: bool = False,
    limite: int = 50,
    repo: MongoDBReporteRepository = Depends(get_reporte_repository)
):
    """Obtiene reportes con filtros opcionales"""
    try:
        if pendientes:
            reportes = repo.obtener_pendientes()
        elif urgentes:
            reportes = repo.obtener_urgentes()
        elif estado:
            reportes = repo.obtener_por_estado(EstadoReporte(estado))
        elif urgencia:
            reportes = repo.obtener_por_urgencia(Urgencia(urgencia))
        else:
            reportes = repo.obtener_ultimos_reportes(limite)
        
        return {
            "success": True,
            "count": len(reportes),
            "data": [
                {
                    "id": r.id,
                    "familia_id": r.familia_id,
                    "tipo": r.tipo.value,
                    "descripcion": r.descripcion,
                    "urgencia": r.urgencia.value,
                    "estado": r.estado.value,
                    "cisterna_id": r.cisterna_id,
                    "fecha_reporte": r.fecha_reporte.isoformat(),
                    "es_urgente": r.es_urgente(),
                    "tiempo_transcurrido_horas": round(r.tiempo_desde_reporte(), 2)
                }
                for r in reportes
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{reporte_id}", response_model=dict)
async def obtener_reporte(
    reporte_id: str,
    repo: MongoDBReporteRepository = Depends(get_reporte_repository)
):
    """Obtiene un reporte por su ID"""
    try:
        reporte = repo.obtener_por_id(reporte_id)
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        return {
            "success": True,
            "data": {
                "id": reporte.id,
                "familia_id": reporte.familia_id,
                "tipo": reporte.tipo.value,
                "descripcion": reporte.descripcion,
                "urgencia": reporte.urgencia.value,
                "estado": reporte.estado.value,
                "cisterna_id": reporte.cisterna_id,
                "latitud": reporte.latitud,
                "longitud": reporte.longitud,
                "fecha_reporte": reporte.fecha_reporte.isoformat(),
                "fecha_resolucion": reporte.fecha_resolucion.isoformat() if reporte.fecha_resolucion else None,
                "observaciones_resolucion": reporte.observaciones_resolucion,
                "es_urgente": reporte.es_urgente(),
                "esta_resuelto": reporte.esta_resuelto()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{reporte_id}/resolver", response_model=dict)
async def resolver_reporte(
    reporte_id: str,
    observaciones: str = None,
    repo: MongoDBReporteRepository = Depends(get_reporte_repository)
):
    """Marca un reporte como resuelto"""
    try:
        reporte = repo.obtener_por_id(reporte_id)
        if not reporte:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        reporte.resolver(observaciones or "")
        repo.actualizar(reporte)
        
        return {
            "success": True,
            "message": "Reporte marcado como resuelto",
            "data": {
                "id": reporte.id,
                "estado": reporte.estado.value,
                "fecha_resolucion": reporte.fecha_resolucion.isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas/resumen", response_model=dict)
async def obtener_estadisticas_reportes(
    repo: MongoDBReporteRepository = Depends(get_reporte_repository)
):
    """Obtiene estadísticas de reportes"""
    try:
        total = repo.contar_reportes()
        pendientes = repo.contar_por_estado(EstadoReporte.PENDIENTE)
        resueltos = repo.contar_por_estado(EstadoReporte.RESUELTO)
        urgentes = repo.contar_urgentes()
        
        return {
            "success": True,
            "data": {
                "total_reportes": total,
                "pendientes": pendientes,
                "resueltos": resueltos,
                "urgentes": urgentes,
                "porcentaje_resueltos": round((resueltos / total * 100) if total > 0 else 0, 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

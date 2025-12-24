"""
Routes de Cisternas
Endpoints para gestionar cisternas.
"""

from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import get_cisterna_repository, get_registrar_cisterna_usecase
from src.api.dtos import CisternaCreate
from src.infrastructure.repositories import MongoDBCisternaRepository
from src.application.use_cases import RegistrarCisterna

router = APIRouter()


@router.post("/", response_model=dict)
async def registrar_cisterna(
    cisterna: CisternaCreate,
    usecase: RegistrarCisterna = Depends(get_registrar_cisterna_usecase)
):
    """Registra una nueva cisterna"""
    try:
        cisterna_guardada = usecase.ejecutar(
            ubicacion=cisterna.ubicacion,
            tipo=cisterna.tipo,
            capacidad_total=cisterna.capacidad_total,
            nivel_actual=cisterna.nivel_actual,
            latitud=cisterna.latitud,
            longitud=cisterna.longitud,
            familia_id=cisterna.familia_id
        )
        
        return {
            "success": True,
            "message": "Cisterna registrada exitosamente",
            "data": {
                "id": cisterna_guardada.id,
                "ubicacion": cisterna_guardada.ubicacion,
                "tipo": cisterna_guardada.tipo.value,
                "capacidad_total": cisterna_guardada.capacidad_total,
                "nivel_actual": cisterna_guardada.nivel_actual,
                "porcentaje_lleno": round(cisterna_guardada.porcentaje_lleno(), 2)
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def obtener_cisternas(
    tipo: str = None,
    nivel_critico: bool = False,
    vacias: bool = False,
    repo: MongoDBCisternaRepository = Depends(get_cisterna_repository)
):
    """Obtiene cisternas con filtros opcionales"""
    try:
        if nivel_critico:
            cisternas = repo.obtener_con_nivel_critico()
        elif vacias:
            cisternas = repo.obtener_vacias()
        elif tipo:
            from src.domain.entities.cisterna import TipoCisterna
            cisternas = repo.obtener_por_tipo(TipoCisterna(tipo))
        else:
            cisternas = repo.obtener_todas()
        
        return {
            "success": True,
            "count": len(cisternas),
            "data": [
                {
                    "id": c.id,
                    "ubicacion": c.ubicacion,
                    "tipo": c.tipo.value,
                    "capacidad_total": c.capacidad_total,
                    "nivel_actual": c.nivel_actual,
                    "porcentaje_lleno": round(c.porcentaje_lleno(), 2),
                    "estado": c.estado.value,
                    "es_prioritaria": c.es_prioritaria(),
                    "nivel_critico": c.nivel_critico(),
                    "latitud": c.latitud,
                    "longitud": c.longitud
                }
                for c in cisternas
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cisterna_id}", response_model=dict)
async def obtener_cisterna(
    cisterna_id: str,
    repo: MongoDBCisternaRepository = Depends(get_cisterna_repository)
):
    """Obtiene una cisterna por su ID"""
    try:
        cisterna = repo.obtener_por_id(cisterna_id)
        if not cisterna:
            raise HTTPException(status_code=404, detail="Cisterna no encontrada")
        
        return {
            "success": True,
            "data": {
                "id": cisterna.id,
                "ubicacion": cisterna.ubicacion,
                "tipo": cisterna.tipo.value,
                "capacidad_total": cisterna.capacidad_total,
                "nivel_actual": cisterna.nivel_actual,
                "porcentaje_lleno": round(cisterna.porcentaje_lleno(), 2),
                "estado": cisterna.estado.value,
                "familia_id": cisterna.familia_id,
                "latitud": cisterna.latitud,
                "longitud": cisterna.longitud,
                "litros_para_llenar": cisterna.litros_para_llenar(),
                "esta_vacia": cisterna.esta_vacia(),
                "nivel_critico": cisterna.nivel_critico(),
                "es_prioritaria": cisterna.es_prioritaria()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mapa/coordenadas", response_model=dict)
async def obtener_cisternas_mapa(
    repo: MongoDBCisternaRepository = Depends(get_cisterna_repository)
):
    """Obtiene cisternas con coordenadas para mostrar en mapa"""
    try:
        cisternas = repo.obtener_con_coordenadas()
        
        return {
            "success": True,
            "count": len(cisternas),
            "data": [
                {
                    "id": c.id,
                    "ubicacion": c.ubicacion,
                    "tipo": c.tipo.value,
                    "nivel_actual": c.nivel_actual,
                    "capacidad_total": c.capacidad_total,
                    "porcentaje_lleno": round(c.porcentaje_lleno(), 2),
                    "latitud": c.latitud,
                    "longitud": c.longitud,
                    "estado": c.estado.value,
                    "nivel_critico": c.nivel_critico(),
                    "es_prioritaria": c.es_prioritaria()
                }
                for c in cisternas
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

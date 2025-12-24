"""
Routes de Llenados
Endpoints para gestionar llenados de cisternas.
"""

from fastapi import APIRouter, Depends, HTTPException
from datetime import date
from src.api.dependencies import get_llenado_repository, get_registrar_llenado_usecase
from src.api.dtos import LlenadoCreate
from src.infrastructure.repositories import MongoDBLlenadoRepository
from src.application.use_cases import RegistrarLlenado

router = APIRouter()


@router.post("/", response_model=dict)
async def registrar_llenado(
    llenado: LlenadoCreate,
    usecase: RegistrarLlenado = Depends(get_registrar_llenado_usecase)
):
    """Registra un nuevo llenado de cisterna"""
    try:
        llenado_guardado = usecase.ejecutar(
            cisterna_id=llenado.cisterna_id,
            litros_suministrados=llenado.litros_suministrados,
            costo=llenado.costo,
            proveedor=llenado.proveedor,
            observaciones=llenado.observaciones
        )
        
        return {
            "success": True,
            "message": "Llenado registrado exitosamente",
            "data": {
                "id": llenado_guardado.id,
                "cisterna_id": llenado_guardado.cisterna_id,
                "litros_suministrados": llenado_guardado.litros_suministrados,
                "costo": llenado_guardado.costo,
                "costo_por_litro": round(llenado_guardado.costo_por_litro(), 2),
                "proveedor": llenado_guardado.proveedor,
                "nivel_anterior": llenado_guardado.nivel_anterior,
                "nivel_posterior": llenado_guardado.nivel_posterior,
                "fecha": llenado_guardado.fecha.isoformat()
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=dict)
async def obtener_llenados(
    cisterna_id: str = None,
    proveedor: str = None,
    limite: int = 50,
    repo: MongoDBLlenadoRepository = Depends(get_llenado_repository)
):
    """Obtiene llenados con filtros opcionales"""
    try:
        if cisterna_id:
            llenados = repo.obtener_por_cisterna(cisterna_id)
        elif proveedor:
            llenados = repo.obtener_por_proveedor(proveedor)
        else:
            llenados = repo.obtener_ultimos_llenados(limite)
        
        return {
            "success": True,
            "count": len(llenados),
            "data": [
                {
                    "id": l.id,
                    "cisterna_id": l.cisterna_id,
                    "fecha": l.fecha.isoformat(),
                    "litros_suministrados": l.litros_suministrados,
                    "costo": l.costo,
                    "costo_por_litro": round(l.costo_por_litro(), 2),
                    "proveedor": l.proveedor,
                    "nivel_anterior": l.nivel_anterior,
                    "nivel_posterior": l.nivel_posterior
                }
                for l in llenados
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas", response_model=dict)
async def obtener_estadisticas_llenados(
    repo: MongoDBLlenadoRepository = Depends(get_llenado_repository)
):
    """Obtiene estadísticas de llenados"""
    try:
        total_llenados = repo.contar_llenados()
        total_litros = repo.calcular_total_litros()
        total_costo = repo.calcular_total_costo()
        costo_promedio = repo.calcular_costo_promedio_por_litro()
        proveedores = repo.obtener_proveedores()
        
        return {
            "success": True,
            "data": {
                "total_llenados": total_llenados,
                "total_litros_suministrados": total_litros,
                "total_costo_bs": round(total_costo, 2),
                "costo_promedio_por_litro_bs": round(costo_promedio, 2),
                "proveedores": proveedores,
                "total_proveedores": len(proveedores)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cisterna/{cisterna_id}/historial", response_model=dict)
async def obtener_historial_cisterna(
    cisterna_id: str,
    repo: MongoDBLlenadoRepository = Depends(get_llenado_repository)
):
    """Obtiene historial de llenados de una cisterna"""
    try:
        llenados = repo.obtener_por_cisterna(cisterna_id)
        
        if not llenados:
            return {
                "success": True,
                "message": "No hay llenados registrados para esta cisterna",
                "count": 0,
                "data": []
            }
        
        total_litros = sum(l.litros_suministrados for l in llenados)
        total_costo = sum(l.costo for l in llenados)
        
        return {
            "success": True,
            "count": len(llenados),
            "resumen": {
                "total_llenados": len(llenados),
                "total_litros": total_litros,
                "total_costo_bs": round(total_costo, 2),
                "ultimo_llenado": llenados[0].fecha.isoformat() if llenados else None
            },
            "data": [
                {
                    "id": l.id,
                    "fecha": l.fecha.isoformat(),
                    "litros_suministrados": l.litros_suministrados,
                    "costo": l.costo,
                    "proveedor": l.proveedor,
                    "nivel_posterior": l.nivel_posterior
                }
                for l in llenados
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

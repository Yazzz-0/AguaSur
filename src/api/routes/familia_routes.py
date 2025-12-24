"""
Routes de Familias
Endpoints para gestionar familias.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.api.dependencies import get_familia_repository, get_registrar_familia_usecase
from src.api.dtos import FamiliaCreate, FamiliaResponse
from src.infrastructure.repositories import MongoDBFamiliaRepository
from src.application.use_cases import RegistrarFamilia

router = APIRouter()


@router.post("/", response_model=dict)
async def registrar_familia(
    familia: FamiliaCreate,
    usecase: RegistrarFamilia = Depends(get_registrar_familia_usecase)
):
    """Registra una nueva familia en el sistema"""
    try:
        familia_guardada = usecase.ejecutar(
            direccion=familia.direccion,
            num_personas=familia.num_personas,
            contacto=familia.contacto,
            capacidad_almacenamiento=familia.capacidad_almacenamiento,
            tiene_cisterna=familia.tiene_cisterna,
            zona=familia.zona,
            consumo_promedio_diario=familia.consumo_promedio_diario
        )
        
        return {
            "success": True,
            "message": "Familia registrada exitosamente",
            "data": {
                "id": familia_guardada.id,
                "direccion": familia_guardada.direccion,
                "contacto": familia_guardada.contacto,
                "zona": familia_guardada.zona
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/", response_model=dict)
async def obtener_familias(
    zona: str = None,
    repo: MongoDBFamiliaRepository = Depends(get_familia_repository)
):
    """Obtiene todas las familias o filtra por zona"""
    try:
        if zona:
            familias = repo.obtener_por_zona(zona)
        else:
            familias = repo.obtener_todas()
        
        return {
            "success": True,
            "count": len(familias),
            "data": [
                {
                    "id": f.id,
                    "direccion": f.direccion,
                    "num_personas": f.num_personas,
                    "contacto": f.contacto,
                    "zona": f.zona,
                    "tiene_cisterna": f.tiene_cisterna,
                    "consumo_promedio_diario": f.consumo_promedio_diario
                }
                for f in familias
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{familia_id}", response_model=dict)
async def obtener_familia(
    familia_id: str,
    repo: MongoDBFamiliaRepository = Depends(get_familia_repository)
):
    """Obtiene una familia por su ID"""
    try:
        familia = repo.obtener_por_id(familia_id)
        if not familia:
            raise HTTPException(status_code=404, detail="Familia no encontrada")
        
        return {
            "success": True,
            "data": {
                "id": familia.id,
                "direccion": familia.direccion,
                "num_personas": familia.num_personas,
                "contacto": familia.contacto,
                "capacidad_almacenamiento": familia.capacidad_almacenamiento,
                "tiene_cisterna": familia.tiene_cisterna,
                "zona": familia.zona,
                "consumo_promedio_diario": familia.consumo_promedio_diario,
                "activo": familia.activo
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

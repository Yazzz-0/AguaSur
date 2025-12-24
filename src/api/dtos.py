"""
DTOs (Data Transfer Objects) - Modelos Pydantic
Define los esquemas de entrada y salida de la API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# === FAMILIA DTOs ===

class FamiliaCreate(BaseModel):
    """DTO para crear una familia"""
    direccion: str = Field(..., min_length=1, description="Dirección completa")
    num_personas: int = Field(..., gt=0, description="Número de personas")
    contacto: str = Field(..., min_length=1, description="Teléfono o Telegram")
    capacidad_almacenamiento: int = Field(..., gt=0, description="Capacidad en litros")
    tiene_cisterna: bool = Field(..., description="¿Tiene cisterna propia?")
    zona: str = Field(..., min_length=1, description="Zona")
    consumo_promedio_diario: Optional[float] = Field(None, description="Consumo promedio L/día")


class FamiliaResponse(BaseModel):
    """DTO de respuesta de familia"""
    id: str
    direccion: str
    num_personas: int
    contacto: str
    capacidad_almacenamiento: int
    tiene_cisterna: bool
    zona: str
    consumo_promedio_diario: float
    activo: bool
    fecha_registro: datetime


# === CISTERNA DTOs ===

class CisternaCreate(BaseModel):
    """DTO para crear una cisterna"""
    ubicacion: str = Field(..., min_length=1)
    tipo: str = Field(..., description="familiar, comunitaria, escolar, centro_salud")
    capacidad_total: int = Field(..., gt=0)
    nivel_actual: int = Field(0, ge=0)
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    familia_id: Optional[str] = None


class CisternaResponse(BaseModel):
    """DTO de respuesta de cisterna"""
    id: str
    ubicacion: str
    tipo: str
    capacidad_total: int
    nivel_actual: int
    porcentaje_lleno: float
    latitud: Optional[float]
    longitud: Optional[float]
    familia_id: Optional[str]
    estado: str
    fecha_instalacion: datetime


# === LLENADO DTOs ===

class LlenadoCreate(BaseModel):
    """DTO para registrar un llenado"""
    cisterna_id: str = Field(..., min_length=1)
    litros_suministrados: int = Field(..., gt=0)
    costo: float = Field(..., ge=0)
    proveedor: str = Field(..., min_length=1)
    observaciones: Optional[str] = None


class LlenadoResponse(BaseModel):
    """DTO de respuesta de llenado"""
    id: str
    cisterna_id: str
    fecha: datetime
    litros_suministrados: int
    costo: float
    costo_por_litro: float
    proveedor: str
    nivel_anterior: int
    nivel_posterior: int
    observaciones: Optional[str]


# === REPORTE DTOs ===

class ReporteCreate(BaseModel):
    """DTO para crear un reporte"""
    familia_id: str = Field(..., min_length=1)
    tipo: str = Field(..., description="Tipo de reporte")
    descripcion: str = Field(..., min_length=1)
    urgencia: str = Field("media", description="baja, media, alta, critica")
    cisterna_id: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None


class ReporteResponse(BaseModel):
    """DTO de respuesta de reporte"""
    id: str
    familia_id: str
    tipo: str
    descripcion: str
    urgencia: str
    estado: str
    cisterna_id: Optional[str]
    latitud: Optional[float]
    longitud: Optional[float]
    fecha_reporte: datetime
    fecha_resolucion: Optional[datetime]

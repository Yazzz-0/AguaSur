"""
Entidad Reporte - Domain Layer
Representa un reporte de problema o solicitud relacionada con el agua.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class TipoReporte(Enum):
    """Tipos de reportes posibles"""
    AGUA_ACABANDOSE = "agua_acabandose"
    AGUA_CONTAMINADA = "agua_contaminada"
    CISTERNA_DANADA = "cisterna_dañada"
    FUGA_AGUA = "fuga_agua"
    SOLICITUD_LLENADO = "solicitud_llenado"
    OTRO = "otro"


class Urgencia(Enum):
    """Niveles de urgencia"""
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class EstadoReporte(Enum):
    """Estados posibles de un reporte"""
    PENDIENTE = "pendiente"
    EN_REVISION = "en_revision"
    EN_PROCESO = "en_proceso"
    RESUELTO = "resuelto"
    CERRADO = "cerrado"


@dataclass
class Reporte:
    """
    Entidad que representa un reporte de problema o solicitud.
    
    Atributos:
        familia_id: ID de la familia que reporta
        tipo: Tipo de reporte
        descripcion: Descripción del problema
        urgencia: Nivel de urgencia
        estado: Estado actual del reporte
        cisterna_id: ID de cisterna relacionada (opcional)
        latitud: Coordenada si es reporte de ubicación específica
        longitud: Coordenada si es reporte de ubicación específica
        fecha_reporte: Fecha del reporte
        fecha_resolucion: Fecha de resolución (si fue resuelto)
        observaciones_resolucion: Observaciones al resolver
        id: ID de MongoDB (opcional)
    """
    familia_id: str
    tipo: TipoReporte
    descripcion: str
    urgencia: Urgencia = Urgencia.MEDIA
    estado: EstadoReporte = EstadoReporte.PENDIENTE
    cisterna_id: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    fecha_reporte: Optional[datetime] = None
    fecha_resolucion: Optional[datetime] = None
    observaciones_resolucion: Optional[str] = None
    id: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.familia_id or not self.familia_id.strip():
            raise ValueError("El familia_id no puede estar vacío")
        
        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")
        
        # Validar enums
        if isinstance(self.tipo, str):
            self.tipo = TipoReporte(self.tipo)
        
        if isinstance(self.urgencia, str):
            self.urgencia = Urgencia(self.urgencia)
        
        if isinstance(self.estado, str):
            self.estado = EstadoReporte(self.estado)
        
        # Normalizar
        self.descripcion = self.descripcion.strip()
        if self.observaciones_resolucion:
            self.observaciones_resolucion = self.observaciones_resolucion.strip()
        
        # Fecha por defecto
        if self.fecha_reporte is None:
            self.fecha_reporte = datetime.now()
    
    def es_urgente(self) -> bool:
        """
        Verifica si el reporte es urgente.
        
        Returns:
            True si es urgencia alta o crítica
        """
        return self.urgencia in [Urgencia.ALTA, Urgencia.CRITICA]
    
    def esta_pendiente(self) -> bool:
        """
        Verifica si el reporte está pendiente de atención.
        
        Returns:
            True si está pendiente
        """
        return self.estado == EstadoReporte.PENDIENTE
    
    def esta_resuelto(self) -> bool:
        """
        Verifica si el reporte fue resuelto.
        
        Returns:
            True si fue resuelto o cerrado
        """
        return self.estado in [EstadoReporte.RESUELTO, EstadoReporte.CERRADO]
    
    def tiempo_desde_reporte(self) -> float:
        """
        Calcula cuánto tiempo ha pasado desde el reporte.
        
        Returns:
            Horas transcurridas
        """
        if self.fecha_reporte is None:
            return 0.0
        
        delta = datetime.now() - self.fecha_reporte
        return delta.total_seconds() / 3600  # convertir a horas
    
    def cambiar_estado(self, nuevo_estado: EstadoReporte) -> None:
        """
        Cambia el estado del reporte.
        
        Args:
            nuevo_estado: Nuevo estado del reporte
        """
        if not isinstance(nuevo_estado, EstadoReporte):
            raise ValueError("El estado debe ser un EstadoReporte válido")
        
        self.estado = nuevo_estado
        
        # Si se marca como resuelto, registrar fecha
        if nuevo_estado in [EstadoReporte.RESUELTO, EstadoReporte.CERRADO]:
            if self.fecha_resolucion is None:
                self.fecha_resolucion = datetime.now()
    
    def resolver(self, observaciones: str = "") -> None:
        """
        Marca el reporte como resuelto.
        
        Args:
            observaciones: Observaciones sobre la resolución
        """
        self.estado = EstadoReporte.RESUELTO
        self.fecha_resolucion = datetime.now()
        if observaciones:
            self.observaciones_resolucion = observaciones.strip()
    
    def aumentar_urgencia(self) -> None:
        """Aumenta el nivel de urgencia del reporte"""
        if self.urgencia == Urgencia.BAJA:
            self.urgencia = Urgencia.MEDIA
        elif self.urgencia == Urgencia.MEDIA:
            self.urgencia = Urgencia.ALTA
        elif self.urgencia == Urgencia.ALTA:
            self.urgencia = Urgencia.CRITICA
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (para MongoDB).
        
        Returns:
            Diccionario con los datos del reporte
        """
        data = {
            'familia_id': self.familia_id,
            'tipo': self.tipo.value,
            'descripcion': self.descripcion,
            'urgencia': self.urgencia.value,
            'estado': self.estado.value,
            'cisterna_id': self.cisterna_id,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'fecha_reporte': self.fecha_reporte,
            'fecha_resolucion': self.fecha_resolucion,
            'observaciones_resolucion': self.observaciones_resolucion
        }
        
        if self.id:
            data['_id'] = self.id
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reporte':
        """
        Crea una instancia de Reporte desde un diccionario (desde MongoDB).
        
        Args:
            data: Diccionario con los datos del reporte
            
        Returns:
            Instancia de Reporte
        """
        return cls(
            familia_id=data['familia_id'],
            tipo=TipoReporte(data['tipo']),
            descripcion=data['descripcion'],
            urgencia=Urgencia(data.get('urgencia', 'media')),
            estado=EstadoReporte(data.get('estado', 'pendiente')),
            cisterna_id=data.get('cisterna_id'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            fecha_reporte=data.get('fecha_reporte'),
            fecha_resolucion=data.get('fecha_resolucion'),
            observaciones_resolucion=data.get('observaciones_resolucion'),
            id=str(data.get('_id', ''))
        )
    
    def __str__(self) -> str:
        """Representación en string del reporte"""
        return (
            f"Reporte({self.tipo.value}, {self.urgencia.value}, "
            f"{self.estado.value}, {self.fecha_reporte.strftime('%Y-%m-%d')})"
        )
    
    def __repr__(self) -> str:
        """Representación detallada del reporte"""
        return (
            f"Reporte(tipo={self.tipo.value}, urgencia={self.urgencia.value}, "
            f"estado={self.estado.value}, familia_id='{self.familia_id}')"
        )

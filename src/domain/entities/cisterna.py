"""
Entidad Cisterna - Domain Layer
Representa una cisterna de almacenamiento de agua.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class TipoCisterna(Enum):
    """Tipos de cisternas en el sistema"""
    FAMILIAR = "familiar"
    COMUNITARIA = "comunitaria"
    ESCOLAR = "escolar"
    CENTRO_SALUD = "centro_salud"


class EstadoCisterna(Enum):
    """Estados posibles de una cisterna"""
    OPERATIVA = "operativa"
    DANADA = "dañada"
    EN_MANTENIMIENTO = "en_mantenimiento"
    INACTIVA = "inactiva"


@dataclass
class Cisterna:
    """
    Entidad que representa una cisterna de almacenamiento de agua.
    
    Atributos:
        ubicacion: Dirección o descripción de ubicación
        tipo: Tipo de cisterna
        capacidad_total: Capacidad máxima en litros
        nivel_actual: Nivel actual en litros
        latitud: Coordenada de latitud (opcional)
        longitud: Coordenada de longitud (opcional)
        familia_id: ID de la familia propietaria (si es familiar)
        estado: Estado de la cisterna
        id: ID de MongoDB (opcional)
        fecha_instalacion: Fecha de instalación
        ultima_actualizacion: Última vez que se actualizó el nivel
    """
    ubicacion: str
    tipo: TipoCisterna
    capacidad_total: int  # litros
    nivel_actual: int = 0  # litros
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    familia_id: Optional[str] = None
    estado: EstadoCisterna = EstadoCisterna.OPERATIVA
    id: Optional[str] = None
    fecha_instalacion: Optional[datetime] = None
    ultima_actualizacion: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.ubicacion or not self.ubicacion.strip():
            raise ValueError("La ubicación no puede estar vacía")
        
        if self.capacidad_total <= 0:
            raise ValueError("La capacidad total debe ser mayor a 0")
        
        if self.nivel_actual < 0:
            raise ValueError("El nivel actual no puede ser negativo")
        
        if self.nivel_actual > self.capacidad_total:
            raise ValueError("El nivel actual no puede ser mayor a la capacidad total")
        
        # Validar tipo
        if isinstance(self.tipo, str):
            self.tipo = TipoCisterna(self.tipo)
        
        # Validar estado
        if isinstance(self.estado, str):
            self.estado = EstadoCisterna(self.estado)
        
        # Normalizar
        self.ubicacion = self.ubicacion.strip()
        
        # Fechas por defecto
        if self.fecha_instalacion is None:
            self.fecha_instalacion = datetime.now()
        
        if self.ultima_actualizacion is None:
            self.ultima_actualizacion = datetime.now()
    
    def porcentaje_lleno(self) -> float:
        """
        Calcula el porcentaje de llenado de la cisterna.
        
        Returns:
            Porcentaje (0-100)
        """
        if self.capacidad_total == 0:
            return 0.0
        
        return (self.nivel_actual / self.capacidad_total) * 100
    
    def esta_vacia(self) -> bool:
        """
        Verifica si la cisterna está vacía.
        
        Returns:
            True si está vacía
        """
        return self.nivel_actual == 0
    
    def esta_llena(self) -> bool:
        """
        Verifica si la cisterna está llena.
        
        Returns:
            True si está llena
        """
        return self.nivel_actual >= self.capacidad_total
    
    def nivel_critico(self, porcentaje_critico: float = 20.0) -> bool:
        """
        Verifica si el nivel está en estado crítico.
        
        Args:
            porcentaje_critico: Porcentaje considerado crítico
            
        Returns:
            True si está en nivel crítico
        """
        return self.porcentaje_lleno() <= porcentaje_critico
    
    def nivel_bajo(self, porcentaje_bajo: float = 40.0) -> bool:
        """
        Verifica si el nivel está bajo.
        
        Args:
            porcentaje_bajo: Porcentaje considerado bajo
            
        Returns:
            True si está en nivel bajo
        """
        return self.porcentaje_lleno() <= porcentaje_bajo
    
    def llenar(self, litros: int) -> None:
        """
        Llena la cisterna con una cantidad de litros.
        
        Args:
            litros: Cantidad de litros a agregar
            
        Raises:
            ValueError: Si la cantidad es inválida o excede la capacidad
        """
        if litros <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        nuevo_nivel = self.nivel_actual + litros
        
        if nuevo_nivel > self.capacidad_total:
            self.nivel_actual = self.capacidad_total
        else:
            self.nivel_actual = nuevo_nivel
        
        self.ultima_actualizacion = datetime.now()
    
    def consumir(self, litros: int) -> None:
        """
        Registra consumo de agua de la cisterna.
        
        Args:
            litros: Cantidad de litros consumidos
            
        Raises:
            ValueError: Si la cantidad es inválida o excede el nivel actual
        """
        if litros <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        if litros > self.nivel_actual:
            raise ValueError(
                f"No hay suficiente agua. Disponible: {self.nivel_actual}L, Solicitado: {litros}L"
            )
        
        self.nivel_actual -= litros
        self.ultima_actualizacion = datetime.now()
    
    def actualizar_nivel(self, nuevo_nivel: int) -> None:
        """
        Actualiza el nivel actual de la cisterna.
        
        Args:
            nuevo_nivel: Nuevo nivel en litros
            
        Raises:
            ValueError: Si el nivel es inválido
        """
        if nuevo_nivel < 0:
            raise ValueError("El nivel no puede ser negativo")
        
        if nuevo_nivel > self.capacidad_total:
            raise ValueError(
                f"El nivel ({nuevo_nivel}L) no puede ser mayor a la capacidad ({self.capacidad_total}L)"
            )
        
        self.nivel_actual = nuevo_nivel
        self.ultima_actualizacion = datetime.now()
    
    def cambiar_estado(self, nuevo_estado: EstadoCisterna) -> None:
        """
        Cambia el estado de la cisterna.
        
        Args:
            nuevo_estado: Nuevo estado de la cisterna
        """
        if not isinstance(nuevo_estado, EstadoCisterna):
            raise ValueError("El estado debe ser un EstadoCisterna válido")
        
        self.estado = nuevo_estado
    
    def es_prioritaria(self) -> bool:
        """
        Determina si la cisterna es prioritaria (escuela o centro de salud).
        
        Returns:
            True si es prioritaria
        """
        return self.tipo in [TipoCisterna.ESCOLAR, TipoCisterna.CENTRO_SALUD]
    
    def litros_para_llenar(self) -> int:
        """
        Calcula cuántos litros se necesitan para llenar completamente.
        
        Returns:
            Litros necesarios
        """
        return self.capacidad_total - self.nivel_actual
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (para MongoDB).
        
        Returns:
            Diccionario con los datos de la cisterna
        """
        data = {
            'ubicacion': self.ubicacion,
            'tipo': self.tipo.value,
            'capacidad_total': self.capacidad_total,
            'nivel_actual': self.nivel_actual,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'familia_id': self.familia_id,
            'estado': self.estado.value,
            'fecha_instalacion': self.fecha_instalacion,
            'ultima_actualizacion': self.ultima_actualizacion
        }
        
        if self.id:
            data['_id'] = self.id
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cisterna':
        """
        Crea una instancia de Cisterna desde un diccionario (desde MongoDB).
        
        Args:
            data: Diccionario con los datos de la cisterna
            
        Returns:
            Instancia de Cisterna
        """
        return cls(
            ubicacion=data['ubicacion'],
            tipo=TipoCisterna(data['tipo']),
            capacidad_total=data['capacidad_total'],
            nivel_actual=data.get('nivel_actual', 0),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            familia_id=data.get('familia_id'),
            estado=EstadoCisterna(data.get('estado', 'operativa')),
            id=str(data.get('_id', '')),
            fecha_instalacion=data.get('fecha_instalacion'),
            ultima_actualizacion=data.get('ultima_actualizacion')
        )
    
    def __str__(self) -> str:
        """Representación en string de la cisterna"""
        return (
            f"Cisterna({self.tipo.value}, {self.ubicacion}, "
            f"{self.nivel_actual}/{self.capacidad_total}L - {self.porcentaje_lleno():.1f}%)"
        )
    
    def __repr__(self) -> str:
        """Representación detallada de la cisterna"""
        return (
            f"Cisterna(tipo={self.tipo.value}, capacidad={self.capacidad_total}L, "
            f"nivel={self.nivel_actual}L, estado={self.estado.value})"
        )

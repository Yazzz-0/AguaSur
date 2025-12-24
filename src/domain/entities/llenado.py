"""
Entidad Llenado - Domain Layer
Representa un registro de llenado de cisterna.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Llenado:
    """
    Entidad que representa un llenado de cisterna.
    
    Atributos:
        cisterna_id: ID de la cisterna llenada
        fecha: Fecha y hora del llenado
        litros_suministrados: Cantidad de litros agregados
        costo: Costo del llenado en bolivianos
        proveedor: Nombre del proveedor (ej: "Pipas de Agua S.A.")
        nivel_anterior: Nivel de la cisterna antes del llenado
        nivel_posterior: Nivel de la cisterna después del llenado
        observaciones: Observaciones adicionales
        id: ID de MongoDB (opcional)
    """
    cisterna_id: str
    litros_suministrados: int
    costo: float
    proveedor: str
    nivel_anterior: int = 0
    nivel_posterior: int = 0
    fecha: Optional[datetime] = None
    observaciones: Optional[str] = None
    id: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.cisterna_id or not self.cisterna_id.strip():
            raise ValueError("El cisterna_id no puede estar vacío")
        
        if self.litros_suministrados <= 0:
            raise ValueError("Los litros suministrados deben ser mayores a 0")
        
        if self.costo < 0:
            raise ValueError("El costo no puede ser negativo")
        
        if not self.proveedor or not self.proveedor.strip():
            raise ValueError("El proveedor no puede estar vacío")
        
        if self.nivel_anterior < 0:
            raise ValueError("El nivel anterior no puede ser negativo")
        
        if self.nivel_posterior < self.nivel_anterior:
            raise ValueError("El nivel posterior no puede ser menor al nivel anterior")
        
        # Normalizar
        self.proveedor = self.proveedor.strip()
        if self.observaciones:
            self.observaciones = self.observaciones.strip()
        
        # Fecha por defecto
        if self.fecha is None:
            self.fecha = datetime.now()
    
    def costo_por_litro(self) -> float:
        """
        Calcula el costo por litro del llenado.
        
        Returns:
            Costo por litro en bolivianos
        """
        if self.litros_suministrados == 0:
            return 0.0
        
        return self.costo / self.litros_suministrados
    
    def es_llenado_completo(self, capacidad_cisterna: int) -> bool:
        """
        Verifica si fue un llenado completo de la cisterna.
        
        Args:
            capacidad_cisterna: Capacidad total de la cisterna
            
        Returns:
            True si se llenó completamente
        """
        return self.nivel_posterior >= capacidad_cisterna
    
    def porcentaje_llenado(self, capacidad_cisterna: int) -> float:
        """
        Calcula qué porcentaje de la capacidad se llenó.
        
        Args:
            capacidad_cisterna: Capacidad total de la cisterna
            
        Returns:
            Porcentaje llenado (0-100)
        """
        if capacidad_cisterna == 0:
            return 0.0
        
        return (self.litros_suministrados / capacidad_cisterna) * 100
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (para MongoDB).
        
        Returns:
            Diccionario con los datos del llenado
        """
        data = {
            'cisterna_id': self.cisterna_id,
            'fecha': self.fecha,
            'litros_suministrados': self.litros_suministrados,
            'costo': self.costo,
            'proveedor': self.proveedor,
            'nivel_anterior': self.nivel_anterior,
            'nivel_posterior': self.nivel_posterior,
            'observaciones': self.observaciones
        }
        
        if self.id:
            data['_id'] = self.id
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Llenado':
        """
        Crea una instancia de Llenado desde un diccionario (desde MongoDB).
        
        Args:
            data: Diccionario con los datos del llenado
            
        Returns:
            Instancia de Llenado
        """
        return cls(
            cisterna_id=data['cisterna_id'],
            litros_suministrados=data['litros_suministrados'],
            costo=data['costo'],
            proveedor=data['proveedor'],
            nivel_anterior=data.get('nivel_anterior', 0),
            nivel_posterior=data.get('nivel_posterior', 0),
            fecha=data.get('fecha'),
            observaciones=data.get('observaciones'),
            id=str(data.get('_id', ''))
        )
    
    def __str__(self) -> str:
        """Representación en string del llenado"""
        return (
            f"Llenado({self.fecha.strftime('%Y-%m-%d')}, "
            f"{self.litros_suministrados}L, Bs.{self.costo:.2f}, {self.proveedor})"
        )
    
    def __repr__(self) -> str:
        """Representación detallada del llenado"""
        return (
            f"Llenado(cisterna_id='{self.cisterna_id}', litros={self.litros_suministrados}L, "
            f"costo=Bs.{self.costo:.2f}, fecha='{self.fecha}')"
        )

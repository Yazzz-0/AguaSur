"""
CisternaRepository - Interface (Domain Layer)
Define el contrato para operaciones con cisternas.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.cisterna import Cisterna, TipoCisterna, EstadoCisterna


class CisternaRepository(ABC):
    """
    Interface que define las operaciones para gestionar cisternas.
    """
    
    @abstractmethod
    def guardar(self, cisterna: Cisterna) -> Cisterna:
        """Guarda una nueva cisterna"""
        pass
    
    @abstractmethod
    def actualizar(self, cisterna: Cisterna) -> Cisterna:
        """Actualiza una cisterna existente"""
        pass
    
    @abstractmethod
    def eliminar(self, cisterna_id: str) -> bool:
        """Elimina una cisterna por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, cisterna_id: str) -> Optional[Cisterna]:
        """Obtiene una cisterna por su ID"""
        pass
    
    @abstractmethod
    def obtener_todas(self) -> List[Cisterna]:
        """Obtiene todas las cisternas"""
        pass
    
    @abstractmethod
    def obtener_por_tipo(self, tipo: TipoCisterna) -> List[Cisterna]:
        """Obtiene cisternas de un tipo específico"""
        pass
    
    @abstractmethod
    def obtener_por_familia(self, familia_id: str) -> List[Cisterna]:
        """Obtiene cisternas de una familia"""
        pass
    
    @abstractmethod
    def obtener_operativas(self) -> List[Cisterna]:
        """Obtiene cisternas operativas"""
        pass
    
    @abstractmethod
    def obtener_con_nivel_critico(self, porcentaje: float = 20.0) -> List[Cisterna]:
        """Obtiene cisternas con nivel crítico"""
        pass
    
    @abstractmethod
    def obtener_con_nivel_bajo(self, porcentaje: float = 40.0) -> List[Cisterna]:
        """Obtiene cisternas con nivel bajo"""
        pass
    
    @abstractmethod
    def obtener_vacias(self) -> List[Cisterna]:
        """Obtiene cisternas vacías"""
        pass
    
    @abstractmethod
    def obtener_prioritarias(self) -> List[Cisterna]:
        """Obtiene cisternas prioritarias (escuelas, centros de salud)"""
        pass
    
    @abstractmethod
    def obtener_con_coordenadas(self) -> List[Cisterna]:
        """Obtiene cisternas que tienen coordenadas GPS"""
        pass
    
    @abstractmethod
    def contar_cisternas(self) -> int:
        """Cuenta el total de cisternas"""
        pass
    
    @abstractmethod
    def contar_por_tipo(self, tipo: TipoCisterna) -> int:
        """Cuenta cisternas por tipo"""
        pass
    
    @abstractmethod
    def calcular_capacidad_total(self) -> int:
        """Calcula la capacidad total de almacenamiento"""
        pass
    
    @abstractmethod
    def calcular_nivel_total(self) -> int:
        """Calcula el nivel total actual de agua"""
        pass

"""
LlenadoRepository - Interface (Domain Layer)
Define el contrato para operaciones con llenados.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from src.domain.entities.llenado import Llenado


class LlenadoRepository(ABC):
    """
    Interface que define las operaciones para gestionar llenados.
    """
    
    @abstractmethod
    def guardar(self, llenado: Llenado) -> Llenado:
        """Guarda un nuevo registro de llenado"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, llenado_id: str) -> Optional[Llenado]:
        """Obtiene un llenado por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Llenado]:
        """Obtiene todos los llenados"""
        pass
    
    @abstractmethod
    def obtener_por_cisterna(self, cisterna_id: str) -> List[Llenado]:
        """Obtiene todos los llenados de una cisterna"""
        pass
    
    @abstractmethod
    def obtener_por_fecha(self, fecha: date) -> List[Llenado]:
        """Obtiene llenados de una fecha específica"""
        pass
    
    @abstractmethod
    def obtener_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> List[Llenado]:
        """Obtiene llenados en un rango de fechas"""
        pass
    
    @abstractmethod
    def obtener_por_proveedor(self, proveedor: str) -> List[Llenado]:
        """Obtiene llenados de un proveedor específico"""
        pass
    
    @abstractmethod
    def obtener_ultimo_llenado(self, cisterna_id: str) -> Optional[Llenado]:
        """Obtiene el último llenado de una cisterna"""
        pass
    
    @abstractmethod
    def obtener_ultimos_llenados(self, limite: int = 10) -> List[Llenado]:
        """Obtiene los últimos N llenados"""
        pass
    
    @abstractmethod
    def contar_llenados(self) -> int:
        """Cuenta el total de llenados"""
        pass
    
    @abstractmethod
    def contar_llenados_por_cisterna(self, cisterna_id: str) -> int:
        """Cuenta llenados de una cisterna"""
        pass
    
    @abstractmethod
    def calcular_total_litros(self) -> int:
        """Calcula el total de litros suministrados"""
        pass
    
    @abstractmethod
    def calcular_total_costo(self) -> float:
        """Calcula el costo total de todos los llenados"""
        pass
    
    @abstractmethod
    def calcular_costo_promedio_por_litro(self) -> float:
        """Calcula el costo promedio por litro"""
        pass
    
    @abstractmethod
    def obtener_proveedores(self) -> List[str]:
        """Obtiene lista de proveedores únicos"""
        pass

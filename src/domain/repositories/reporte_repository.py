"""
ReporteRepository - Interface (Domain Layer)
Define el contrato para operaciones con reportes.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date
from src.domain.entities.reporte import Reporte, TipoReporte, Urgencia, EstadoReporte


class ReporteRepository(ABC):
    """
    Interface que define las operaciones para gestionar reportes.
    """
    
    @abstractmethod
    def guardar(self, reporte: Reporte) -> Reporte:
        """Guarda un nuevo reporte"""
        pass
    
    @abstractmethod
    def actualizar(self, reporte: Reporte) -> Reporte:
        """Actualiza un reporte existente"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, reporte_id: str) -> Optional[Reporte]:
        """Obtiene un reporte por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Reporte]:
        """Obtiene todos los reportes"""
        pass
    
    @abstractmethod
    def obtener_por_familia(self, familia_id: str) -> List[Reporte]:
        """Obtiene reportes de una familia"""
        pass
    
    @abstractmethod
    def obtener_por_cisterna(self, cisterna_id: str) -> List[Reporte]:
        """Obtiene reportes relacionados a una cisterna"""
        pass
    
    @abstractmethod
    def obtener_por_tipo(self, tipo: TipoReporte) -> List[Reporte]:
        """Obtiene reportes de un tipo específico"""
        pass
    
    @abstractmethod
    def obtener_por_estado(self, estado: EstadoReporte) -> List[Reporte]:
        """Obtiene reportes con un estado específico"""
        pass
    
    @abstractmethod
    def obtener_por_urgencia(self, urgencia: Urgencia) -> List[Reporte]:
        """Obtiene reportes con una urgencia específica"""
        pass
    
    @abstractmethod
    def obtener_pendientes(self) -> List[Reporte]:
        """Obtiene reportes pendientes"""
        pass
    
    @abstractmethod
    def obtener_urgentes(self) -> List[Reporte]:
        """Obtiene reportes urgentes (alta o crítica)"""
        pass
    
    @abstractmethod
    def obtener_por_fecha(self, fecha: date) -> List[Reporte]:
        """Obtiene reportes de una fecha específica"""
        pass
    
    @abstractmethod
    def obtener_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> List[Reporte]:
        """Obtiene reportes en un rango de fechas"""
        pass
    
    @abstractmethod
    def obtener_ultimos_reportes(self, limite: int = 10) -> List[Reporte]:
        """Obtiene los últimos N reportes"""
        pass
    
    @abstractmethod
    def contar_reportes(self) -> int:
        """Cuenta el total de reportes"""
        pass
    
    @abstractmethod
    def contar_por_estado(self, estado: EstadoReporte) -> int:
        """Cuenta reportes por estado"""
        pass
    
    @abstractmethod
    def contar_por_tipo(self, tipo: TipoReporte) -> int:
        """Cuenta reportes por tipo"""
        pass
    
    @abstractmethod
    def contar_urgentes(self) -> int:
        """Cuenta reportes urgentes"""
        pass

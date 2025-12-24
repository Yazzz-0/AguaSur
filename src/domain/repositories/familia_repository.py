"""
FamiliaRepository - Interface (Domain Layer)
Define el contrato para operaciones con familias.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.familia import Familia


class FamiliaRepository(ABC):
    """
    Interface que define las operaciones para gestionar familias.
    """
    
    @abstractmethod
    def guardar(self, familia: Familia) -> Familia:
        """
        Guarda una nueva familia en la base de datos.
        
        Args:
            familia: Instancia de Familia a guardar
            
        Returns:
            Familia guardada con su ID asignado
        """
        pass
    
    @abstractmethod
    def actualizar(self, familia: Familia) -> Familia:
        """
        Actualiza una familia existente.
        
        Args:
            familia: Familia con los datos actualizados
            
        Returns:
            Familia actualizada
        """
        pass
    
    @abstractmethod
    def eliminar(self, familia_id: str) -> bool:
        """
        Elimina una familia por su ID.
        
        Args:
            familia_id: ID de la familia a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        pass
    
    @abstractmethod
    def obtener_por_id(self, familia_id: str) -> Optional[Familia]:
        """
        Obtiene una familia por su ID.
        
        Args:
            familia_id: ID de la familia
            
        Returns:
            Familia si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def obtener_todas(self) -> List[Familia]:
        """
        Obtiene todas las familias registradas.
        
        Returns:
            Lista de todas las familias
        """
        pass
    
    @abstractmethod
    def obtener_activas(self) -> List[Familia]:
        """
        Obtiene todas las familias activas.
        
        Returns:
            Lista de familias activas
        """
        pass
    
    @abstractmethod
    def obtener_por_zona(self, zona: str) -> List[Familia]:
        """
        Obtiene familias de una zona específica.
        
        Args:
            zona: Nombre de la zona
            
        Returns:
            Lista de familias de esa zona
        """
        pass
    
    @abstractmethod
    def obtener_con_cisterna(self) -> List[Familia]:
        """
        Obtiene familias que tienen cisterna propia.
        
        Returns:
            Lista de familias con cisterna
        """
        pass
    
    @abstractmethod
    def obtener_sin_cisterna(self) -> List[Familia]:
        """
        Obtiene familias que NO tienen cisterna propia.
        
        Returns:
            Lista de familias sin cisterna
        """
        pass
    
    @abstractmethod
    def buscar_por_direccion(self, direccion: str) -> List[Familia]:
        """
        Busca familias por dirección (búsqueda parcial).
        
        Args:
            direccion: Texto a buscar en la dirección
            
        Returns:
            Lista de familias que coinciden
        """
        pass
    
    @abstractmethod
    def buscar_por_contacto(self, contacto: str) -> Optional[Familia]:
        """
        Busca una familia por su contacto.
        
        Args:
            contacto: Contacto a buscar
            
        Returns:
            Familia si existe, None en caso contrario
        """
        pass
    
    @abstractmethod
    def contar_familias(self) -> int:
        """
        Cuenta el número total de familias.
        
        Returns:
            Número de familias
        """
        pass
    
    @abstractmethod
    def contar_por_zona(self, zona: str) -> int:
        """
        Cuenta familias por zona.
        
        Args:
            zona: Nombre de la zona
            
        Returns:
            Número de familias en esa zona
        """
        pass
    
    @abstractmethod
    def obtener_zonas(self) -> List[str]:
        """
        Obtiene todas las zonas únicas.
        
        Returns:
            Lista de nombres de zonas
        """
        pass

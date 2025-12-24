"""
Entidad Familia - Domain Layer
Representa una familia u hogar en el sistema AguaSur.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Familia:
    """
    Entidad que representa una familia/hogar registrado en el sistema.
    
    Atributos:
        direccion: Dirección completa del hogar
        num_personas: Cantidad de personas en el hogar
        contacto: Teléfono o usuario de Telegram
        capacidad_almacenamiento: Capacidad total en litros
        tiene_cisterna: Si tiene cisterna propia
        zona: Zona dentro de la Zona Sud
        consumo_promedio_diario: Litros por día (calculado)
        id: ID de MongoDB (opcional)
        fecha_registro: Fecha de registro en el sistema
        activo: Si la familia está activa en el sistema
    """
    direccion: str
    num_personas: int
    contacto: str
    capacidad_almacenamiento: int  # litros
    tiene_cisterna: bool
    zona: str
    consumo_promedio_diario: Optional[float] = None
    id: Optional[str] = None
    fecha_registro: Optional[datetime] = None
    activo: bool = True
    
    def __post_init__(self):
        """Validaciones después de inicializar"""
        if not self.direccion or not self.direccion.strip():
            raise ValueError("La dirección no puede estar vacía")
        
        if self.num_personas <= 0:
            raise ValueError("El número de personas debe ser mayor a 0")
        
        if self.capacidad_almacenamiento <= 0:
            raise ValueError("La capacidad de almacenamiento debe ser mayor a 0")
        
        if not self.contacto or not self.contacto.strip():
            raise ValueError("El contacto no puede estar vacío")
        
        # Normalizar datos
        self.direccion = self.direccion.strip()
        self.contacto = self.contacto.strip()
        self.zona = self.zona.strip()
        
        # Si no se proporciona fecha, usar la actual
        if self.fecha_registro is None:
            self.fecha_registro = datetime.now()
        
        # Calcular consumo promedio si no se proporcionó
        if self.consumo_promedio_diario is None:
            self.consumo_promedio_diario = self.calcular_consumo_estimado()
    
    def calcular_consumo_estimado(self) -> float:
        """
        Calcula el consumo promedio diario estimado.
        Basado en: ~50 litros por persona por día (estándar OMS mínimo).
        
        Returns:
            Consumo estimado en litros por día
        """
        LITROS_POR_PERSONA_DIA = 50
        return self.num_personas * LITROS_POR_PERSONA_DIA
    
    def dias_autonomia(self, litros_actuales: float) -> float:
        """
        Calcula cuántos días de autonomía tiene con la cantidad actual de agua.
        
        Args:
            litros_actuales: Litros disponibles actualmente
            
        Returns:
            Días de autonomía estimados
        """
        if self.consumo_promedio_diario <= 0:
            return 0.0
        
        return litros_actuales / self.consumo_promedio_diario
    
    def necesita_agua_urgente(self, litros_actuales: float, dias_minimos: float = 2.0) -> bool:
        """
        Verifica si la familia necesita agua urgentemente.
        
        Args:
            litros_actuales: Litros disponibles actualmente
            dias_minimos: Días mínimos de autonomía antes de considerar urgente
            
        Returns:
            True si necesita agua urgente, False en caso contrario
        """
        dias = self.dias_autonomia(litros_actuales)
        return dias < dias_minimos
    
    def actualizar_consumo(self, nuevo_consumo: float) -> None:
        """
        Actualiza el consumo promedio diario.
        
        Args:
            nuevo_consumo: Nuevo consumo promedio en litros/día
            
        Raises:
            ValueError: Si el consumo es negativo
        """
        if nuevo_consumo < 0:
            raise ValueError("El consumo no puede ser negativo")
        
        self.consumo_promedio_diario = nuevo_consumo
    
    def desactivar(self) -> None:
        """Desactiva la familia del sistema"""
        self.activo = False
    
    def activar(self) -> None:
        """Activa la familia en el sistema"""
        self.activo = True
    
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario (para MongoDB).
        
        Returns:
            Diccionario con los datos de la familia
        """
        data = {
            'direccion': self.direccion,
            'num_personas': self.num_personas,
            'contacto': self.contacto,
            'capacidad_almacenamiento': self.capacidad_almacenamiento,
            'tiene_cisterna': self.tiene_cisterna,
            'zona': self.zona,
            'consumo_promedio_diario': self.consumo_promedio_diario,
            'fecha_registro': self.fecha_registro,
            'activo': self.activo
        }
        
        if self.id:
            data['_id'] = self.id
        
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Familia':
        """
        Crea una instancia de Familia desde un diccionario (desde MongoDB).
        
        Args:
            data: Diccionario con los datos de la familia
            
        Returns:
            Instancia de Familia
        """
        return cls(
            direccion=data['direccion'],
            num_personas=data['num_personas'],
            contacto=data['contacto'],
            capacidad_almacenamiento=data['capacidad_almacenamiento'],
            tiene_cisterna=data['tiene_cisterna'],
            zona=data['zona'],
            consumo_promedio_diario=data.get('consumo_promedio_diario'),
            id=str(data.get('_id', '')),
            fecha_registro=data.get('fecha_registro'),
            activo=data.get('activo', True)
        )
    
    def __str__(self) -> str:
        """Representación en string de la familia"""
        return f"Familia({self.direccion}, {self.num_personas} personas, Zona: {self.zona})"
    
    def __repr__(self) -> str:
        """Representación detallada de la familia"""
        return (
            f"Familia(direccion='{self.direccion}', num_personas={self.num_personas}, "
            f"capacidad={self.capacidad_almacenamiento}L, consumo={self.consumo_promedio_diario:.1f}L/día)"
        )

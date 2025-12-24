"""
Caso de Uso: Registrar Familia
Coordina la lógica para registrar una nueva familia en el sistema.
"""

from src.domain.entities.familia import Familia
from src.domain.repositories.familia_repository import FamiliaRepository


class RegistrarFamilia:
    """
    Caso de uso para registrar una nueva familia.
    """
    
    def __init__(self, familia_repository: FamiliaRepository):
        """
        Inicializa el caso de uso.
        
        Args:
            familia_repository: Repositorio de familias
        """
        self.familia_repo = familia_repository
    
    def ejecutar(
        self,
        direccion: str,
        num_personas: int,
        contacto: str,
        capacidad_almacenamiento: int,
        tiene_cisterna: bool,
        zona: str,
        consumo_promedio_diario: float = None
    ) -> Familia:
        """
        Ejecuta el caso de uso para registrar una familia.
        
        Args:
            direccion: Dirección completa del hogar
            num_personas: Cantidad de personas en el hogar
            contacto: Teléfono o usuario de Telegram
            capacidad_almacenamiento: Capacidad total en litros
            tiene_cisterna: Si tiene cisterna propia
            zona: Zona dentro de la Zona Sud
            consumo_promedio_diario: Consumo promedio (opcional)
            
        Returns:
            Familia creada y guardada
            
        Raises:
            ValueError: Si el contacto ya existe o los datos son inválidos
        """
        # 1. Validar que el contacto no exista
        familia_existente = self.familia_repo.buscar_por_contacto(contacto)
        if familia_existente:
            raise ValueError(f"Ya existe una familia registrada con el contacto: {contacto}")
        
        # 2. Crear la entidad Familia (validaciones en el constructor)
        familia = Familia(
            direccion=direccion,
            num_personas=num_personas,
            contacto=contacto,
            capacidad_almacenamiento=capacidad_almacenamiento,
            tiene_cisterna=tiene_cisterna,
            zona=zona,
            consumo_promedio_diario=consumo_promedio_diario
        )
        
        # 3. Guardar en el repositorio
        familia_guardada = self.familia_repo.guardar(familia)
        
        return familia_guardada

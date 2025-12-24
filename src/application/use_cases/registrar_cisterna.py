"""
Caso de Uso: Registrar Cisterna
Coordina la lógica para registrar una nueva cisterna.
"""

from typing import Optional
from src.domain.entities.cisterna import Cisterna, TipoCisterna, EstadoCisterna
from src.domain.repositories.cisterna_repository import CisternaRepository
from src.domain.repositories.familia_repository import FamiliaRepository


class RegistrarCisterna:
    """
    Caso de uso para registrar una nueva cisterna.
    """
    
    def __init__(
        self,
        cisterna_repository: CisternaRepository,
        familia_repository: FamiliaRepository
    ):
        """
        Inicializa el caso de uso.
        
        Args:
            cisterna_repository: Repositorio de cisternas
            familia_repository: Repositorio de familias
        """
        self.cisterna_repo = cisterna_repository
        self.familia_repo = familia_repository
    
    def ejecutar(
        self,
        ubicacion: str,
        tipo: str,
        capacidad_total: int,
        nivel_actual: int = 0,
        latitud: Optional[float] = None,
        longitud: Optional[float] = None,
        familia_id: Optional[str] = None
    ) -> Cisterna:
        """
        Ejecuta el caso de uso para registrar una cisterna.
        
        Args:
            ubicacion: Dirección o descripción de ubicación
            tipo: Tipo de cisterna (familiar, comunitaria, escolar, centro_salud)
            capacidad_total: Capacidad máxima en litros
            nivel_actual: Nivel inicial en litros
            latitud: Coordenada de latitud (opcional)
            longitud: Coordenada de longitud (opcional)
            familia_id: ID de la familia propietaria (si es familiar)
            
        Returns:
            Cisterna creada y guardada
            
        Raises:
            ValueError: Si los datos son inválidos o la familia no existe
        """
        # 1. Validar tipo
        try:
            tipo_cisterna = TipoCisterna(tipo)
        except ValueError:
            raise ValueError(
                f"Tipo de cisterna inválido: {tipo}. "
                f"Valores válidos: {[t.value for t in TipoCisterna]}"
            )
        
        # 2. Si es cisterna familiar, validar que la familia exista
        if tipo_cisterna == TipoCisterna.FAMILIAR and familia_id:
            familia = self.familia_repo.obtener_por_id(familia_id)
            if not familia:
                raise ValueError(f"No se encontró la familia con ID: {familia_id}")
            
            if not familia.tiene_cisterna:
                # Actualizar familia para indicar que ahora tiene cisterna
                familia.tiene_cisterna = True
                self.familia_repo.actualizar(familia)
        
        # 3. Crear la entidad Cisterna
        cisterna = Cisterna(
            ubicacion=ubicacion,
            tipo=tipo_cisterna,
            capacidad_total=capacidad_total,
            nivel_actual=nivel_actual,
            latitud=latitud,
            longitud=longitud,
            familia_id=familia_id,
            estado=EstadoCisterna.OPERATIVA
        )
        
        # 4. Guardar en el repositorio
        cisterna_guardada = self.cisterna_repo.guardar(cisterna)
        
        return cisterna_guardada

"""
Caso de Uso: Registrar Llenado
Coordina la lógica para registrar un llenado de cisterna.
"""

from typing import Optional
from src.domain.entities.llenado import Llenado
from src.domain.repositories.llenado_repository import LlenadoRepository
from src.domain.repositories.cisterna_repository import CisternaRepository


class RegistrarLlenado:
    """
    Caso de uso para registrar un llenado de cisterna.
    Este caso de uso:
    1. Registra el llenado
    2. Actualiza el nivel de la cisterna
    """
    
    def __init__(
        self,
        llenado_repository: LlenadoRepository,
        cisterna_repository: CisternaRepository
    ):
        """
        Inicializa el caso de uso.
        
        Args:
            llenado_repository: Repositorio de llenados
            cisterna_repository: Repositorio de cisternas
        """
        self.llenado_repo = llenado_repository
        self.cisterna_repo = cisterna_repository
    
    def ejecutar(
        self,
        cisterna_id: str,
        litros_suministrados: int,
        costo: float,
        proveedor: str,
        observaciones: Optional[str] = None
    ) -> Llenado:
        """
        Ejecuta el caso de uso para registrar un llenado.
        
        Args:
            cisterna_id: ID de la cisterna a llenar
            litros_suministrados: Cantidad de litros agregados
            costo: Costo del llenado en bolivianos
            proveedor: Nombre del proveedor
            observaciones: Observaciones adicionales (opcional)
            
        Returns:
            Llenado registrado
            
        Raises:
            ValueError: Si la cisterna no existe o los datos son inválidos
        """
        # 1. Obtener la cisterna
        cisterna = self.cisterna_repo.obtener_por_id(cisterna_id)
        if not cisterna:
            raise ValueError(f"No se encontró la cisterna con ID: {cisterna_id}")
        
        # 2. Verificar que la cisterna esté operativa
        if not cisterna.estado.value == "operativa":
            raise ValueError(
                f"La cisterna no está operativa. Estado actual: {cisterna.estado.value}"
            )
        
        # 3. Guardar nivel anterior
        nivel_anterior = cisterna.nivel_actual
        
        # 4. Llenar la cisterna (esto actualiza el nivel)
        cisterna.llenar(litros_suministrados)
        nivel_posterior = cisterna.nivel_actual
        
        # 5. Crear el registro de llenado
        llenado = Llenado(
            cisterna_id=cisterna_id,
            litros_suministrados=litros_suministrados,
            costo=costo,
            proveedor=proveedor,
            nivel_anterior=nivel_anterior,
            nivel_posterior=nivel_posterior,
            observaciones=observaciones
        )
        
        # 6. Guardar el llenado
        llenado_guardado = self.llenado_repo.guardar(llenado)
        
        # 7. Actualizar la cisterna con el nuevo nivel
        self.cisterna_repo.actualizar(cisterna)
        
        return llenado_guardado

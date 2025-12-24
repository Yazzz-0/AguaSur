"""
Caso de Uso: Crear Reporte
Coordina la lógica para crear un reporte de problema o solicitud.
"""

from typing import Optional
from src.domain.entities.reporte import Reporte, TipoReporte, Urgencia, EstadoReporte
from src.domain.repositories.reporte_repository import ReporteRepository
from src.domain.repositories.familia_repository import FamiliaRepository
from src.domain.repositories.cisterna_repository import CisternaRepository


class CrearReporte:
    """
    Caso de uso para crear un nuevo reporte.
    """
    
    def __init__(
        self,
        reporte_repository: ReporteRepository,
        familia_repository: FamiliaRepository,
        cisterna_repository: CisternaRepository
    ):
        """
        Inicializa el caso de uso.
        
        Args:
            reporte_repository: Repositorio de reportes
            familia_repository: Repositorio de familias
            cisterna_repository: Repositorio de cisternas
        """
        self.reporte_repo = reporte_repository
        self.familia_repo = familia_repository
        self.cisterna_repo = cisterna_repository
    
    def ejecutar(
        self,
        familia_id: str,
        tipo: str,
        descripcion: str,
        urgencia: str = "media",
        cisterna_id: Optional[str] = None,
        latitud: Optional[float] = None,
        longitud: Optional[float] = None
    ) -> Reporte:
        """
        Ejecuta el caso de uso para crear un reporte.
        
        Args:
            familia_id: ID de la familia que reporta
            tipo: Tipo de reporte
            descripcion: Descripción del problema
            urgencia: Nivel de urgencia (baja, media, alta, critica)
            cisterna_id: ID de cisterna relacionada (opcional)
            latitud: Coordenada si es ubicación específica (opcional)
            longitud: Coordenada si es ubicación específica (opcional)
            
        Returns:
            Reporte creado
            
        Raises:
            ValueError: Si los datos son inválidos o las entidades no existen
        """
        # 1. Validar que la familia exista
        familia = self.familia_repo.obtener_por_id(familia_id)
        if not familia:
            raise ValueError(f"No se encontró la familia con ID: {familia_id}")
        
        # 2. Validar tipo de reporte
        try:
            tipo_reporte = TipoReporte(tipo)
        except ValueError:
            raise ValueError(
                f"Tipo de reporte inválido: {tipo}. "
                f"Valores válidos: {[t.value for t in TipoReporte]}"
            )
        
        # 3. Validar urgencia
        try:
            nivel_urgencia = Urgencia(urgencia)
        except ValueError:
            raise ValueError(
                f"Nivel de urgencia inválido: {urgencia}. "
                f"Valores válidos: {[u.value for u in Urgencia]}"
            )
        
        # 4. Si hay cisterna_id, validar que exista
        if cisterna_id:
            cisterna = self.cisterna_repo.obtener_por_id(cisterna_id)
            if not cisterna:
                raise ValueError(f"No se encontró la cisterna con ID: {cisterna_id}")
        
        # 5. Ajustar urgencia automáticamente según el tipo
        if tipo_reporte == TipoReporte.AGUA_ACABANDOSE:
            # Si el agua se está acabando, al menos urgencia MEDIA
            if nivel_urgencia == Urgencia.BAJA:
                nivel_urgencia = Urgencia.MEDIA
        
        # 6. Crear el reporte
        reporte = Reporte(
            familia_id=familia_id,
            tipo=tipo_reporte,
            descripcion=descripcion,
            urgencia=nivel_urgencia,
            estado=EstadoReporte.PENDIENTE,
            cisterna_id=cisterna_id,
            latitud=latitud,
            longitud=longitud
        )
        
        # 7. Guardar el reporte
        reporte_guardado = self.reporte_repo.guardar(reporte)
        
        return reporte_guardado

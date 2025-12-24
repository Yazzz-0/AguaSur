"""
Caso de Uso: Obtener Dashboard
Coordina la lógica para obtener estadísticas generales del sistema.
"""

from typing import Dict, Any
from src.domain.repositories.familia_repository import FamiliaRepository
from src.domain.repositories.cisterna_repository import CisternaRepository
from src.domain.repositories.llenado_repository import LlenadoRepository
from src.domain.repositories.reporte_repository import ReporteRepository
from src.domain.entities.reporte import EstadoReporte


class ObtenerDashboard:
    """
    Caso de uso para obtener el dashboard con estadísticas del sistema.
    """
    
    def __init__(
        self,
        familia_repository: FamiliaRepository,
        cisterna_repository: CisternaRepository,
        llenado_repository: LlenadoRepository,
        reporte_repository: ReporteRepository
    ):
        """
        Inicializa el caso de uso.
        
        Args:
            familia_repository: Repositorio de familias
            cisterna_repository: Repositorio de cisternas
            llenado_repository: Repositorio de llenados
            reporte_repository: Repositorio de reportes
        """
        self.familia_repo = familia_repository
        self.cisterna_repo = cisterna_repository
        self.llenado_repo = llenado_repository
        self.reporte_repo = reporte_repository
    
    def ejecutar(self) -> Dict[str, Any]:
        """
        Ejecuta el caso de uso para obtener estadísticas.
        
        Returns:
            Diccionario con estadísticas del sistema:
            - Familias registradas
            - Cisternas operativas
            - Nivel total de agua
            - Reportes pendientes
            - Cisternas con nivel crítico
            - Etc.
        """
        # Estadísticas de familias
        total_familias = self.familia_repo.contar_familias()
        familias_activas = len(self.familia_repo.obtener_activas())
        familias_con_cisterna = len(self.familia_repo.obtener_con_cisterna())
        familias_sin_cisterna = len(self.familia_repo.obtener_sin_cisterna())
        
        # Estadísticas de cisternas
        total_cisternas = self.cisterna_repo.contar_cisternas()
        cisternas_operativas = len(self.cisterna_repo.obtener_operativas())
        cisternas_vacias = len(self.cisterna_repo.obtener_vacias())
        cisternas_nivel_critico = len(self.cisterna_repo.obtener_con_nivel_critico())
        cisternas_nivel_bajo = len(self.cisterna_repo.obtener_con_nivel_bajo())
        cisternas_prioritarias = len(self.cisterna_repo.obtener_prioritarias())
        
        capacidad_total = self.cisterna_repo.calcular_capacidad_total()
        nivel_total = self.cisterna_repo.calcular_nivel_total()
        porcentaje_lleno = (nivel_total / capacidad_total * 100) if capacidad_total > 0 else 0
        
        # Estadísticas de llenados
        total_llenados = self.llenado_repo.contar_llenados()
        total_litros_suministrados = self.llenado_repo.calcular_total_litros()
        total_costo_llenados = self.llenado_repo.calcular_total_costo()
        costo_promedio_litro = self.llenado_repo.calcular_costo_promedio_por_litro()
        
        # Estadísticas de reportes
        total_reportes = self.reporte_repo.contar_reportes()
        reportes_pendientes = self.reporte_repo.contar_por_estado(EstadoReporte.PENDIENTE)
        reportes_urgentes = self.reporte_repo.contar_urgentes()
        
        # Alertas
        alertas = []
        
        if cisternas_vacias > 0:
            alertas.append({
                'tipo': 'critico',
                'mensaje': f'{cisternas_vacias} cisterna(s) vacía(s)',
                'cantidad': cisternas_vacias
            })
        
        if cisternas_nivel_critico > 0:
            alertas.append({
                'tipo': 'urgente',
                'mensaje': f'{cisternas_nivel_critico} cisterna(s) con nivel crítico',
                'cantidad': cisternas_nivel_critico
            })
        
        if reportes_urgentes > 0:
            alertas.append({
                'tipo': 'urgente',
                'mensaje': f'{reportes_urgentes} reporte(s) urgente(s) pendiente(s)',
                'cantidad': reportes_urgentes
            })
        
        if cisternas_nivel_bajo > 0:
            alertas.append({
                'tipo': 'advertencia',
                'mensaje': f'{cisternas_nivel_bajo} cisterna(s) con nivel bajo',
                'cantidad': cisternas_nivel_bajo
            })
        
        return {
            'familias': {
                'total': total_familias,
                'activas': familias_activas,
                'con_cisterna': familias_con_cisterna,
                'sin_cisterna': familias_sin_cisterna
            },
            'cisternas': {
                'total': total_cisternas,
                'operativas': cisternas_operativas,
                'vacias': cisternas_vacias,
                'nivel_critico': cisternas_nivel_critico,
                'nivel_bajo': cisternas_nivel_bajo,
                'prioritarias': cisternas_prioritarias,
                'capacidad_total_litros': capacidad_total,
                'nivel_total_litros': nivel_total,
                'porcentaje_lleno': round(porcentaje_lleno, 2)
            },
            'llenados': {
                'total': total_llenados,
                'litros_suministrados': total_litros_suministrados,
                'costo_total_bs': round(total_costo_llenados, 2),
                'costo_promedio_litro_bs': round(costo_promedio_litro, 2)
            },
            'reportes': {
                'total': total_reportes,
                'pendientes': reportes_pendientes,
                'urgentes': reportes_urgentes
            },
            'alertas': alertas
        }

"""
MongoDBReporteRepository - Infrastructure Layer
Implementación del repositorio de reportes usando MongoDB.
"""

from typing import List, Optional
from datetime import date, datetime
from bson import ObjectId
from pymongo.database import Database

from src.domain.entities.reporte import Reporte, TipoReporte, Urgencia, EstadoReporte
from src.domain.repositories.reporte_repository import ReporteRepository


class MongoDBReporteRepository(ReporteRepository):
    """Implementación del repositorio de reportes usando MongoDB"""
    
    def __init__(self, database: Database):
        self.db = database
        self.collection = database['reportes']
    
    def guardar(self, reporte: Reporte) -> Reporte:
        reporte_dict = reporte.to_dict()
        reporte_dict.pop('_id', None)
        result = self.collection.insert_one(reporte_dict)
        reporte.id = str(result.inserted_id)
        return reporte
    
    def actualizar(self, reporte: Reporte) -> Reporte:
        if not reporte.id:
            raise ValueError("El reporte debe tener un ID")
        reporte_dict = reporte.to_dict()
        reporte_dict.pop('_id', None)
        self.collection.update_one(
            {'_id': ObjectId(reporte.id)},
            {'$set': reporte_dict}
        )
        return reporte
    
    def obtener_por_id(self, reporte_id: str) -> Optional[Reporte]:
        doc = self.collection.find_one({'_id': ObjectId(reporte_id)})
        return Reporte.from_dict(doc) if doc else None
    
    def obtener_todos(self) -> List[Reporte]:
        docs = self.collection.find().sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_por_familia(self, familia_id: str) -> List[Reporte]:
        docs = self.collection.find({'familia_id': familia_id}).sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_por_cisterna(self, cisterna_id: str) -> List[Reporte]:
        docs = self.collection.find({'cisterna_id': cisterna_id}).sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_por_tipo(self, tipo: TipoReporte) -> List[Reporte]:
        docs = self.collection.find({'tipo': tipo.value}).sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_por_estado(self, estado: EstadoReporte) -> List[Reporte]:
        docs = self.collection.find({'estado': estado.value}).sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_por_urgencia(self, urgencia: Urgencia) -> List[Reporte]:
        docs = self.collection.find({'urgencia': urgencia.value}).sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_pendientes(self) -> List[Reporte]:
        docs = self.collection.find({'estado': EstadoReporte.PENDIENTE.value}).sort('urgencia', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_urgentes(self) -> List[Reporte]:
        docs = self.collection.find({
            'urgencia': {'$in': [Urgencia.ALTA.value, Urgencia.CRITICA.value]},
            'estado': {'$in': [EstadoReporte.PENDIENTE.value, EstadoReporte.EN_REVISION.value]}
        }).sort('urgencia', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_por_fecha(self, fecha: date) -> List[Reporte]:
        inicio = datetime.combine(fecha, datetime.min.time())
        fin = datetime.combine(fecha, datetime.max.time())
        docs = self.collection.find({
            'fecha_reporte': {'$gte': inicio, '$lte': fin}
        }).sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> List[Reporte]:
        inicio = datetime.combine(fecha_inicio, datetime.min.time())
        fin = datetime.combine(fecha_fin, datetime.max.time())
        docs = self.collection.find({
            'fecha_reporte': {'$gte': inicio, '$lte': fin}
        }).sort('fecha_reporte', -1)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def obtener_ultimos_reportes(self, limite: int = 10) -> List[Reporte]:
        docs = self.collection.find().sort('fecha_reporte', -1).limit(limite)
        return [Reporte.from_dict(doc) for doc in docs]
    
    def contar_reportes(self) -> int:
        return self.collection.count_documents({})
    
    def contar_por_estado(self, estado: EstadoReporte) -> int:
        return self.collection.count_documents({'estado': estado.value})
    
    def contar_por_tipo(self, tipo: TipoReporte) -> int:
        return self.collection.count_documents({'tipo': tipo.value})
    
    def contar_urgentes(self) -> int:
        return self.collection.count_documents({
            'urgencia': {'$in': [Urgencia.ALTA.value, Urgencia.CRITICA.value]},
            'estado': {'$in': [EstadoReporte.PENDIENTE.value, EstadoReporte.EN_REVISION.value]}
        })

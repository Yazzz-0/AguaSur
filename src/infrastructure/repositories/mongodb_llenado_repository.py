"""
MongoDBLlenadoRepository - Infrastructure Layer
Implementación del repositorio de llenados usando MongoDB.
"""

from typing import List, Optional
from datetime import date, datetime, timedelta
from bson import ObjectId
from pymongo.database import Database

from src.domain.entities.llenado import Llenado
from src.domain.repositories.llenado_repository import LlenadoRepository


class MongoDBLlenadoRepository(LlenadoRepository):
    """Implementación del repositorio de llenados usando MongoDB"""
    
    def __init__(self, database: Database):
        self.db = database
        self.collection = database['llenados']
    
    def guardar(self, llenado: Llenado) -> Llenado:
        llenado_dict = llenado.to_dict()
        llenado_dict.pop('_id', None)
        result = self.collection.insert_one(llenado_dict)
        llenado.id = str(result.inserted_id)
        return llenado
    
    def obtener_por_id(self, llenado_id: str) -> Optional[Llenado]:
        doc = self.collection.find_one({'_id': ObjectId(llenado_id)})
        return Llenado.from_dict(doc) if doc else None
    
    def obtener_todos(self) -> List[Llenado]:
        docs = self.collection.find().sort('fecha', -1)
        return [Llenado.from_dict(doc) for doc in docs]
    
    def obtener_por_cisterna(self, cisterna_id: str) -> List[Llenado]:
        docs = self.collection.find({'cisterna_id': cisterna_id}).sort('fecha', -1)
        return [Llenado.from_dict(doc) for doc in docs]
    
    def obtener_por_fecha(self, fecha: date) -> List[Llenado]:
        inicio = datetime.combine(fecha, datetime.min.time())
        fin = datetime.combine(fecha, datetime.max.time())
        docs = self.collection.find({
            'fecha': {'$gte': inicio, '$lte': fin}
        }).sort('fecha', -1)
        return [Llenado.from_dict(doc) for doc in docs]
    
    def obtener_por_rango_fechas(self, fecha_inicio: date, fecha_fin: date) -> List[Llenado]:
        inicio = datetime.combine(fecha_inicio, datetime.min.time())
        fin = datetime.combine(fecha_fin, datetime.max.time())
        docs = self.collection.find({
            'fecha': {'$gte': inicio, '$lte': fin}
        }).sort('fecha', -1)
        return [Llenado.from_dict(doc) for doc in docs]
    
    def obtener_por_proveedor(self, proveedor: str) -> List[Llenado]:
        docs = self.collection.find({'proveedor': proveedor}).sort('fecha', -1)
        return [Llenado.from_dict(doc) for doc in docs]
    
    def obtener_ultimo_llenado(self, cisterna_id: str) -> Optional[Llenado]:
        doc = self.collection.find_one(
            {'cisterna_id': cisterna_id},
            sort=[('fecha', -1)]
        )
        return Llenado.from_dict(doc) if doc else None
    
    def obtener_ultimos_llenados(self, limite: int = 10) -> List[Llenado]:
        docs = self.collection.find().sort('fecha', -1).limit(limite)
        return [Llenado.from_dict(doc) for doc in docs]
    
    def contar_llenados(self) -> int:
        return self.collection.count_documents({})
    
    def contar_llenados_por_cisterna(self, cisterna_id: str) -> int:
        return self.collection.count_documents({'cisterna_id': cisterna_id})
    
    def calcular_total_litros(self) -> int:
        pipeline = [
            {'$group': {'_id': None, 'total': {'$sum': '$litros_suministrados'}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]['total'] if result else 0
    
    def calcular_total_costo(self) -> float:
        pipeline = [
            {'$group': {'_id': None, 'total': {'$sum': '$costo'}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return float(result[0]['total']) if result else 0.0
    
    def calcular_costo_promedio_por_litro(self) -> float:
        total_costo = self.calcular_total_costo()
        total_litros = self.calcular_total_litros()
        return total_costo / total_litros if total_litros > 0 else 0.0
    
    def obtener_proveedores(self) -> List[str]:
        return sorted(self.collection.distinct('proveedor'))

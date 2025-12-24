"""
MongoDBCisternaRepository - Infrastructure Layer
Implementación del repositorio de cisternas usando MongoDB.
"""

from typing import List, Optional
from bson import ObjectId
from pymongo.database import Database

from src.domain.entities.cisterna import Cisterna, TipoCisterna, EstadoCisterna
from src.domain.repositories.cisterna_repository import CisternaRepository


class MongoDBCisternaRepository(CisternaRepository):
    """Implementación del repositorio de cisternas usando MongoDB"""
    
    def __init__(self, database: Database):
        self.db = database
        self.collection = database['cisternas']
    
    def guardar(self, cisterna: Cisterna) -> Cisterna:
        cisterna_dict = cisterna.to_dict()
        cisterna_dict.pop('_id', None)
        result = self.collection.insert_one(cisterna_dict)
        cisterna.id = str(result.inserted_id)
        return cisterna
    
    def actualizar(self, cisterna: Cisterna) -> Cisterna:
        if not cisterna.id:
            raise ValueError("La cisterna debe tener un ID")
        cisterna_dict = cisterna.to_dict()
        cisterna_dict.pop('_id', None)
        self.collection.update_one(
            {'_id': ObjectId(cisterna.id)},
            {'$set': cisterna_dict}
        )
        return cisterna
    
    def eliminar(self, cisterna_id: str) -> bool:
        result = self.collection.delete_one({'_id': ObjectId(cisterna_id)})
        return result.deleted_count > 0
    
    def obtener_por_id(self, cisterna_id: str) -> Optional[Cisterna]:
        doc = self.collection.find_one({'_id': ObjectId(cisterna_id)})
        return Cisterna.from_dict(doc) if doc else None
    
    def obtener_todas(self) -> List[Cisterna]:
        docs = self.collection.find().sort('ubicacion', 1)
        return [Cisterna.from_dict(doc) for doc in docs]
    
    def obtener_por_tipo(self, tipo: TipoCisterna) -> List[Cisterna]:
        docs = self.collection.find({'tipo': tipo.value})
        return [Cisterna.from_dict(doc) for doc in docs]
    
    def obtener_por_familia(self, familia_id: str) -> List[Cisterna]:
        docs = self.collection.find({'familia_id': familia_id})
        return [Cisterna.from_dict(doc) for doc in docs]
    
    def obtener_operativas(self) -> List[Cisterna]:
        docs = self.collection.find({'estado': EstadoCisterna.OPERATIVA.value})
        return [Cisterna.from_dict(doc) for doc in docs]
    
    def obtener_con_nivel_critico(self, porcentaje: float = 20.0) -> List[Cisterna]:
        docs = self.collection.find({'estado': EstadoCisterna.OPERATIVA.value})
        cisternas = [Cisterna.from_dict(doc) for doc in docs]
        return [c for c in cisternas if c.nivel_critico(porcentaje)]
    
    def obtener_con_nivel_bajo(self, porcentaje: float = 40.0) -> List[Cisterna]:
        docs = self.collection.find({'estado': EstadoCisterna.OPERATIVA.value})
        cisternas = [Cisterna.from_dict(doc) for doc in docs]
        return [c for c in cisternas if c.nivel_bajo(porcentaje)]
    
    def obtener_vacias(self) -> List[Cisterna]:
        docs = self.collection.find({'nivel_actual': 0})
        return [Cisterna.from_dict(doc) for doc in docs]
    
    def obtener_prioritarias(self) -> List[Cisterna]:
        docs = self.collection.find({
            'tipo': {'$in': [TipoCisterna.ESCOLAR.value, TipoCisterna.CENTRO_SALUD.value]}
        })
        return [Cisterna.from_dict(doc) for doc in docs]
    
    def obtener_con_coordenadas(self) -> List[Cisterna]:
        docs = self.collection.find({
            'latitud': {'$ne': None},
            'longitud': {'$ne': None}
        })
        return [Cisterna.from_dict(doc) for doc in docs]
    
    def contar_cisternas(self) -> int:
        return self.collection.count_documents({})
    
    def contar_por_tipo(self, tipo: TipoCisterna) -> int:
        return self.collection.count_documents({'tipo': tipo.value})
    
    def calcular_capacidad_total(self) -> int:
        pipeline = [
            {'$group': {'_id': None, 'total': {'$sum': '$capacidad_total'}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]['total'] if result else 0
    
    def calcular_nivel_total(self) -> int:
        pipeline = [
            {'$group': {'_id': None, 'total': {'$sum': '$nivel_actual'}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]['total'] if result else 0

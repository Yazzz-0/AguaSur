"""
MongoDBFamiliaRepository - Infrastructure Layer
Implementación del repositorio de familias usando MongoDB.
"""

from typing import List, Optional
from bson import ObjectId
from pymongo.database import Database

from src.domain.entities.familia import Familia
from src.domain.repositories.familia_repository import FamiliaRepository


class MongoDBFamiliaRepository(FamiliaRepository):
    """Implementación del repositorio de familias usando MongoDB"""
    
    def __init__(self, database: Database):
        self.db = database
        self.collection = database['familias']
    
    def guardar(self, familia: Familia) -> Familia:
        familia_dict = familia.to_dict()
        familia_dict.pop('_id', None)
        result = self.collection.insert_one(familia_dict)
        familia.id = str(result.inserted_id)
        return familia
    
    def actualizar(self, familia: Familia) -> Familia:
        if not familia.id:
            raise ValueError("La familia debe tener un ID")
        familia_dict = familia.to_dict()
        familia_dict.pop('_id', None)
        self.collection.update_one(
            {'_id': ObjectId(familia.id)},
            {'$set': familia_dict}
        )
        return familia
    
    def eliminar(self, familia_id: str) -> bool:
        result = self.collection.delete_one({'_id': ObjectId(familia_id)})
        return result.deleted_count > 0
    
    def obtener_por_id(self, familia_id: str) -> Optional[Familia]:
        doc = self.collection.find_one({'_id': ObjectId(familia_id)})
        return Familia.from_dict(doc) if doc else None
    
    def obtener_todas(self) -> List[Familia]:
        docs = self.collection.find().sort('direccion', 1)
        return [Familia.from_dict(doc) for doc in docs]
    
    def obtener_activas(self) -> List[Familia]:
        docs = self.collection.find({'activo': True}).sort('direccion', 1)
        return [Familia.from_dict(doc) for doc in docs]
    
    def obtener_por_zona(self, zona: str) -> List[Familia]:
        docs = self.collection.find({'zona': zona}).sort('direccion', 1)
        return [Familia.from_dict(doc) for doc in docs]
    
    def obtener_con_cisterna(self) -> List[Familia]:
        docs = self.collection.find({'tiene_cisterna': True})
        return [Familia.from_dict(doc) for doc in docs]
    
    def obtener_sin_cisterna(self) -> List[Familia]:
        docs = self.collection.find({'tiene_cisterna': False})
        return [Familia.from_dict(doc) for doc in docs]
    
    def buscar_por_direccion(self, direccion: str) -> List[Familia]:
        docs = self.collection.find({
            'direccion': {'$regex': direccion, '$options': 'i'}
        })
        return [Familia.from_dict(doc) for doc in docs]
    
    def buscar_por_contacto(self, contacto: str) -> Optional[Familia]:
        doc = self.collection.find_one({'contacto': contacto})
        return Familia.from_dict(doc) if doc else None
    
    def contar_familias(self) -> int:
        return self.collection.count_documents({})
    
    def contar_por_zona(self, zona: str) -> int:
        return self.collection.count_documents({'zona': zona})
    
    def obtener_zonas(self) -> List[str]:
        return sorted(self.collection.distinct('zona'))

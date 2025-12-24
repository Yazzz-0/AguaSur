"""
MongoDB Connection - Infrastructure Layer
Implementa un patrón Singleton para la conexión a MongoDB.
"""

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import os
from typing import Optional


class MongoDBConnection:
    """
    Singleton para gestionar la conexión a MongoDB.
    Garantiza que solo exista una única conexión en toda la aplicación.
    """
    
    _instance: Optional['MongoDBConnection'] = None
    _client: Optional[MongoClient] = None
    _database: Optional[Database] = None
    
    def __new__(cls):
        """Implementación del patrón Singleton"""
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa la conexión (solo se ejecuta una vez)"""
        if self._client is None:
            self._connect()
    
    def _connect(self) -> None:
        """Establece la conexión con MongoDB"""
        load_dotenv()
        
        mongodb_uri = os.getenv('MONGODB_URI')
        database_name = os.getenv('DATABASE_NAME', 'aguasur_db')
        
        if not mongodb_uri:
            raise ValueError(
                "MONGODB_URI no encontrada en el archivo .env. "
                "Por favor, configura tu connection string de MongoDB Atlas."
            )
        
        try:
            self._client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000
            )
            
            self._client.admin.command('ping')
            self._database = self._client[database_name]
            
            print(f"✅ Conexión exitosa a MongoDB - Base de datos: {database_name}")
            
            self._crear_indices()
            
        except ServerSelectionTimeoutError:
            raise ConnectionFailure(
                "No se pudo conectar a MongoDB. Verifica tu connection string y conexión a internet."
            )
        except Exception as e:
            raise ConnectionFailure(f"Error al conectar a MongoDB: {str(e)}")
    
    def _crear_indices(self) -> None:
        """Crea índices en las colecciones para mejorar el rendimiento"""
        try:
            # Índices para familias
            self._database.familias.create_index('contacto', unique=True)
            self._database.familias.create_index('zona')
            self._database.familias.create_index('activo')
            
            # Índices para cisternas
            self._database.cisternas.create_index('tipo')
            self._database.cisternas.create_index('estado')
            self._database.cisternas.create_index('familia_id')
            
            # Índices para llenados
            self._database.llenados.create_index('cisterna_id')
            self._database.llenados.create_index('fecha')
            
            # Índices para reportes
            self._database.reportes.create_index('familia_id')
            self._database.reportes.create_index('estado')
            self._database.reportes.create_index('urgencia')
            self._database.reportes.create_index('fecha_reporte')
            
            print("✅ Índices de MongoDB creados correctamente")
            
        except Exception as e:
            print(f"⚠️ Advertencia al crear índices: {str(e)}")
    
    def get_database(self) -> Database:
        """Obtiene la instancia de la base de datos"""
        if self._database is None:
            raise ConnectionFailure("No hay conexión a MongoDB.")
        return self._database
    
    def get_client(self) -> MongoClient:
        """Obtiene el cliente de MongoDB"""
        if self._client is None:
            raise ConnectionFailure("No hay conexión a MongoDB.")
        return self._client
    
    def close(self) -> None:
        """Cierra la conexión a MongoDB"""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None
            print("✅ Conexión a MongoDB cerrada")
    
    def is_connected(self) -> bool:
        """Verifica si hay una conexión activa"""
        if self._client is None:
            return False
        try:
            self._client.admin.command('ping')
            return True
        except Exception:
            return False
    
    @classmethod
    def get_instance(cls) -> 'MongoDBConnection':
        """Obtiene la instancia única"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_database() -> Database:
    """Función helper para obtener la base de datos"""
    connection = MongoDBConnection.get_instance()
    return connection.get_database()


def close_connection() -> None:
    """Función helper para cerrar la conexión"""
    connection = MongoDBConnection.get_instance()
    connection.close()

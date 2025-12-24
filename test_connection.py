"""
Script para probar la conexión a MongoDB.
"""

from src.infrastructure.database import get_database, MongoDBConnection

def main():
    print("🔄 Probando conexión a MongoDB para AguaSur...")
    print("-" * 50)
    
    try:
        connection = MongoDBConnection.get_instance()
        
        if connection.is_connected():
            print("✅ Conexión establecida correctamente")
            
            db = get_database()
            
            print(f"📂 Base de datos: {db.name}")
            print(f"📋 Colecciones existentes: {db.list_collection_names()}")
            
            # Prueba básica
            test_collection = db['test']
            result = test_collection.insert_one({'mensaje': '¡AguaSur funciona!'})
            print(f"✅ Documento de prueba insertado con ID: {result.inserted_id}")
            
            documento = test_collection.find_one({'_id': result.inserted_id})
            print(f"📄 Documento leído: {documento}")
            
            test_collection.delete_one({'_id': result.inserted_id})
            print("🗑️ Documento de prueba eliminado")
            
            print("\n" + "=" * 50)
            print("✅ ¡Todas las pruebas pasaron correctamente!")
            print("=" * 50)
            
        else:
            print("❌ No se pudo establecer conexión")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

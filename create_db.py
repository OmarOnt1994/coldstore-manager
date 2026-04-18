"""Script para crear la base de datos en PostgreSQL"""
from sqlalchemy import create_engine, text
import psycopg2

try:
    # Conectar directamente con psycopg2 (sin SQLAlchemy para evitar transacciones)
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="1234",
        database="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Verificar si la BD ya existe
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'coldstore_db'")
    
    if cursor.fetchone() is None:
        # Crear la BD
        cursor.execute("CREATE DATABASE coldstore_db")
        print("✅ Base de datos 'coldstore_db' creada exitosamente")
    else:
        print("ℹ️  La base de datos 'coldstore_db' ya existe")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n¿PostgreSQL está corriendo? Verifica que el servicio esté iniciado.")


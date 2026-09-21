import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "ERP Agrícola API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Configuración de Base de Datos MySQL
    MYSQL_USER: str = os.getenv("MYSQL_USER", "agricola_user")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "agricola_password")
    MYSQL_SERVER: str = os.getenv("MYSQL_SERVER", "db")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "erp_agricola")
    
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"

settings = Settings()

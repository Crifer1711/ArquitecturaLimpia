"""Configuración de la aplicación"""
import os
from typing import Literal


class Config:
    """Configuración base de la aplicación"""
    
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    
    # Comunicación externa
    MODO_COMUNICACION: Literal["http", "mensajeria", "hibrido"] = os.getenv(
        "MODO_COMUNICACION", "mensajeria"
    )
    
    # URLs de servicios externos
    PEDIDOS_SERVICE_URL = os.getenv("PEDIDOS_SERVICE_URL", "http://localhost:5001")
    TRANSPORTISTAS_SERVICE_URL = os.getenv(
        "TRANSPORTISTAS_SERVICE_URL",
        "http://localhost:5002"
    )
    
    # RabbitMQ
    RABBITMQ_URL = os.getenv(
        "RABBITMQ_URL",
        "amqp://guest:guest@localhost:5672/"
    )
    USAR_MENSAJERIA_SIMULADA = os.getenv(
        "USAR_MENSAJERIA_SIMULADA",
        "True"
    ).lower() == "true"
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    USAR_MENSAJERIA_SIMULADA = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    USAR_MENSAJERIA_SIMULADA = False


def get_config():
    """Obtiene la configuración según el entorno"""
    env = os.getenv("ENVIRONMENT", "development")
    
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig
    }
    
    return configs.get(env, DevelopmentConfig)

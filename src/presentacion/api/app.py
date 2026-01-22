"""Aplicación Flask - API REST"""
from flask import Flask
from flask_cors import CORS

from ...infraestructura.config import get_config
from ...infraestructura.persistencia import EnvioRepositoryMemoria
from ...infraestructura.http import PedidosHttpClient, TransportistasHttpClient
from ...infraestructura.mensajeria import MensajeriaClient
from ...aplicacion.casos_uso import (
    CrearEnvioUseCase,
    ActualizarEstadoEnvioUseCase,
    ObtenerEnvioUseCase,
    ListarEnviosUseCase,
    AsignarTransportistaUseCase
)
from .controllers import crear_envios_blueprint


def crear_app():
    """Factory para crear la aplicación Flask"""
    
    app = Flask(__name__)
    
    # Cargar configuración
    config = get_config()
    app.config.from_object(config)
    
    # Configurar CORS
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Inicializar dependencias de infraestructura
    envio_repository = EnvioRepositoryMemoria()
    
    # Determinar el modo de comunicación
    if config.MODO_COMUNICACION in ["http", "hibrido"]:
        pedidos_client = PedidosHttpClient(config.PEDIDOS_SERVICE_URL)
        transportistas_client = TransportistasHttpClient(config.TRANSPORTISTAS_SERVICE_URL)
    else:
        pedidos_client = None
        transportistas_client = None
    
    if config.MODO_COMUNICACION in ["mensajeria", "hibrido"]:
        mensajeria_client = MensajeriaClient(
            config.RABBITMQ_URL,
            modo_simulado=config.USAR_MENSAJERIA_SIMULADA
        )
        # Si usamos mensajería, la usamos como notificador
        if config.MODO_COMUNICACION == "mensajeria":
            pedidos_client = mensajeria_client
            transportistas_client = mensajeria_client
    else:
        mensajeria_client = None
    
    # Inicializar casos de uso
    crear_envio_uc = CrearEnvioUseCase(
        envio_repository=envio_repository,
        notificador_pedidos=pedidos_client
    )
    
    actualizar_estado_uc = ActualizarEstadoEnvioUseCase(
        envio_repository=envio_repository,
        notificador_pedidos=pedidos_client
    )
    
    obtener_envio_uc = ObtenerEnvioUseCase(
        envio_repository=envio_repository
    )
    
    listar_envios_uc = ListarEnviosUseCase(
        envio_repository=envio_repository
    )
    
    asignar_transportista_uc = AsignarTransportistaUseCase(
        envio_repository=envio_repository,
        cliente_transportistas=transportistas_client
    )
    
    # Registrar blueprints
    envios_bp = crear_envios_blueprint(
        crear_envio_uc=crear_envio_uc,
        actualizar_estado_uc=actualizar_estado_uc,
        obtener_envio_uc=obtener_envio_uc,
        listar_envios_uc=listar_envios_uc,
        asignar_transportista_uc=asignar_transportista_uc
    )
    
    app.register_blueprint(envios_bp)
    
    # Ruta raíz
    @app.route('/')
    def index():
        return {
            "servicio": "Microservicio de Gestión de Envíos",
            "version": "1.0.0",
            "arquitectura": "Clean Architecture + DDD",
            "endpoints": {
                "health": "/api/envios/health",
                "crear_envio": "POST /api/envios",
                "obtener_envio": "GET /api/envios/{id}",
                "tracking": "GET /api/envios/tracking/{tracking_number}",
                "listar": "GET /api/envios",
                "actualizar_estado": "PUT /api/envios/{id}/estado",
                "asignar_transportista": "PUT /api/envios/{id}/transportista"
            }
        }
    
    return app

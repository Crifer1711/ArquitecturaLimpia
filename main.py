"""Punto de entrada de la aplicación"""
from src.presentacion.api.app import crear_app
from src.infraestructura.config import get_config

if __name__ == '__main__':
    config = get_config()
    app = crear_app()
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║   Microservicio de Gestión de Envíos                         ║
    ║   Arquitectura Limpia + DDD                                   ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    🚀 Servidor iniciado en http://{config.HOST}:{config.PORT}
    📦 Modo: {config.MODO_COMUNICACION}
    🔧 Entorno: {'Desarrollo' if config.DEBUG else 'Producción'}
    
    Endpoints disponibles:
    - GET  /                              → Info del servicio
    - GET  /api/envios/health             → Health check
    - POST /api/envios                    → Crear envío
    - GET  /api/envios                    → Listar envíos
    - GET  /api/envios/{{id}}               → Obtener envío
    - GET  /api/envios/tracking/{{number}}  → Buscar por tracking
    - PUT  /api/envios/{{id}}/estado       → Actualizar estado
    - PUT  /api/envios/{{id}}/transportista → Asignar transportista
    """)
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )

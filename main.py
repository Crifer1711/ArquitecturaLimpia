from src.presentacion.api import crear_app
import os

# Crear app (para gunicorn)
app = crear_app()

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════╗
    ║  Microservicio de Gestión de Envíos          ║
    ║  Arquitectura Limpia + DDD                     ║
    ╚════════════════════════════════════════════════╝
    
    🚀 http://localhost:5000
    
    POST   /envios                      → Crear
    GET    /envios                      → Listar
    GET    /envios/{id}                 → Obtener
    PUT    /envios/{id}/transportista   → Asignar transportista
    PUT    /envios/{id}/estado          → Actualizar estado
    """)
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


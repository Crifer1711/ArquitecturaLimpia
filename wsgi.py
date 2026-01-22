"""
Módulo principal del microservicio de envíos.
Expone la aplicación Flask para ser importada por gunicorn.
"""
from src.presentacion.api.app import crear_app

# Crear la aplicación para ser usada por gunicorn
app = crear_app()

if __name__ == '__main__':
    from src.infraestructura.config import get_config
    config = get_config()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

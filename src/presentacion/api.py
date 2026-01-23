"""API REST con Flask - Controladores"""
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.infraestructura.repositorio_memoria import EnvioRepositoryMemoria
from src.aplicacion.casos_uso import (
    CrearEnvioUseCase,
    ObtenerEnvioUseCase,
    ListarEnviosUseCase,
    AsignarTransportistaUseCase,
    ActualizarEstadoUseCase
)

# Crear app
app = Flask(__name__)
CORS(app)

# Repositorio singleton
repositorio = EnvioRepositoryMemoria()


@app.route('/')
def home():
    """Información del servicio"""
    return jsonify({
        "servicio": "Gestión de Envíos",
        "version": "1.0",
        "arquitectura": "Clean Architecture + DDD",
        "endpoints": {
            "crear": "POST /envios",
            "listar": "GET /envios",
            "obtener": "GET /envios/{id}",
            "asignar_transportista": "PUT /envios/{id}/transportista",
            "actualizar_estado": "PUT /envios/{id}/estado"
        }
    })


@app.route('/envios', methods=['POST'])
def crear_envio():
    """Crear nuevo envío"""
    try:
        data = request.json
        caso_uso = CrearEnvioUseCase(repositorio)
        envio = caso_uso.ejecutar(
            data['pedido_id'],
            data['origen'],
            data['destino'],
            data['peso']
        )
        return jsonify(envio.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/envios', methods=['GET'])
def listar_envios():
    """Listar todos los envíos"""
    try:
        caso_uso = ListarEnviosUseCase(repositorio)
        envios = caso_uso.ejecutar()
        return jsonify([e.to_dict() for e in envios])
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/envios/<envio_id>', methods=['GET'])
def obtener_envio(envio_id):
    """Obtener un envío por ID"""
    try:
        caso_uso = ObtenerEnvioUseCase(repositorio)
        envio = caso_uso.ejecutar(envio_id)
        if not envio:
            return jsonify({"error": "Envío no encontrado"}), 404
        return jsonify(envio.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/envios/<envio_id>/transportista', methods=['PUT'])
def asignar_transportista(envio_id):
    """Asignar transportista a un envío"""
    try:
        data = request.json
        caso_uso = AsignarTransportistaUseCase(repositorio)
        envio = caso_uso.ejecutar(envio_id, data['transportista_id'])
        return jsonify(envio.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/envios/<envio_id>/estado', methods=['PUT'])
def actualizar_estado(envio_id):
    """Actualizar estado de un envío"""
    try:
        data = request.json
        caso_uso = ActualizarEstadoUseCase(repositorio)
        envio = caso_uso.ejecutar(envio_id, data['estado'])
        return jsonify(envio.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def crear_app():
    """Factory para crear la app"""
    return app

"""Controlador REST para gestión de envíos"""
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from ....aplicacion.casos_uso import (
    CrearEnvioUseCase,
    ActualizarEstadoEnvioUseCase,
    ObtenerEnvioUseCase,
    ListarEnviosUseCase,
    AsignarTransportistaUseCase
)
from ....aplicacion.dto import (
    CrearEnvioDTO,
    ActualizarEstadoEnvioDTO,
    AsignarTransportistaDTO
)
from ..schemas import (
    CrearEnvioRequestSchema,
    ActualizarEstadoRequestSchema,
    AsignarTransportistaRequestSchema,
    EnvioResponseSchema,
    ErrorResponseSchema
)


def crear_envios_blueprint(
    crear_envio_uc: CrearEnvioUseCase,
    actualizar_estado_uc: ActualizarEstadoEnvioUseCase,
    obtener_envio_uc: ObtenerEnvioUseCase,
    listar_envios_uc: ListarEnviosUseCase,
    asignar_transportista_uc: AsignarTransportistaUseCase
):
    """Factory para crear el blueprint de envíos con las dependencias inyectadas"""
    
    bp = Blueprint('envios', __name__, url_prefix='/api/envios')
    
    # Schemas
    crear_envio_schema = CrearEnvioRequestSchema()
    actualizar_estado_schema = ActualizarEstadoRequestSchema()
    asignar_transportista_schema = AsignarTransportistaRequestSchema()
    envio_response_schema = EnvioResponseSchema()
    error_schema = ErrorResponseSchema()
    
    @bp.route('/health', methods=['GET'])
    def health_check():
        """Endpoint de health check"""
        return jsonify({"status": "healthy", "service": "envios"}), 200
    
    @bp.route('', methods=['POST'])
    def crear_envio():
        """
        Crea un nuevo envío
        ---
        POST /api/envios
        """
        try:
            # Validar request
            data = crear_envio_schema.load(request.json)
            
            # Crear DTO
            dto = CrearEnvioDTO(
                pedido_id=data['pedido_id'],
                calle_origen=data['direccion_origen']['calle'],
                numero_origen=data['direccion_origen']['numero'],
                ciudad_origen=data['direccion_origen']['ciudad'],
                codigo_postal_origen=data['direccion_origen']['codigo_postal'],
                pais_origen=data['direccion_origen']['pais'],
                calle_destino=data['direccion_destino']['calle'],
                numero_destino=data['direccion_destino']['numero'],
                ciudad_destino=data['direccion_destino']['ciudad'],
                codigo_postal_destino=data['direccion_destino']['codigo_postal'],
                pais_destino=data['direccion_destino']['pais'],
                peso_kg=data['peso_kg'],
                dimensiones=data.get('dimensiones'),
                notas=data.get('notas')
            )
            
            # Ejecutar caso de uso
            resultado = crear_envio_uc.ejecutar(dto)
            
            # Serializar respuesta
            response_data = envio_response_schema.dump(resultado)
            
            return jsonify(response_data), 201
            
        except ValidationError as e:
            error_data = error_schema.dump({
                "error": "VALIDATION_ERROR",
                "mensaje": "Datos inválidos",
                "detalles": e.messages
            })
            return jsonify(error_data), 400
            
        except ValueError as e:
            error_data = error_schema.dump({
                "error": "BUSINESS_ERROR",
                "mensaje": str(e)
            })
            return jsonify(error_data), 400
            
        except Exception as e:
            error_data = error_schema.dump({
                "error": "INTERNAL_ERROR",
                "mensaje": "Error interno del servidor"
            })
            return jsonify(error_data), 500
    
    @bp.route('/<envio_id>', methods=['GET'])
    def obtener_envio(envio_id: str):
        """
        Obtiene un envío por ID
        ---
        GET /api/envios/{envio_id}
        """
        try:
            resultado = obtener_envio_uc.ejecutar_por_id(envio_id)
            response_data = envio_response_schema.dump(resultado)
            return jsonify(response_data), 200
            
        except ValueError as e:
            error_data = error_schema.dump({
                "error": "NOT_FOUND",
                "mensaje": str(e)
            })
            return jsonify(error_data), 404
            
        except Exception as e:
            error_data = error_schema.dump({
                "error": "INTERNAL_ERROR",
                "mensaje": "Error interno del servidor"
            })
            return jsonify(error_data), 500
    
    @bp.route('/tracking/<tracking_number>', methods=['GET'])
    def obtener_por_tracking(tracking_number: str):
        """
        Obtiene un envío por número de seguimiento
        ---
        GET /api/envios/tracking/{tracking_number}
        """
        try:
            resultado = obtener_envio_uc.ejecutar_por_tracking(tracking_number)
            response_data = envio_response_schema.dump(resultado)
            return jsonify(response_data), 200
            
        except ValueError as e:
            error_data = error_schema.dump({
                "error": "NOT_FOUND",
                "mensaje": str(e)
            })
            return jsonify(error_data), 404
            
        except Exception as e:
            error_data = error_schema.dump({
                "error": "INTERNAL_ERROR",
                "mensaje": "Error interno del servidor"
            })
            return jsonify(error_data), 500
    
    @bp.route('', methods=['GET'])
    def listar_envios():
        """
        Lista envíos con filtros opcionales
        ---
        GET /api/envios?estado=EN_TRANSITO&pedido_id=123
        """
        try:
            estado = request.args.get('estado')
            pedido_id = request.args.get('pedido_id')
            
            if estado:
                resultados = listar_envios_uc.ejecutar_por_estado(estado)
            elif pedido_id:
                resultados = listar_envios_uc.ejecutar_por_pedido(pedido_id)
            else:
                resultados = listar_envios_uc.ejecutar_todos()
            
            response_data = [envio_response_schema.dump(r) for r in resultados]
            return jsonify(response_data), 200
            
        except ValueError as e:
            error_data = error_schema.dump({
                "error": "VALIDATION_ERROR",
                "mensaje": str(e)
            })
            return jsonify(error_data), 400
            
        except Exception as e:
            error_data = error_schema.dump({
                "error": "INTERNAL_ERROR",
                "mensaje": "Error interno del servidor"
            })
            return jsonify(error_data), 500
    
    @bp.route('/<envio_id>/estado', methods=['PUT'])
    def actualizar_estado(envio_id: str):
        """
        Actualiza el estado de un envío
        ---
        PUT /api/envios/{envio_id}/estado
        """
        try:
            # Validar request
            data = actualizar_estado_schema.load(request.json)
            
            # Crear DTO
            dto = ActualizarEstadoEnvioDTO(
                envio_id=envio_id,
                nuevo_estado=data['nuevo_estado'],
                ubicacion=data['ubicacion'],
                descripcion=data['descripcion']
            )
            
            # Ejecutar caso de uso
            resultado = actualizar_estado_uc.ejecutar(dto)
            
            # Serializar respuesta
            response_data = envio_response_schema.dump(resultado)
            
            return jsonify(response_data), 200
            
        except ValidationError as e:
            error_data = error_schema.dump({
                "error": "VALIDATION_ERROR",
                "mensaje": "Datos inválidos",
                "detalles": e.messages
            })
            return jsonify(error_data), 400
            
        except ValueError as e:
            error_data = error_schema.dump({
                "error": "BUSINESS_ERROR",
                "mensaje": str(e)
            })
            return jsonify(error_data), 400
            
        except Exception as e:
            error_data = error_schema.dump({
                "error": "INTERNAL_ERROR",
                "mensaje": "Error interno del servidor"
            })
            return jsonify(error_data), 500
    
    @bp.route('/<envio_id>/transportista', methods=['PUT'])
    def asignar_transportista(envio_id: str):
        """
        Asigna un transportista a un envío
        ---
        PUT /api/envios/{envio_id}/transportista
        """
        try:
            # Validar request
            data = asignar_transportista_schema.load(request.json)
            
            # Crear DTO
            dto = AsignarTransportistaDTO(
                envio_id=envio_id,
                transportista_id=data['transportista_id']
            )
            
            # Ejecutar caso de uso
            resultado = asignar_transportista_uc.ejecutar(dto)
            
            # Serializar respuesta
            response_data = envio_response_schema.dump(resultado)
            
            return jsonify(response_data), 200
            
        except ValidationError as e:
            error_data = error_schema.dump({
                "error": "VALIDATION_ERROR",
                "mensaje": "Datos inválidos",
                "detalles": e.messages
            })
            return jsonify(error_data), 400
            
        except ValueError as e:
            error_data = error_schema.dump({
                "error": "BUSINESS_ERROR",
                "mensaje": str(e)
            })
            return jsonify(error_data), 400
            
        except Exception as e:
            error_data = error_schema.dump({
                "error": "INTERNAL_ERROR",
                "mensaje": "Error interno del servidor"
            })
            return jsonify(error_data), 500
    
    return bp

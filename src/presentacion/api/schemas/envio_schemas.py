"""Schemas de request/response para la API"""
from marshmallow import Schema, fields, validate, ValidationError


class DireccionSchema(Schema):
    """Schema para validar direcciones"""
    calle = fields.Str(required=True)
    numero = fields.Str(required=True)
    ciudad = fields.Str(required=True)
    codigo_postal = fields.Str(required=True)
    pais = fields.Str(required=True)


class CrearEnvioRequestSchema(Schema):
    """Schema para crear un nuevo envío"""
    pedido_id = fields.Str(required=True)
    direccion_origen = fields.Nested(DireccionSchema, required=True)
    direccion_destino = fields.Nested(DireccionSchema, required=True)
    peso_kg = fields.Float(required=True, validate=validate.Range(min=0.01))
    dimensiones = fields.Str(required=False, allow_none=True)
    notas = fields.Str(required=False, allow_none=True)


class ActualizarEstadoRequestSchema(Schema):
    """Schema para actualizar el estado de un envío"""
    nuevo_estado = fields.Str(
        required=True,
        validate=validate.OneOf([
            "PENDIENTE",
            "EN_PREPARACION",
            "EN_TRANSITO",
            "EN_DISTRIBUCION",
            "ENTREGADO",
            "CANCELADO",
            "DEVUELTO"
        ])
    )
    ubicacion = fields.Str(required=True)
    descripcion = fields.Str(required=True)


class AsignarTransportistaRequestSchema(Schema):
    """Schema para asignar un transportista"""
    transportista_id = fields.Str(required=True)


class EventoEnvioResponseSchema(Schema):
    """Schema de respuesta para eventos"""
    id = fields.Str()
    descripcion = fields.Str()
    ubicacion = fields.Str()
    fecha = fields.DateTime()
    detalles = fields.Str(allow_none=True)


class EnvioResponseSchema(Schema):
    """Schema de respuesta para envíos"""
    id = fields.Str()
    tracking_number = fields.Str()
    pedido_id = fields.Str()
    direccion_origen = fields.Str()
    direccion_destino = fields.Str()
    estado = fields.Str()
    transportista_id = fields.Str(allow_none=True)
    peso_kg = fields.Float()
    dimensiones = fields.Str(allow_none=True)
    fecha_creacion = fields.DateTime()
    fecha_estimada_entrega = fields.DateTime(allow_none=True)
    fecha_entrega_real = fields.DateTime(allow_none=True)
    eventos = fields.List(fields.Nested(EventoEnvioResponseSchema))
    notas = fields.Str(allow_none=True)


class ErrorResponseSchema(Schema):
    """Schema de respuesta para errores"""
    error = fields.Str()
    mensaje = fields.Str()
    detalles = fields.Dict(required=False)

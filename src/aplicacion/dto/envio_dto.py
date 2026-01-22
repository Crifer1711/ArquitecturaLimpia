"""DTOs para los casos de uso de la aplicación"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CrearEnvioDTO:
    """DTO para crear un nuevo envío"""
    pedido_id: str
    calle_origen: str
    numero_origen: str
    ciudad_origen: str
    codigo_postal_origen: str
    pais_origen: str
    calle_destino: str
    numero_destino: str
    ciudad_destino: str
    codigo_postal_destino: str
    pais_destino: str
    peso_kg: float
    dimensiones: Optional[str] = None
    notas: Optional[str] = None


@dataclass
class ActualizarEstadoEnvioDTO:
    """DTO para actualizar el estado de un envío"""
    envio_id: str
    nuevo_estado: str
    ubicacion: str
    descripcion: str


@dataclass
class AsignarTransportistaDTO:
    """DTO para asignar un transportista"""
    envio_id: str
    transportista_id: str


@dataclass
class EventoEnvioDTO:
    """DTO para eventos del envío"""
    id: str
    descripcion: str
    ubicacion: str
    fecha: datetime
    detalles: Optional[str] = None


@dataclass
class EnvioDTO:
    """DTO de respuesta con la información del envío"""
    id: str
    tracking_number: str
    pedido_id: str
    direccion_origen: str
    direccion_destino: str
    estado: str
    transportista_id: Optional[str]
    peso_kg: float
    dimensiones: Optional[str]
    fecha_creacion: datetime
    fecha_estimada_entrega: Optional[datetime]
    fecha_entrega_real: Optional[datetime]
    eventos: List[EventoEnvioDTO]
    notas: Optional[str]

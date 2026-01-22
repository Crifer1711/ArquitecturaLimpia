"""Entidad: Evento de seguimiento del envío"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EventoEnvio:
    """Representa un evento en el historial del envío"""
    
    id: str
    descripcion: str
    ubicacion: str
    fecha: datetime
    detalles: Optional[str] = None
    
    def __post_init__(self):
        if not self.id:
            raise ValueError("El ID del evento no puede estar vacío")
        if not self.descripcion:
            raise ValueError("La descripción del evento no puede estar vacía")
        if not self.ubicacion:
            raise ValueError("La ubicación del evento no puede estar vacía")

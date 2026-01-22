"""Agregado Raíz: Envío"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from ..value_objects import TrackingNumber, Direccion, EstadoEnvio
from ..entidades import EventoEnvio


@dataclass
class Envio:
    """
    Agregado raíz que representa un envío completo.
    Mantiene la consistencia de todos los datos relacionados con el envío.
    """
    
    id: str
    tracking_number: TrackingNumber
    pedido_id: str
    direccion_origen: Direccion
    direccion_destino: Direccion
    estado: EstadoEnvio
    transportista_id: Optional[str] = None
    peso_kg: float = 0.0
    dimensiones: Optional[str] = None
    fecha_creacion: datetime = field(default_factory=datetime.utcnow)
    fecha_estimada_entrega: Optional[datetime] = None
    fecha_entrega_real: Optional[datetime] = None
    eventos: List[EventoEnvio] = field(default_factory=list)
    notas: Optional[str] = None
    
    def __post_init__(self):
        self._validar()
    
    def _validar(self):
        """Valida las invariantes del agregado"""
        if not self.id:
            raise ValueError("El ID del envío no puede estar vacío")
        if not self.pedido_id:
            raise ValueError("El ID del pedido no puede estar vacío")
        if self.peso_kg <= 0:
            raise ValueError("El peso debe ser mayor a 0")
    
    def cambiar_estado(self, nuevo_estado: EstadoEnvio, ubicacion: str, descripcion: str) -> None:
        """
        Cambia el estado del envío validando las reglas de negocio.
        Registra un evento en el historial.
        """
        if not EstadoEnvio.puede_transicionar(self.estado, nuevo_estado):
            raise ValueError(
                f"No se puede cambiar de {self.estado.value} a {nuevo_estado.value}"
            )
        
        self.estado = nuevo_estado
        self._agregar_evento(descripcion, ubicacion)
        
        # Si se entrega, registrar la fecha
        if nuevo_estado == EstadoEnvio.ENTREGADO:
            self.fecha_entrega_real = datetime.utcnow()
    
    def asignar_transportista(self, transportista_id: str) -> None:
        """Asigna un transportista al envío"""
        if self.estado not in [EstadoEnvio.PENDIENTE, EstadoEnvio.EN_PREPARACION]:
            raise ValueError("Solo se puede asignar transportista en estados iniciales")
        
        self.transportista_id = transportista_id
        self._agregar_evento(
            f"Transportista asignado: {transportista_id}",
            "Centro de distribución"
        )
    
    def _agregar_evento(self, descripcion: str, ubicacion: str, detalles: Optional[str] = None) -> None:
        """Agrega un evento al historial del envío"""
        evento = EventoEnvio(
            id=str(uuid4()),
            descripcion=descripcion,
            ubicacion=ubicacion,
            fecha=datetime.utcnow(),
            detalles=detalles
        )
        self.eventos.append(evento)
    
    def esta_en_transito(self) -> bool:
        """Verifica si el envío está en tránsito"""
        return self.estado in [EstadoEnvio.EN_TRANSITO, EstadoEnvio.EN_DISTRIBUCION]
    
    def esta_finalizado(self) -> bool:
        """Verifica si el envío está finalizado"""
        return self.estado in [EstadoEnvio.ENTREGADO, EstadoEnvio.CANCELADO, EstadoEnvio.DEVUELTO]
    
    @staticmethod
    def crear_nuevo(
        pedido_id: str,
        direccion_origen: Direccion,
        direccion_destino: Direccion,
        peso_kg: float,
        dimensiones: Optional[str] = None,
        notas: Optional[str] = None
    ) -> 'Envio':
        """Factory method para crear un nuevo envío"""
        envio_id = str(uuid4())
        tracking = TrackingNumber(f"ENV-{datetime.utcnow().strftime('%Y%m%d%H')}{envio_id[:2]}")
        
        envio = Envio(
            id=envio_id,
            tracking_number=tracking,
            pedido_id=pedido_id,
            direccion_origen=direccion_origen,
            direccion_destino=direccion_destino,
            estado=EstadoEnvio.PENDIENTE,
            peso_kg=peso_kg,
            dimensiones=dimensiones,
            notas=notas
        )
        
        envio._agregar_evento("Envío creado", "Sistema")
        return envio

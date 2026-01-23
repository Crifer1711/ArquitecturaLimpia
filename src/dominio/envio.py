"""AGREGADO: Envio - Núcleo del dominio"""
from datetime import datetime
from enum import Enum


class EstadoEnvio(Enum):
    """Estados válidos de un envío"""
    PENDIENTE = "PENDIENTE"
    EN_PREPARACION = "EN_PREPARACION"
    EN_TRANSITO = "EN_TRANSITO"
    ENTREGADO = "ENTREGADO"


class Envio:
    """AGREGADO RAÍZ - Representa un envío completo"""
    
    def __init__(self, pedido_id: str, origen: str, destino: str, peso: float, transportista_id: str = None):
        # Validaciones de negocio
        if peso <= 0:
            raise ValueError("El peso debe ser mayor a 0")
        if not pedido_id or not origen or not destino:
            raise ValueError("Datos obligatorios faltantes")
        
        self.id = None  # Se asigna al guardar
        self.pedido_id = pedido_id
        self.tracking = f"ENV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.transportista_id = transportista_id
        
        # Si ya tiene transportista, inicia EN_PREPARACION
        if transportista_id:
            self.estado = EstadoEnvio.EN_PREPARACION
            self.historial = [{"estado": "EN_PREPARACION", "fecha": datetime.now().isoformat()}]
        else:
            self.estado = EstadoEnvio.PENDIENTE
            self.historial = [{"estado": "PENDIENTE", "fecha": datetime.now().isoformat()}]
        
        self.fecha_creacion = datetime.now()
    
    def asignar_transportista(self, transportista_id: str):
        """Asigna transportista y cambia a EN_PREPARACION"""
        if self.estado != EstadoEnvio.PENDIENTE:
            raise ValueError("Solo se puede asignar transportista en estado PENDIENTE")
        self.transportista_id = transportista_id
        self._cambiar_estado(EstadoEnvio.EN_PREPARACION)
    
    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado del envío"""
        estado_enum = EstadoEnvio[nuevo_estado]
        self._cambiar_estado(estado_enum)
    
    def _cambiar_estado(self, estado: EstadoEnvio):
        """Método privado para cambiar estado"""
        self.estado = estado
        self.historial.append({
            "estado": estado.value,
            "fecha": datetime.now().isoformat()
        })
    
    def to_dict(self):
        """Convierte a diccionario"""
        return {
            "id": self.id,
            "pedido_id": self.pedido_id,
            "tracking": self.tracking,
            "origen": self.origen,
            "destino": self.destino,
            "peso": self.peso,
            "estado": self.estado.value,
            "transportista_id": self.transportista_id,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "historial": self.historial
        }

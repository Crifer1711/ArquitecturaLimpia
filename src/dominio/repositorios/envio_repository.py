"""Interfaz del repositorio de envíos"""
from abc import ABC, abstractmethod
from typing import List, Optional

from ..agregados import Envio
from ..value_objects import TrackingNumber, EstadoEnvio


class EnvioRepository(ABC):
    """Interfaz para el repositorio de envíos (patrón Repository de DDD)"""
    
    @abstractmethod
    def guardar(self, envio: Envio) -> Envio:
        """Guarda o actualiza un envío"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, envio_id: str) -> Optional[Envio]:
        """Obtiene un envío por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_tracking(self, tracking_number: TrackingNumber) -> Optional[Envio]:
        """Obtiene un envío por su número de seguimiento"""
        pass
    
    @abstractmethod
    def obtener_por_pedido(self, pedido_id: str) -> List[Envio]:
        """Obtiene todos los envíos asociados a un pedido"""
        pass
    
    @abstractmethod
    def listar_todos(self) -> List[Envio]:
        """Lista todos los envíos"""
        pass
    
    @abstractmethod
    def listar_por_estado(self, estado: EstadoEnvio) -> List[Envio]:
        """Lista envíos por estado"""
        pass
    
    @abstractmethod
    def eliminar(self, envio_id: str) -> bool:
        """Elimina un envío (soft delete recomendado)"""
        pass

"""Implementación en memoria del repositorio de envíos"""
from typing import Dict, List, Optional

from ...dominio.repositorios import EnvioRepository
from ...dominio.agregados import Envio
from ...dominio.value_objects import TrackingNumber, EstadoEnvio


class EnvioRepositoryMemoria(EnvioRepository):
    """
    Implementación en memoria del repositorio de envíos.
    Útil para desarrollo y pruebas.
    """
    
    def __init__(self):
        self._envios: Dict[str, Envio] = {}
    
    def guardar(self, envio: Envio) -> Envio:
        """Guarda o actualiza un envío en memoria"""
        self._envios[envio.id] = envio
        return envio
    
    def obtener_por_id(self, envio_id: str) -> Optional[Envio]:
        """Obtiene un envío por su ID"""
        return self._envios.get(envio_id)
    
    def obtener_por_tracking(self, tracking_number: TrackingNumber) -> Optional[Envio]:
        """Obtiene un envío por su número de seguimiento"""
        for envio in self._envios.values():
            if envio.tracking_number == tracking_number:
                return envio
        return None
    
    def obtener_por_pedido(self, pedido_id: str) -> List[Envio]:
        """Obtiene todos los envíos asociados a un pedido"""
        return [
            envio for envio in self._envios.values()
            if envio.pedido_id == pedido_id
        ]
    
    def listar_todos(self) -> List[Envio]:
        """Lista todos los envíos"""
        return list(self._envios.values())
    
    def listar_por_estado(self, estado: EstadoEnvio) -> List[Envio]:
        """Lista envíos por estado"""
        return [
            envio for envio in self._envios.values()
            if envio.estado == estado
        ]
    
    def eliminar(self, envio_id: str) -> bool:
        """Elimina un envío de memoria"""
        if envio_id in self._envios:
            del self._envios[envio_id]
            return True
        return False
    
    def limpiar(self):
        """Limpia todos los envíos (útil para testing)"""
        self._envios.clear()

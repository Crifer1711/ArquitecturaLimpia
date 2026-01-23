"""INTERFAZ del Repositorio - Puerto del dominio"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .envio import Envio


class IEnvioRepository(ABC):
    """Interfaz que define cómo se debe persistir un Envío"""
    
    @abstractmethod
    def guardar(self, envio: Envio) -> Envio:
        pass
    
    @abstractmethod
    def obtener(self, envio_id: str) -> Optional[Envio]:
        pass
    
    @abstractmethod
    def listar(self) -> List[Envio]:
        pass

"""IMPLEMENTACIÓN del Repositorio en Memoria"""
from typing import List, Optional
from src.dominio.envio import Envio
from src.dominio.repositorio import IEnvioRepository


class EnvioRepositoryMemoria(IEnvioRepository):
    """Implementación concreta del repositorio usando memoria"""
    
    def __init__(self):
        self._envios = {}
    
    def guardar(self, envio: Envio) -> Envio:
        self._envios[envio.id] = envio
        return envio
    
    def obtener(self, envio_id: str) -> Optional[Envio]:
        return self._envios.get(envio_id)
    
    def listar(self) -> List[Envio]:
        return list(self._envios.values())

"""Caso de uso: Listar envíos"""
from typing import List

from ...dominio.repositorios import EnvioRepository
from ...dominio.value_objects import EstadoEnvio
from ..dto import EnvioDTO
from ..mappers import EnvioMapper


class ListarEnviosUseCase:
    """Caso de uso para listar envíos"""
    
    def __init__(self, envio_repository: EnvioRepository):
        self.envio_repository = envio_repository
    
    def ejecutar_todos(self) -> List[EnvioDTO]:
        """
        Lista todos los envíos.
        
        Returns:
            Lista de EnvioDTO
        """
        envios = self.envio_repository.listar_todos()
        return [EnvioMapper.a_dto(envio) for envio in envios]
    
    def ejecutar_por_estado(self, estado: str) -> List[EnvioDTO]:
        """
        Lista envíos filtrados por estado.
        
        Args:
            estado: Estado a filtrar
            
        Returns:
            Lista de EnvioDTO
            
        Raises:
            ValueError: Si el estado es inválido
        """
        try:
            estado_enum = EstadoEnvio[estado]
        except KeyError:
            raise ValueError(f"Estado inválido: {estado}")
        
        envios = self.envio_repository.listar_por_estado(estado_enum)
        return [EnvioMapper.a_dto(envio) for envio in envios]
    
    def ejecutar_por_pedido(self, pedido_id: str) -> List[EnvioDTO]:
        """
        Lista envíos asociados a un pedido.
        
        Args:
            pedido_id: ID del pedido
            
        Returns:
            Lista de EnvioDTO
        """
        envios = self.envio_repository.obtener_por_pedido(pedido_id)
        return [EnvioMapper.a_dto(envio) for envio in envios]

"""Caso de uso: Obtener información de un envío"""
from ...dominio.repositorios import EnvioRepository
from ..dto import EnvioDTO
from ..mappers import EnvioMapper


class ObtenerEnvioUseCase:
    """Caso de uso para obtener la información de un envío"""
    
    def __init__(self, envio_repository: EnvioRepository):
        self.envio_repository = envio_repository
    
    def ejecutar_por_id(self, envio_id: str) -> EnvioDTO:
        """
        Obtiene un envío por su ID.
        
        Args:
            envio_id: ID del envío
            
        Returns:
            EnvioDTO con la información del envío
            
        Raises:
            ValueError: Si el envío no existe
        """
        envio = self.envio_repository.obtener_por_id(envio_id)
        
        if not envio:
            raise ValueError(f"Envío con ID {envio_id} no encontrado")
        
        return EnvioMapper.a_dto(envio)
    
    def ejecutar_por_tracking(self, tracking_number: str) -> EnvioDTO:
        """
        Obtiene un envío por su número de seguimiento.
        
        Args:
            tracking_number: Número de seguimiento
            
        Returns:
            EnvioDTO con la información del envío
            
        Raises:
            ValueError: Si el envío no existe
        """
        from ...dominio.value_objects import TrackingNumber
        
        tracking = TrackingNumber(tracking_number)
        envio = self.envio_repository.obtener_por_tracking(tracking)
        
        if not envio:
            raise ValueError(f"Envío con tracking {tracking_number} no encontrado")
        
        return EnvioMapper.a_dto(envio)

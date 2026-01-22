"""Caso de uso: Actualizar el estado de un envío"""
from typing import Optional

from ...dominio.repositorios import EnvioRepository
from ...dominio.value_objects import EstadoEnvio
from ..dto import ActualizarEstadoEnvioDTO, EnvioDTO
from ..mappers import EnvioMapper


class ActualizarEstadoEnvioUseCase:
    """Caso de uso para actualizar el estado de un envío"""
    
    def __init__(
        self,
        envio_repository: EnvioRepository,
        notificador_pedidos: Optional[object] = None
    ):
        self.envio_repository = envio_repository
        self.notificador_pedidos = notificador_pedidos
    
    def ejecutar(self, dto: ActualizarEstadoEnvioDTO) -> EnvioDTO:
        """
        Ejecuta el caso de uso de actualizar estado.
        
        Args:
            dto: Datos para actualizar el estado
            
        Returns:
            EnvioDTO con la información actualizada
            
        Raises:
            ValueError: Si el envío no existe o la transición no es válida
        """
        # Obtener el envío
        envio = self.envio_repository.obtener_por_id(dto.envio_id)
        
        if not envio:
            raise ValueError(f"Envío con ID {dto.envio_id} no encontrado")
        
        # Convertir string a enum
        try:
            nuevo_estado = EstadoEnvio[dto.nuevo_estado]
        except KeyError:
            raise ValueError(f"Estado inválido: {dto.nuevo_estado}")
        
        # Cambiar estado (esto valida las reglas de negocio)
        envio.cambiar_estado(nuevo_estado, dto.ubicacion, dto.descripcion)
        
        # Guardar cambios
        envio_actualizado = self.envio_repository.guardar(envio)
        
        # Notificar a otros contextos
        if self.notificador_pedidos and nuevo_estado == EstadoEnvio.ENTREGADO:
            try:
                self.notificador_pedidos.notificar_envio_entregado(
                    pedido_id=envio_actualizado.pedido_id,
                    envio_id=envio_actualizado.id
                )
            except Exception as e:
                print(f"Error al notificar: {e}")
        
        return EnvioMapper.a_dto(envio_actualizado)

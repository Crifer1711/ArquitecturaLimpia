"""Caso de uso: Crear un nuevo envío"""
from typing import Optional

from ...dominio.repositorios import EnvioRepository
from ...dominio.agregados import Envio
from ...dominio.value_objects import Direccion
from ..dto import CrearEnvioDTO, EnvioDTO
from ..mappers import EnvioMapper


class CrearEnvioUseCase:
    """Caso de uso para crear un nuevo envío"""
    
    def __init__(
        self,
        envio_repository: EnvioRepository,
        notificador_pedidos: Optional[object] = None
    ):
        self.envio_repository = envio_repository
        self.notificador_pedidos = notificador_pedidos
    
    def ejecutar(self, dto: CrearEnvioDTO) -> EnvioDTO:
        """
        Ejecuta el caso de uso de crear un envío.
        
        Args:
            dto: Datos para crear el envío
            
        Returns:
            EnvioDTO con la información del envío creado
            
        Raises:
            ValueError: Si los datos son inválidos
        """
        # Crear value objects
        direccion_origen = Direccion(
            calle=dto.calle_origen,
            numero=dto.numero_origen,
            ciudad=dto.ciudad_origen,
            codigo_postal=dto.codigo_postal_origen,
            pais=dto.pais_origen
        )
        
        direccion_destino = Direccion(
            calle=dto.calle_destino,
            numero=dto.numero_destino,
            ciudad=dto.ciudad_destino,
            codigo_postal=dto.codigo_postal_destino,
            pais=dto.pais_destino
        )
        
        # Crear el agregado Envio
        envio = Envio.crear_nuevo(
            pedido_id=dto.pedido_id,
            direccion_origen=direccion_origen,
            direccion_destino=direccion_destino,
            peso_kg=dto.peso_kg,
            dimensiones=dto.dimensiones,
            notas=dto.notas
        )
        
        # Guardar en el repositorio
        envio_guardado = self.envio_repository.guardar(envio)
        
        # Notificar a otros contextos si es necesario
        if self.notificador_pedidos:
            try:
                self.notificador_pedidos.notificar_envio_creado(
                    pedido_id=envio_guardado.pedido_id,
                    envio_id=envio_guardado.id,
                    tracking_number=str(envio_guardado.tracking_number)
                )
            except Exception as e:
                # Log error but don't fail the use case
                print(f"Error al notificar: {e}")
        
        # Retornar DTO
        return EnvioMapper.a_dto(envio_guardado)

"""Caso de uso: Asignar transportista a un envío"""
from typing import Optional

from ...dominio.repositorios import EnvioRepository
from ..dto import AsignarTransportistaDTO, EnvioDTO
from ..mappers import EnvioMapper


class AsignarTransportistaUseCase:
    """Caso de uso para asignar un transportista a un envío"""
    
    def __init__(
        self,
        envio_repository: EnvioRepository,
        cliente_transportistas: Optional[object] = None
    ):
        self.envio_repository = envio_repository
        self.cliente_transportistas = cliente_transportistas
    
    def ejecutar(self, dto: AsignarTransportistaDTO) -> EnvioDTO:
        """
        Ejecuta el caso de uso de asignar transportista.
        
        Args:
            dto: Datos para asignar el transportista
            
        Returns:
            EnvioDTO con la información actualizada
            
        Raises:
            ValueError: Si el envío no existe o no se puede asignar transportista
        """
        # Obtener el envío
        envio = self.envio_repository.obtener_por_id(dto.envio_id)
        
        if not envio:
            raise ValueError(f"Envío con ID {dto.envio_id} no encontrado")
        
        # Validar transportista (comunicación con contexto de Transportistas)
        if self.cliente_transportistas:
            try:
                transportista_valido = self.cliente_transportistas.validar_transportista(
                    dto.transportista_id
                )
                if not transportista_valido:
                    raise ValueError(f"Transportista {dto.transportista_id} no válido")
            except Exception as e:
                print(f"Error al validar transportista: {e}")
                # Continuar con la asignación incluso si falla la validación externa
        
        # Asignar transportista (esto valida las reglas de negocio)
        envio.asignar_transportista(dto.transportista_id)
        
        # Guardar cambios
        envio_actualizado = self.envio_repository.guardar(envio)
        
        # Notificar al transportista
        if self.cliente_transportistas:
            try:
                self.cliente_transportistas.notificar_nuevo_envio(
                    transportista_id=dto.transportista_id,
                    envio_id=envio_actualizado.id,
                    direccion_origen=str(envio_actualizado.direccion_origen),
                    direccion_destino=str(envio_actualizado.direccion_destino),
                    peso_kg=envio_actualizado.peso_kg
                )
            except Exception as e:
                print(f"Error al notificar transportista: {e}")
        
        return EnvioMapper.a_dto(envio_actualizado)

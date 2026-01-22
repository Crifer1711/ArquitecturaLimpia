"""Mapper para convertir entre entidades de dominio y DTOs"""
from typing import List

from ...dominio.agregados import Envio
from ...dominio.entidades import EventoEnvio
from ..dto import EnvioDTO, EventoEnvioDTO


class EnvioMapper:
    """Mapea entre el agregado Envio y EnvioDTO"""
    
    @staticmethod
    def a_dto(envio: Envio) -> EnvioDTO:
        """Convierte un agregado Envio a EnvioDTO"""
        eventos_dto = [
            EventoEnvioDTO(
                id=evento.id,
                descripcion=evento.descripcion,
                ubicacion=evento.ubicacion,
                fecha=evento.fecha,
                detalles=evento.detalles
            )
            for evento in envio.eventos
        ]
        
        return EnvioDTO(
            id=envio.id,
            tracking_number=str(envio.tracking_number),
            pedido_id=envio.pedido_id,
            direccion_origen=str(envio.direccion_origen),
            direccion_destino=str(envio.direccion_destino),
            estado=envio.estado.value,
            transportista_id=envio.transportista_id,
            peso_kg=envio.peso_kg,
            dimensiones=envio.dimensiones,
            fecha_creacion=envio.fecha_creacion,
            fecha_estimada_entrega=envio.fecha_estimada_entrega,
            fecha_entrega_real=envio.fecha_entrega_real,
            eventos=eventos_dto,
            notas=envio.notas
        )

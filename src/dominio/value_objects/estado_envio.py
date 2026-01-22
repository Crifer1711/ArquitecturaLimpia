"""Value Object: Estado del envío"""
from enum import Enum


class EstadoEnvio(str, Enum):
    """Estados posibles de un envío"""
    
    PENDIENTE = "PENDIENTE"
    EN_PREPARACION = "EN_PREPARACION"
    EN_TRANSITO = "EN_TRANSITO"
    EN_DISTRIBUCION = "EN_DISTRIBUCION"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"
    DEVUELTO = "DEVUELTO"
    
    @classmethod
    def puede_transicionar(cls, estado_actual: 'EstadoEnvio', nuevo_estado: 'EstadoEnvio') -> bool:
        """Valida si una transición de estado es válida"""
        transiciones_validas = {
            cls.PENDIENTE: [cls.EN_PREPARACION, cls.CANCELADO],
            cls.EN_PREPARACION: [cls.EN_TRANSITO, cls.CANCELADO],
            cls.EN_TRANSITO: [cls.EN_DISTRIBUCION, cls.DEVUELTO],
            cls.EN_DISTRIBUCION: [cls.ENTREGADO, cls.DEVUELTO],
            cls.ENTREGADO: [],
            cls.CANCELADO: [],
            cls.DEVUELTO: []
        }
        
        return nuevo_estado in transiciones_validas.get(estado_actual, [])

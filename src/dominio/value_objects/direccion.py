"""Value Object: Dirección de envío"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Direccion:
    """Dirección completa para envío"""
    
    calle: str
    numero: str
    ciudad: str
    codigo_postal: str
    pais: str
    
    def __post_init__(self):
        if not all([self.calle, self.numero, self.ciudad, self.codigo_postal, self.pais]):
            raise ValueError("Todos los campos de la dirección son obligatorios")
        
        if len(self.codigo_postal) < 4:
            raise ValueError("Código postal inválido")
    
    def direccion_completa(self) -> str:
        """Retorna la dirección formateada"""
        return f"{self.calle} {self.numero}, {self.ciudad}, {self.codigo_postal}, {self.pais}"
    
    def __str__(self) -> str:
        return self.direccion_completa()

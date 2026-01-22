"""Value Object: Número de seguimiento"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class TrackingNumber:
    """Número de seguimiento único para cada envío"""
    
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("El número de seguimiento no puede estar vacío")
        
        if not re.match(r'^ENV-\d{10}$', self.value):
            raise ValueError("Formato de número de seguimiento inválido. Debe ser ENV-XXXXXXXXXX")
    
    def __str__(self) -> str:
        return self.value

"""Cliente HTTP para comunicación con el servicio de Transportistas"""
import requests
from typing import Optional, Dict, Any


class TransportistasHttpClient:
    """
    Cliente HTTP para comunicarse con el contexto de Transportistas.
    Permite validar transportistas y notificar nuevos envíos.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or "http://localhost:5002"
    
    def validar_transportista(self, transportista_id: str) -> bool:
        """
        Valida si un transportista existe y está disponible.
        
        Args:
            transportista_id: ID del transportista a validar
            
        Returns:
            True si el transportista es válido
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/transportistas/{transportista_id}",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error al validar transportista: {e}")
            return True
    
    def obtener_disponibilidad(self, transportista_id: str) -> Dict[str, Any]:
        """
        Obtiene la disponibilidad de un transportista.
        
        Args:
            transportista_id: ID del transportista
            
        Returns:
            Diccionario con información de disponibilidad
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/transportistas/{transportista_id}/disponibilidad",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error al obtener disponibilidad: {e}")
        
        return {"disponible": True, "capacidad_restante": 100}
    
    def notificar_nuevo_envio(
        self,
        transportista_id: str,
        envio_id: str,
        direccion_origen: str,
        direccion_destino: str,
        peso_kg: float
    ) -> bool:
        """
        Notifica al transportista sobre un nuevo envío asignado.
        
        Args:
            transportista_id: ID del transportista
            envio_id: ID del envío
            direccion_origen: Dirección de origen
            direccion_destino: Dirección de destino
            peso_kg: Peso del envío
            
        Returns:
            True si la notificación fue exitosa
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/transportistas/{transportista_id}/envios",
                json={
                    "envio_id": envio_id,
                    "direccion_origen": direccion_origen,
                    "direccion_destino": direccion_destino,
                    "peso_kg": peso_kg
                },
                timeout=5
            )
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error al notificar nuevo envío: {e}")
            return False

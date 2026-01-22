"""Cliente HTTP para comunicación con el servicio de Pedidos"""
import requests
from typing import Optional, Dict, Any


class PedidosHttpClient:
    """
    Cliente HTTP para comunicarse con el contexto de Pedidos.
    Permite validar y notificar eventos relacionados con pedidos.
    """
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or "http://localhost:5001"
    
    def validar_pedido(self, pedido_id: str) -> bool:
        """
        Valida si un pedido existe y está listo para envío.
        
        Args:
            pedido_id: ID del pedido a validar
            
        Returns:
            True si el pedido es válido, False en caso contrario
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/pedidos/{pedido_id}",
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error al validar pedido: {e}")
            # En caso de error, asumimos que el pedido es válido
            # para no bloquear el flujo
            return True
    
    def notificar_envio_creado(
        self,
        pedido_id: str,
        envio_id: str,
        tracking_number: str
    ) -> bool:
        """
        Notifica al servicio de Pedidos que se ha creado un envío.
        
        Args:
            pedido_id: ID del pedido
            envio_id: ID del envío creado
            tracking_number: Número de seguimiento
            
        Returns:
            True si la notificación fue exitosa
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/pedidos/{pedido_id}/envio-creado",
                json={
                    "envio_id": envio_id,
                    "tracking_number": tracking_number
                },
                timeout=5
            )
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error al notificar envío creado: {e}")
            return False
    
    def notificar_envio_entregado(self, pedido_id: str, envio_id: str) -> bool:
        """
        Notifica al servicio de Pedidos que un envío ha sido entregado.
        
        Args:
            pedido_id: ID del pedido
            envio_id: ID del envío
            
        Returns:
            True si la notificación fue exitosa
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/pedidos/{pedido_id}/envio-entregado",
                json={"envio_id": envio_id},
                timeout=5
            )
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"Error al notificar envío entregado: {e}")
            return False

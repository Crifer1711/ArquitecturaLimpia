"""Cliente de mensajería para comunicación asíncrona con RabbitMQ"""
import json
from typing import Optional, Dict, Any
import os


class MensajeriaClient:
    """
    Cliente para publicar y consumir mensajes usando colas de mensajería.
    Implementación flexible que puede usar RabbitMQ, Redis, o modo simulado.
    """
    
    def __init__(self, connection_url: Optional[str] = None, modo_simulado: bool = True):
        self.connection_url = connection_url or os.getenv(
            "RABBITMQ_URL",
            "amqp://guest:guest@localhost:5672/"
        )
        self.modo_simulado = modo_simulado
        self.connection = None
        self.channel = None
        
        if not modo_simulado:
            self._conectar()
    
    def _conectar(self):
        """Establece conexión con RabbitMQ"""
        try:
            import pika
            
            parameters = pika.URLParameters(self.connection_url)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declarar exchanges y colas
            self.channel.exchange_declare(
                exchange='envios',
                exchange_type='topic',
                durable=True
            )
            
            print("Conectado a RabbitMQ")
        except Exception as e:
            print(f"Error al conectar con RabbitMQ: {e}")
            print("Usando modo simulado")
            self.modo_simulado = True
    
    def publicar_evento(
        self,
        evento: str,
        datos: Dict[str, Any],
        routing_key: Optional[str] = None
    ) -> bool:
        """
        Publica un evento en la cola de mensajería.
        
        Args:
            evento: Nombre del evento
            datos: Datos del evento
            routing_key: Clave de enrutamiento (opcional)
            
        Returns:
            True si el mensaje fue publicado exitosamente
        """
        if self.modo_simulado:
            print(f"[SIMULADO] Publicando evento: {evento}")
            print(f"[SIMULADO] Datos: {json.dumps(datos, indent=2, default=str)}")
            return True
        
        try:
            import pika
            
            routing_key = routing_key or f"envios.{evento}"
            mensaje = {
                "evento": evento,
                "datos": datos
            }
            
            self.channel.basic_publish(
                exchange='envios',
                routing_key=routing_key,
                body=json.dumps(mensaje, default=str),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Hacer el mensaje persistente
                    content_type='application/json'
                )
            )
            
            print(f"Evento publicado: {evento} - {routing_key}")
            return True
        except Exception as e:
            print(f"Error al publicar evento: {e}")
            return False
    
    def notificar_envio_creado(
        self,
        pedido_id: str,
        envio_id: str,
        tracking_number: str
    ) -> bool:
        """Notifica que se ha creado un envío"""
        return self.publicar_evento(
            evento="envio.creado",
            datos={
                "pedido_id": pedido_id,
                "envio_id": envio_id,
                "tracking_number": tracking_number
            },
            routing_key="envios.creado"
        )
    
    def notificar_envio_entregado(self, pedido_id: str, envio_id: str) -> bool:
        """Notifica que un envío ha sido entregado"""
        return self.publicar_evento(
            evento="envio.entregado",
            datos={
                "pedido_id": pedido_id,
                "envio_id": envio_id
            },
            routing_key="envios.entregado"
        )
    
    def notificar_estado_actualizado(
        self,
        envio_id: str,
        estado_anterior: str,
        estado_nuevo: str,
        ubicacion: str
    ) -> bool:
        """Notifica que el estado de un envío ha cambiado"""
        return self.publicar_evento(
            evento="envio.estado_actualizado",
            datos={
                "envio_id": envio_id,
                "estado_anterior": estado_anterior,
                "estado_nuevo": estado_nuevo,
                "ubicacion": ubicacion
            },
            routing_key="envios.estado_actualizado"
        )
    
    def cerrar(self):
        """Cierra la conexión con RabbitMQ"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            print("Conexión con RabbitMQ cerrada")

"""Clientes HTTP para comunicación con otros contextos"""
from .pedidos_http_client import PedidosHttpClient
from .transportistas_http_client import TransportistasHttpClient

__all__ = ['PedidosHttpClient', 'TransportistasHttpClient']

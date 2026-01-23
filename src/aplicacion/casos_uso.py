"""CASOS DE USO - Orquestan la lógica de aplicación"""
import uuid
from src.dominio.envio import Envio
from src.dominio.repositorio import IEnvioRepository


class CrearEnvioUseCase:
    """Caso de uso: Crear un nuevo envío"""
    
    def __init__(self, repositorio: IEnvioRepository):
        self.repo = repositorio
    
    def ejecutar(self, pedido_id: str, origen: str, destino: str, peso: float, transportista_id: str = None):
        # Crear entidad de dominio
        envio = Envio(pedido_id, origen, destino, peso, transportista_id)
        envio.id = str(uuid.uuid4())
        
        # Guardar
        return self.repo.guardar(envio)


class ObtenerEnvioUseCase:
    """Caso de uso: Obtener un envío"""
    
    def __init__(self, repositorio: IEnvioRepository):
        self.repo = repositorio
    
    def ejecutar(self, envio_id: str):
        return self.repo.obtener(envio_id)


class ListarEnviosUseCase:
    """Caso de uso: Listar todos los envíos"""
    
    def __init__(self, repositorio: IEnvioRepository):
        self.repo = repositorio
    
    def ejecutar(self):
        return self.repo.listar()


class AsignarTransportistaUseCase:
    """Caso de uso: Asignar transportista"""
    
    def __init__(self, repositorio: IEnvioRepository):
        self.repo = repositorio
    
    def ejecutar(self, envio_id: str, transportista_id: str):
        envio = self.repo.obtener(envio_id)
        if not envio:
            raise ValueError("Envío no encontrado")
        
        envio.asignar_transportista(transportista_id)
        return self.repo.guardar(envio)


class ActualizarEstadoUseCase:
    """Caso de uso: Actualizar estado del envío"""
    
    def __init__(self, repositorio: IEnvioRepository):
        self.repo = repositorio
    
    def ejecutar(self, envio_id: str, nuevo_estado: str):
        envio = self.repo.obtener(envio_id)
        if not envio:
            raise ValueError("Envío no encontrado")
        
        envio.cambiar_estado(nuevo_estado)
        return self.repo.guardar(envio)

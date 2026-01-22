# 🚚 Microservicio de Gestión de Envíos

API REST para gestionar envíos de e-commerce con **Arquitectura Limpia** y **DDD**.

## 🚀 Despliegue en Render

### 1. Subir a GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/Crifer1711/ArquitecturaLimpia.git
git push -u origin main
```

### 2. Configurar en Render
1. Ve a [Render.com](https://render.com)
2. Crea un **Web Service**
3. Conecta: `https://github.com/Crifer1711/ArquitecturaLimpia.git`
4. Configura:
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn --bind 0.0.0.0:$PORT wsgi:app --workers 2`
5. Variables:
   ```
   ENVIRONMENT=production
   DEBUG=False
   SECRET_KEY=<genera>
   ```
6. Deploy!

URL: `https://tu-servicio.onrender.com`

## 📡 API - Uso en Postman

### Crear Envío
```http
POST https://tu-servicio.onrender.com/api/envios
Content-Type: application/json

{
  "pedido_id": "PED-001",
  "direccion_origen": {
    "calle": "Av. Principal",
    "numero": "100",
    "ciudad": "Madrid",
    "codigo_postal": "28001",
    "pais": "España"
  },
  "direccion_destino": {
    "calle": "Calle Secundaria",
    "numero": "200",
    "ciudad": "Barcelona",
    "codigo_postal": "08001",
    "pais": "España"
  },
  "peso_kg": 2.5
}
```

### Obtener por ID
```http
GET https://tu-servicio.onrender.com/api/envios/{id}
```

**Respuesta JSON**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "tracking_number": "ENV-2026012215ab",
  "pedido_id": "PED-001",
  "estado": "PENDIENTE",
  "direccion_origen": "Av. Principal 100, Madrid, 28001, España",
  "direccion_destino": "Calle Secundaria 200, Barcelona, 08001, España",
  "peso_kg": 2.5,
  "eventos": [...]
}
```

### Otros Endpoints

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/envios` | Listar todos |
| GET | `/api/envios?estado=EN_TRANSITO` | Filtrar por estado |
| GET | `/api/envios/tracking/{number}` | Buscar por tracking |
| PUT | `/api/envios/{id}/estado` | Actualizar estado |
| PUT | `/api/envios/{id}/transportista` | Asignar transportista |

## 🧪 Flujo en Postman

1. **Crear envío** con POST → obtienes JSON con `id`
2. **Copiar el `id`** del response
3. **Obtener envío** con GET usando ese `id`
4. Ver todos los datos en formato JSON

## 📦 Estados

`PENDIENTE` → `EN_PREPARACION` → `EN_TRANSITO` → `EN_DISTRIBUCION` → `ENTREGADO`

## 🏗️ Arquitectura

```
src/
├── dominio/          # Lógica de negocio
├── aplicacion/       # Casos de uso
├── infraestructura/  # BD, HTTP, etc.
└── presentacion/     # API REST
```

## 🛠️ Local

```bash
pip install -r requirements.txt
python main.py
# http://localhost:5000
```

## 🔧 Tecnologías

Python 3.11, Flask, Marshmallow, Gunicorn

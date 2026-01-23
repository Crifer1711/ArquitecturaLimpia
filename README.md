# 📦 Microservicio de Gestión de Envíos

Arquitectura Limpia + DDD - Simple y Efectivo

## 🏗️ Arquitectura (4 Capas)

```
PRESENTACIÓN (API REST)
        ↓
APLICACIÓN (Casos de Uso)
        ↓
DOMINIO (Lógica de Negocio)
        ↑
INFRAESTRUCTURA (Persistencia)
```

### Estructura del Código

```
src/
├── dominio/              # CAPA 1: Lógica de negocio
│   ├── envio.py         # Agregado Raíz
│   └── repositorio.py   # Interfaz (Puerto)
│
├── aplicacion/          # CAPA 2: Casos de uso
│   └── casos_uso.py     # 5 casos de uso
│
├── infraestructura/     # CAPA 3: Implementaciones
│   └── repositorio_memoria.py
│
└── presentacion/        # CAPA 4: API REST
    └── api.py           # Endpoints Flask
```

## 🚀 Instalación

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python main.py
```

## 📡 API Endpoints

### 1. Crear Envío
```http
POST http://localhost:5000/envios
Content-Type: application/json

{
  "pedido_id": "PED-001",
  "origen": "Bogotá, Colombia",
  "destino": "Medellín, Colombia",
  "peso": 2.5
}
```

### 2. Listar Envíos
```http
GET http://localhost:5000/envios
```

### 3. Obtener Envío
```http
GET http://localhost:5000/envios/{id}
```

### 4. Asignar Transportista
```http
PUT http://localhost:5000/envios/{id}/transportista
Content-Type: application/json

{
  "transportista_id": "TRANS-001"
}
```

### 5. Actualizar Estado
```http
PUT http://localhost:5000/envios/{id}/estado
Content-Type: application/json

{
  "estado": "EN_TRANSITO"
}
```

**Estados válidos:** `PENDIENTE`, `EN_PREPARACION`, `EN_TRANSITO`, `ENTREGADO`

## 🌐 Deploy en Render

1. Sube el código a GitHub
2. En Render.com: New Web Service
3. Conecta tu repo
4. Render detecta automáticamente el `render.yaml`
5. ¡Listo!

## 🎯 DDD Aplicado

- **Agregado:** `Envio` - Controla toda la lógica del envío
- **Reglas de Negocio:**
  - Peso debe ser > 0
  - Solo se puede asignar transportista en estado PENDIENTE
  - Historial completo de cambios de estado

## 📚 Arquitectura Limpia

- **Dominio:** Lógica pura, sin dependencias externas
- **Aplicación:** Coordina casos de uso
- **Infraestructura:** Implementa persistencia
- **Presentación:** Expone API REST

---

**Simple, limpio y funcional** ✨

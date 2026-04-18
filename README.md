# Sistema de Gestión de Almacén Frío

Sistema ERP profesional para la gestión de almacenes frigoríficos, desarrollado con FastAPI (backend) y HTML/CSS/JavaScript vanilla (frontend).

## Características

- ✅ Gestión de múltiples almacenes (Frío, Seco, Contenedores)
- ✅ Sistema de ubicaciones con capacidad de pallet (A1-A4, B1-B4, etc.)
- ✅ Control de inventario por ubicación
- ✅ Óculo automático de ubicaciones llenas
- ✅ Interfaz profesional con diseño Navy ERP
- ✅ Localización en español
- ✅ Tecnología SQLite con SQLAlchemy ORM

## Estructura del Proyecto

```
coldstore-manager/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app setup
│   ├── database.py          # Database configuration
│   ├── crud/
│   │   └── crud.py          # CRUD operations
│   ├── models/
│   │   └── models.py        # SQLAlchemy models
│   ├── routers/
│   │   ├── warehouses.py
│   │   ├── locations.py
│   │   ├── items.py
│   │   └── warehouse.py
│   ├── schemas/
│   │   └── schemas.py       # Pydantic schemas
│   └── utils/
│       ├── schema.sql
│       └── seed.py          # Database seeding
├── static/
│   └── index.html           # Frontend
├── create_db.py
├── run.py                   # Server entry point
├── requirements.txt
└── .env
```

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/yourusername/coldstore-manager.git
cd coldstore-manager
```

### 2. Crear ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python create_db.py
python -m app.utils.seed
```

### 5. Ejecutar servidor
```bash
python run.py
```

El servidor estará disponible en: **http://localhost:8000**

## Tecnología

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Base de Datos**: SQLite
- **Server**: Uvicorn con hot reload

## Modelos de Datos

### Warehouse (Almacén)
- Código único
- Nombre
- Tipo (cold, dry, container)
- Descripción

### Location (Ubicación)
- Código (A1, A2, A3, A4, B1...)
- Almacén asociado
- Capacidad (default: 4 pallets)
- Estado (disponible)
- Contador de items

### Item (Producto/Pallet)
- Nombre del producto
- Peso
- Fechas de entrada y caducidad
- Lote
- Etiqueta (Integer)
- Ubicación

## API Endpoints

### Almacenes
- `GET /warehouses/` - Listar todos
- `POST /warehouses/` - Crear nuevo

### Ubicaciones
- `GET /locations/warehouse/{warehouse_id}` - Listar por almacén
- `POST /locations/` - Crear nueva

### Productos
- `GET /items/` - Listar todos
- `POST /items/` - Crear nuevo
- `DELETE /items/{item_id}` - Eliminar

## Variables de Entorno

```
DATABASE_URL=sqlite:///./coldstore.db
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.

## Autor

Desarrollado para Cesun Frigorífico

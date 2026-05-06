# Resident Evil Franchise Tracker API

API REST para un archivo digital clasificado de juegos de Resident Evil, con estetica Umbrella Records y backend separado del frontend.

## Descripcion general

Este backend expone una API JSON construida con FastAPI. No genera HTML ni contiene frontend: su responsabilidad es servir datos al cliente mediante endpoints REST documentados con Swagger UI y OpenAPI.

La API se conecta a PostgreSQL y maneja:

- Juegos del archivo (`/series`)
- Ratings personales por juego
- Activity logs reales
- Estadisticas de dashboard
- Upload de portadas con Cloudinary

## Stack tecnologico

- Python
- FastAPI
- SQLModel
- PostgreSQL
- Pydantic
- Uvicorn
- Cloudinary
- Docker / Docker Compose
- Preparacion para deploy en Render + Neon

## Arquitectura

El proyecto sigue una **Umbrella Archive Modular Architecture**:

- `app/core`: configuracion, CORS, constantes, errores y response models base.
- `app/db`: conexion, inicializacion y seed de base de datos.
- `app/modules/archive_entries`: dominio principal de juegos del archivo.
- `app/modules/personal_ratings`: rating personal por juego.
- `app/modules/activity_logs`: historial de actividad.
- `app/modules/dashboard`: estadisticas para pantalla principal.
- `app/modules/cover_assets`: subida de portadas a Cloudinary.
- `app/shared`: utilidades compartidas de fechas, labels, codigos visuales, paginacion y sorting.

Cada modulo puede contener:

- `router`: endpoints FastAPI.
- `service`: reglas de negocio y transacciones.
- `repository`: consultas y persistencia.
- `mapper`: conversion de datos internos a contratos de respuesta.
- `schemas`: contratos Pydantic.
- `model`: modelo SQLModel cuando el modulo persiste datos.

## Estructura principal

```text
resident-evil-tracker-api/
├── app/
│   ├── core/
│   ├── db/
│   ├── modules/
│   │   ├── activity_logs/
│   │   ├── archive_entries/
│   │   ├── cover_assets/
│   │   ├── dashboard/
│   │   └── personal_ratings/
│   ├── shared/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Variables de entorno

Usa `.env.example` como referencia. El archivo `.env` real no debe subirse al repositorio.

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/resident_evil_tracker

APP_NAME=Resident Evil Franchise Tracker API
APP_ENV=development
APP_VERSION=0.1.0

BACKEND_CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500,http://localhost:5173,http://127.0.0.1:5173

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_FOLDER=resident-evil-tracker/covers
```

Notas:

- `.env.example` no contiene secretos reales.
- `DATABASE_URL` apunta a PostgreSQL.
- Cloudinary es opcional para levantar la API y usar el resto de endpoints.
- Cloudinary es requerido para que `POST /series/{id}/cover` suba imagenes reales.
- Docker Compose permite cambiar el puerto del PostgreSQL local con `POSTGRES_HOST_PORT`.

## Instalacion local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## PostgreSQL con Docker

```bash
docker compose up -d
```

Por defecto, `docker-compose.yml` publica PostgreSQL en `5432`. Puedes cambiarlo con:

```bash
POSTGRES_HOST_PORT=5434 docker compose up -d
```

Si usas el servicio de DB de Docker desde el host, ajusta `DATABASE_URL` en `.env` segun el puerto publicado.

## Inicializar base de datos

```bash
python -m app.db.init_db
```

Este comando crea las tablas registradas por SQLModel si no existen.

## Ejecutar seed

```bash
python -m app.db.seed_archive
```

El seed inicializa la base si hace falta y carga juegos, ratings y activity logs iniciales. Esta pensado para ser idempotente: evita duplicar registros ya existentes.

## Ejecutar API local

```bash
uvicorn app.main:app --reload
```

URLs locales:

- API local: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- Health check: `http://localhost:8000/health`

## Endpoints principales

| Area | Metodo | Endpoint | Descripcion |
| --- | --- | --- | --- |
| Health | GET | `/health` | Estado de la API |
| Series | GET | `/series` | Listado paginado de juegos |
| Series | GET | `/series/{id}` | Detalle de un juego |
| Series | POST | `/series` | Crear juego |
| Series | PUT | `/series/{id}` | Actualizar juego |
| Series | DELETE | `/series/{id}` | Eliminar juego |
| Ratings | GET | `/series/{id}/rating` | Obtener rating de un juego |
| Ratings | POST | `/series/{id}/rating` | Crear rating |
| Ratings | PUT | `/series/{id}/rating` | Actualizar rating |
| Ratings | DELETE | `/series/{id}/rating` | Eliminar rating |
| Activity | GET | `/activity` | Actividad reciente global |
| Activity | GET | `/series/{id}/activity` | Actividad de un juego |
| Dashboard | GET | `/dashboard/stats` | Estadisticas principales |
| Cover | POST | `/series/{id}/cover` | Subir portada a Cloudinary |

### Query params de `/series`

- `q`: busqueda por texto.
- `sort`: `title`, `release_year`, `chronology_order`, `rating`, `created_at`.
- `order`: `asc` o `desc`.
- `page`: pagina, desde `1`.
- `limit`: elementos por pagina, de `1` a `50`.

## Ejemplos basicos

Health:

```bash
curl http://localhost:8000/health
```

Listado paginado:

```bash
curl "http://localhost:8000/series?page=1&limit=8"
```

Busqueda:

```bash
curl "http://localhost:8000/series?q=remake"
```

Orden por rating:

```bash
curl "http://localhost:8000/series?sort=rating&order=desc"
```

Crear juego con JSON minimo:

```bash
curl -X POST http://localhost:8000/series \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Resident Evil Custom Entry",
    "release_year": 2024,
    "main_protagonist": "Test Protagonist",
    "original_platform": "PC",
    "chronology_order": 99,
    "description": "Registro de prueba para el archivo Umbrella."
  }'
```

Crear rating:

```bash
curl -X POST http://localhost:8000/series/1/rating \
  -H "Content-Type: application/json" \
  -d '{"score": 9.6, "review": "Excelente registro."}'
```

Subir portada:

```bash
curl -X POST http://localhost:8000/series/1/cover \
  -F "file=@cover.png;type=image/png"
```

## Codigos HTTP

- `200`: operacion exitosa.
- `201`: recurso creado.
- `204`: operacion exitosa sin body.
- `400`: archivo o request invalido controlado.
- `404`: recurso no encontrado.
- `409`: conflicto, por ejemplo rating duplicado.
- `422`: validacion Pydantic/FastAPI.
- `503`: Cloudinary no configurado para upload real.

## Formato de error JSON

Los errores se responden con una estructura consistente:

```json
{
  "error": "ValidationError",
  "message": "String should have at least 2 characters",
  "field": "title",
  "status_code": 422
}
```

## Features implementadas / challenges cubiertos

- API REST separada del frontend.
- Swagger UI.
- OpenAPI JSON.
- PostgreSQL.
- CRUD completo de juegos.
- Busqueda.
- Ordenamiento.
- Paginacion.
- Ratings personales.
- Subida de imagenes con Cloudinary.
- Validaciones server-side.
- Codigos HTTP correctos.
- Activity logs reales.
- Dashboard stats.
- CORS.
- Seed idempotente.
- Arquitectura modular.

## Preparacion deploy

### Render

1. Crear un Web Service.
2. Conectar el repositorio.
3. Configurar build command:

```bash
pip install -r requirements.txt
```

4. Configurar start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Configurar variables de entorno en Render.

### Neon

1. Crear una base PostgreSQL.
2. Copiar el connection string.
3. Configurarlo en Render como `DATABASE_URL`.
4. Ejecutar inicializacion y seed desde un entorno con acceso a la DB, si aplica.

### Cloudinary

Configurar en Render:

- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `CLOUDINARY_FOLDER`

No se incluye URL de produccion porque depende del deploy final.

## Comandos de verificacion

Compilacion:

```bash
python -m compileall app
```

Imports principales:

```bash
python -c "from app.main import app; print(app.title)"
python -c "from app.modules.dashboard.dashboard_service import DashboardService; print(callable(DashboardService))"
python -c "from app.modules.cover_assets.cover_service import CoverService; print(callable(CoverService))"
```

Verificar rutas principales en OpenAPI:

```bash
python - <<'PY'
from app.main import app

for path in sorted(app.openapi()["paths"].keys()):
    print(path)
PY
```

## Estado del backend

El backend esta listo para conectarse al frontend vanilla del proyecto.

## Notas importantes

- No hay login ni usuarios.
- No hay roles.
- No hay frontend dentro de este repositorio.
- El endpoint publico usa `/series`, pero internamente el dominio se maneja como `archive_entries`.
- Cloudinary requiere credenciales para upload real.

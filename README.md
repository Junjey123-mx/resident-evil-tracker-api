# Resident Evil Franchise Tracker — API

API REST para el archivo digital clasificado de la franquicia Resident Evil. Backend completamente independiente del frontend: sirve datos JSON a través de endpoints REST, persiste en PostgreSQL y gestiona imágenes con Cloudinary.

---

## Enlaces del proyecto

| Recurso | Link |
|---|---|
| Backend GitHub | https://github.com/Junjey123-mx/resident-evil-tracker-api |
| Frontend GitHub | https://github.com/Junjey123-mx/resident-evil-tracker-client |
| Backend publicado | https://resident-evil-tracker-api-byct.vercel.app |
| Frontend publicado | http://158.23.57.118/vernel/resident-evil-tracker-client/ |

---

## Descripción general

Este backend expone una API JSON construida con FastAPI. No genera HTML ni contiene frontend: su responsabilidad es servir datos al cliente mediante endpoints REST documentados con Swagger UI y OpenAPI.

La API se conecta a PostgreSQL y maneja:

- Juegos del archivo (`/series`)
- Ratings personales por juego
- Activity logs reales
- Estadísticas de dashboard
- Upload de portadas con Cloudinary

---

## Stack tecnológico

| Tecnología | Rol |
|---|---|
| Python 3.12 | Lenguaje principal |
| FastAPI | Framework web y documentación automática |
| SQLModel | ORM y modelos de base de datos |
| Pydantic | Validación y serialización |
| PostgreSQL | Base de datos relacional |
| Uvicorn | Servidor ASGI |
| Cloudinary | Almacenamiento de imágenes |
| Docker / Docker Compose | Contenedorización y DB local |
| Vercel | Deploy del backend |
| Supabase | PostgreSQL en la nube |

---

## Arquitectura

El proyecto sigue una arquitectura modular por dominio:

- `app/core`: configuración, CORS, constantes, errores y response models base.
- `app/db`: conexión, inicialización y seed de base de datos.
- `app/modules/archive_entries`: dominio principal de juegos del archivo.
- `app/modules/personal_ratings`: rating personal por juego.
- `app/modules/activity_logs`: historial de actividad.
- `app/modules/dashboard`: estadísticas para pantalla principal.
- `app/modules/cover_assets`: subida de portadas a Cloudinary.
- `app/shared`: utilidades compartidas de fechas, labels, códigos visuales, paginación y sorting.

Cada módulo puede contener:

- `router`: endpoints FastAPI.
- `service`: reglas de negocio y transacciones.
- `repository`: consultas y persistencia.
- `mapper`: conversión de datos internos a contratos de respuesta.
- `schemas`: contratos Pydantic.
- `model`: modelo SQLModel cuando el módulo persiste datos.

---

## Estructura principal

```
resident-evil-tracker-api/
├── app/
│   ├── core/               ← Configuración, CORS, errores, response models
│   ├── db/                 ← Conexión, inicialización, seed y schema SQL
│   ├── modules/
│   │   ├── activity_logs/  ← Historial de actividad
│   │   ├── archive_entries/← CRUD de juegos del archivo
│   │   ├── cover_assets/   ← Upload de portadas a Cloudinary
│   │   ├── dashboard/      ← Estadísticas del dashboard
│   │   └── personal_ratings/← Ratings personales
│   ├── shared/             ← Fechas, labels, paginación, sorting, códigos
│   └── main.py             ← Punto de entrada de la aplicación
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Variables de entorno

Copia `.env.example` a `.env` y completa los valores reales. El archivo `.env` no debe subirse al repositorio.

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/resident_evil_tracker

APP_NAME=Resident Evil Franchise Tracker API
APP_ENV=development
APP_VERSION=0.1.0

BACKEND_CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_FOLDER=resident-evil-tracker/covers
```

Notas:

- `DATABASE_URL` apunta a PostgreSQL local o en la nube.
- Cloudinary es opcional para levantar la API; el resto de endpoints funciona sin él.
- Cloudinary es requerido para que `POST /series/{id}/cover` suba imágenes reales.
- En producción, agregar el dominio del frontend publicado a `BACKEND_CORS_ORIGINS`.

---

## Instalación y ejecución local

### Opción A — Python directo (sin Docker para la API)

Requiere PostgreSQL corriendo en local o vía Docker.

```bash
# 1. Clonar el repositorio
git clone https://github.com/Junjey123-mx/resident-evil-tracker-api.git
cd resident-evil-tracker-api

# 2. Crear entorno virtual e instalar dependencias
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
# .venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 3. Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con los valores correctos

# 4. Levantar PostgreSQL con Docker (o usar una instancia local)
docker compose up -d resident-evil-tracker-db

# 5. Inicializar la base de datos
python -m app.db.init_db

# 6. Cargar el seed de datos
python -m app.db.seed_archive

# 7. Ejecutar la API
uvicorn app.main:app --reload
```

### Opción B — Docker Compose completo

```bash
# Levantar API y base de datos juntos
docker compose up -d

# Inicializar y cargar seed (primera vez)
docker compose exec resident-evil-tracker-api python -m app.db.init_db
docker compose exec resident-evil-tracker-api python -m app.db.seed_archive
```

**URLs locales:**

| Recurso | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| OpenAPI JSON | http://localhost:8000/openapi.json |
| Health check | http://localhost:8000/health |

---

## Endpoints principales

| Área | Método | Endpoint | Descripción |
|---|---|---|---|
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
| Dashboard | GET | `/dashboard/stats` | Estadísticas principales |
| Cover | POST | `/series/{id}/cover` | Subir portada a Cloudinary |

### Query params de `/series`

| Parámetro | Tipo | Descripción |
|---|---|---|
| `q` | string | Búsqueda por texto en título |
| `sort` | string | Campo de ordenamiento: `title`, `release_year`, `chronology_order`, `rating`, `created_at` |
| `order` | string | Dirección: `asc` o `desc` |
| `page` | int | Página, desde `1` |
| `limit` | int | Elementos por página, de `1` a `50` |

---

## Ejemplos con curl

```bash
# Health check
curl http://localhost:8000/health

# Listado paginado
curl "http://localhost:8000/series?page=1&limit=8"

# Búsqueda
curl "http://localhost:8000/series?q=remake"

# Orden por rating descendente
curl "http://localhost:8000/series?sort=rating&order=desc"

# Detalle de un juego
curl http://localhost:8000/series/1

# Crear juego
curl -X POST http://localhost:8000/series \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Resident Evil Custom Entry",
    "release_year": 2024,
    "main_protagonist": "Test Protagonist",
    "original_platform": "PC",
    "chronology_order": 99,
    "description": "Registro de prueba para el archivo Umbrella.",
    "category": "main_series",
    "status": "registered",
    "threat_level": "high"
  }'

# Crear rating
curl -X POST http://localhost:8000/series/1/rating \
  -H "Content-Type: application/json" \
  -d '{"score": 9.6, "review": "Excelente registro."}'

# Subir portada
curl -X POST http://localhost:8000/series/1/cover \
  -F "file=@cover.png;type=image/png"

# Dashboard stats
curl http://localhost:8000/dashboard/stats

# Eliminar juego
curl -X DELETE http://localhost:8000/series/1
```

---

## Valores de enumeraciones

Los campos `category`, `status` y `threat_level` aceptan los siguientes valores exactos:

### category

| Valor | Etiqueta |
|---|---|
| `main_series` | JUEGO PRINCIPAL |
| `remake` | REMAKE |
| `prequel` | PRECUELA |
| `spin_off` | SPIN-OFF |
| `expansion` | EXPANSIÓN |

### status

| Valor | Etiqueta |
|---|---|
| `registered` | REGISTERED |
| `pending` | PENDING |
| `archived` | ARCHIVED |

### threat_level

| Valor | Etiqueta |
|---|---|
| `low` | LOW |
| `medium` | MEDIUM |
| `high` | HIGH |
| `critical` | CRITICAL |

---

## Códigos HTTP

| Código | Significado |
|---|---|
| `200` | Operación exitosa |
| `201` | Recurso creado |
| `204` | Operación exitosa sin cuerpo de respuesta |
| `400` | Archivo o request inválido controlado |
| `404` | Recurso no encontrado |
| `409` | Conflicto (ej. rating duplicado) |
| `422` | Error de validación Pydantic/FastAPI |
| `503` | Cloudinary no configurado para upload real |

---

## Formato de error JSON

Todos los errores responden con una estructura consistente:

```json
{
  "error": "ValidationError",
  "message": "String should have at least 2 characters",
  "field": "title",
  "status_code": 422
}
```

---

## CORS

El backend tiene configurado `CORSMiddleware` de FastAPI. La lista de orígenes permitidos se define en la variable de entorno `BACKEND_CORS_ORIGINS`.

**¿Por qué es necesario?**
El frontend corre en un origen distinto al backend (diferente puerto o dominio). El navegador bloquea las respuestas cross-origin a menos que el servidor envíe la cabecera `Access-Control-Allow-Origin` con el origen del cliente autorizado.

**En producción:**
Agregar la URL del frontend publicado (ej. `http://158.23.57.118`) a `BACKEND_CORS_ORIGINS` en Vercel antes del deploy. Sin esto, el frontend publicado no podrá comunicarse con el backend.

---

## Separación cliente / servidor

Este repositorio contiene únicamente el backend:

- No genera HTML ni sirve archivos estáticos.
- No conoce la URL del frontend en tiempo de ejecución.
- Toda la comunicación con el cliente ocurre vía HTTP con respuestas JSON.
- El frontend está en un repositorio separado: [resident-evil-tracker-client](https://github.com/Junjey123-mx/resident-evil-tracker-client).

Esta separación permite desplegar cada parte de forma independiente en cualquier servicio compatible.

---

## Challenges implementados

- API REST completamente separada del frontend
- Documentación automática con Swagger UI y OpenAPI
- CRUD completo de juegos del archivo
- Búsqueda por texto en título
- Ordenamiento configurable por múltiples campos
- Paginación con metadatos (`total`, `pages`, `has_next`, `has_previous`)
- Ratings personales por juego (crear, leer, actualizar, eliminar)
- Subida y gestión de imágenes de portada con Cloudinary
- Activity logs reales por cada operación del sistema
- Dashboard con estadísticas agregadas (total, promedio, mejor calificado, últimos registros, top rated, timeline, actividad reciente)
- Validaciones server-side con Pydantic y códigos HTTP correctos
- Manejo de conflictos (rating duplicado → 409)
- Formato de error JSON consistente en todos los endpoints
- CORS configurado para orígenes múltiples vía variable de entorno
- Seed idempotente: carga datos iniciales sin duplicar si ya existen
- Arquitectura modular por dominio
- Deploy en Vercel con Supabase (PostgreSQL en la nube)

---

## Reflexión sobre la tecnología y los challenges

FastAPI fue la elección correcta para este proyecto: la generación automática de documentación con Swagger UI desde las anotaciones de tipo de Python elimina la necesidad de mantener documentación separada, y la validación con Pydantic convierte los errores de entrada en respuestas HTTP estructuradas sin código adicional.

El mayor reto arquitectónico fue definir los contratos de respuesta correctamente desde el inicio. En un sistema donde el frontend consume exactamente lo que el backend devuelve, cualquier inconsistencia en los nombres de campo o en los valores de enumeraciones produce errores en el cliente que son difíciles de rastrear. Establecer los contratos Pydantic primero y construir el frontend después de validarlos resultó ser el flujo correcto.

La separación en módulos por dominio (archive_entries, personal_ratings, activity_logs, dashboard, cover_assets) mantuvo cada área de responsabilidad aislada y facilitó el testing manual de cada parte de forma independiente. La capa de `mapper` que convierte entidades de base de datos en contratos de respuesta fue clave para evitar filtrar campos internos al cliente.

PostgreSQL con SQLModel fue suficiente para las necesidades del proyecto: relaciones simples, consultas de agregación para el dashboard y persistencia confiable. Cloudinary resolvió el almacenamiento de imágenes sin necesidad de gestionar un servidor de archivos propio.

---

## Deploy en Vercel + Supabase

### Supabase (PostgreSQL)

1. Crear un proyecto en [supabase.com](https://supabase.com).
2. Ir a Settings → Database → Connection string (Transaction pooler, puerto 6543).
3. Configurar las variables de conexión en Vercel.

### Vercel (API)

1. Conectar este repositorio en Vercel.
2. Configurar variables de entorno en Vercel → Settings → Environment Variables:

| Variable | Valor |
|---|---|
| `DB_USER` | Usuario de Supabase (ej. `postgres.xxxxxxxxxxxx`) |
| `DB_PASSWORD` | Contraseña de Supabase |
| `DB_HOST` | Host del pooler de Supabase |
| `DB_PORT` | `6543` |
| `DB_NAME` | `postgres` |
| `BACKEND_CORS_ORIGINS` | URL del frontend publicado |
| `CLOUDINARY_CLOUD_NAME` | Credencial de Cloudinary |
| `CLOUDINARY_API_KEY` | Credencial de Cloudinary |
| `CLOUDINARY_API_SECRET` | Credencial de Cloudinary |
| `CLOUDINARY_FOLDER` | `resident-evil-tracker/covers` |

> Se usan variables separadas para la conexión (`DB_*`) en lugar de `DATABASE_URL` completa, para evitar problemas de encoding con caracteres especiales en la contraseña.

3. Redeploy tras configurar las variables.

**URL backend publicado:** https://resident-evil-tracker-api-byct.vercel.app

---

## Comandos de verificación

```bash
# Verificar compilación
python -m compileall app

# Verificar imports principales
python -c "from app.main import app; print(app.title)"

# Ver todas las rutas registradas
python - <<'PY'
from app.main import app
for path in sorted(app.openapi()["paths"].keys()):
    print(path)
PY
```

---

## Notas

- No hay sistema de autenticación ni usuarios.
- No hay roles ni permisos.
- No hay frontend dentro de este repositorio.
- El endpoint público usa `/series`, pero internamente el dominio se llama `archive_entries`.
- Cloudinary requiere credenciales válidas para subir imágenes reales; sin ellas, el endpoint devuelve `503`.

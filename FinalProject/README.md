# FinalProject - Orders Service

## Descripción

Proyecto final integrador sencillo basado en arquitectura hexagonal/limpia.

El sistema implementa un servicio de órdenes con:

- dominio
- casos de uso
- puertos y adaptadores
- API con FastAPI
- persistencia con SQLAlchemy
- migraciones con Alembic
- pruebas
- Docker
- CI
- auditoría de dependencias

## Estructura

- `src/final_orders/domain`: reglas de negocio y eventos
- `src/final_orders/application`: casos de uso y puertos
- `src/final_orders/infrastructure`: base de datos, repositorios y publisher
- `src/final_orders/adapters/api`: API HTTP
- `tests/`: pruebas unitarias, contrato, integración y e2e
- `alembic/`: migraciones
- `.github/workflows/ci.yml`: pipeline de CI
- `docs/`: material para exposición

## Flujo general

1. El cliente llama `POST /orders`
2. FastAPI valida el request
3. El adaptador API invoca el caso de uso
4. El caso de uso crea la entidad de dominio
5. El repositorio guarda la orden
6. Se publica el evento `OrderCreated`
7. La API responde con la orden creada

## Seguridad

La API usa una llave simple por header:

- `x-api-key: demo-key`

Puedes cambiarla en `.env`.

## Cómo ejecutarlo

### 1. Instalar dependencias

- `poetry install`

### 2. Crear `.env`

Copia `.env.example` a `.env`

### 3. Ejecutar migraciones

- `poetry run alembic upgrade head`

### 4. Levantar API

- `poetry run final-api`

O también:

- `poetry run uvicorn final_orders.app:app --reload`

### 5. Abrir documentación

- `http://127.0.0.1:8000/docs`

### 6. Probar endpoint principal

`POST /orders`

Header:

- `x-api-key: demo-key`

Body de ejemplo:

```json
{
  "order_id": 1,
  "customer": "Marco",
  "items": [
    {
      "sku": "A1",
      "name": "Mouse",
      "unit_price": 100,
      "qty": 2
    }
  ]
}
```

## Cómo correr pruebas

- `poetry run pytest`

## Calidad

- `poetry run ruff check src tests`
- `poetry run black --check src tests`
- `poetry run mypy src`

## Auditoría de dependencias

- `poetry run pip-audit`
- `poetry run safety scan`

## Docker

### Build

- `docker build -t final-orders .`

### Run

- `docker run -p 8000:8000 --env-file .env final-orders`

## CI/CD

El pipeline en `.github/workflows/ci.yml` ejecuta:

- instalación
- lint
- format check
- type check
- pruebas
- auditoría de dependencias

## Diagramas y apoyo para exposición

Revisa:

- `docs/architecture.md`
- `docs/manual_exposicion.md`
- `docs/preguntas_posibles.md`

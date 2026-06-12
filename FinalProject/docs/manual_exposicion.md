# Manual de exposición

## Cómo explicar el proyecto en vivo

### 1. Empieza por el objetivo

"Este proyecto implementa un servicio de órdenes usando arquitectura hexagonal para separar la lógica de negocio de la infraestructura y de la API."

### 2. Explica las capas

- Dominio: contiene las reglas del negocio
- Aplicación: contiene los casos de uso
- Infraestructura: conecta con base de datos
- Adaptadores: exponen la API

### 3. Explica el flujo de crear una orden

1. entra una petición `POST /orders`
2. FastAPI valida el body
3. se verifica la API key
4. se llama al caso de uso `CreateOrderUseCase`
5. se crea la entidad `Order`
6. se valida la orden
7. se guarda con el repositorio SQLAlchemy
8. se publica el evento `OrderCreated`
9. se responde al cliente

### 4. Explica por qué es arquitectura limpia

- el dominio no conoce FastAPI
- el dominio no conoce SQLAlchemy
- la aplicación depende de puertos, no de implementaciones concretas
- la infraestructura implementa esos puertos

### 5. Explica la calidad

- pruebas unitarias para dominio
- pruebas de contrato para API
- pruebas de integración para repositorio
- pruebas e2e para flujo completo
- lint, format y type check
- Docker y CI

### 6. Explica seguridad

- uso de `.env`
- `pydantic-settings`
- API key en header
- auditoría con `pip-audit` y `safety`

## Demo sugerida

1. mostrar estructura de carpetas
2. mostrar `domain/entities.py`
3. mostrar `application/use_cases.py`
4. mostrar `infrastructure/repositories/sqlalchemy_order_repository.py`
5. mostrar `adapters/api/routes.py`
6. correr migraciones
7. levantar API
8. abrir `/docs`
9. crear una orden
10. listar órdenes

# Arquitectura del proyecto

## Capas

### 1. Dominio

Contiene las reglas de negocio puras:

- `Order`
- `OrderItem`
- `OrderCreated`

No depende de FastAPI ni de SQLAlchemy.

### 2. Aplicación

Contiene los casos de uso:

- `CreateOrderUseCase`
- `GetOrderUseCase`
- `ListOrdersUseCase`

También define los puertos:

- `OrderRepository`
- `EventPublisher`

### 3. Infraestructura

Implementa detalles técnicos:

- SQLAlchemy
- repositorio concreto
- publisher en memoria
- sesión a base de datos

### 4. Adaptadores

Expone el sistema al exterior:

- FastAPI
- esquemas de entrada/salida
- dependencias de seguridad

## Diagrama simple

```text
Cliente HTTP
   |
   v
FastAPI Router
   |
   v
Use Cases
   |
   +--> OrderRepository (puerto) ---> SqlAlchemyOrderRepository
   |
   +--> EventPublisher (puerto) ---> InMemoryEventPublisher
   |
   v
Dominio (Order, OrderItem, OrderCreated)
```

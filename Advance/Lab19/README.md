# Lab19 - Interoperabilidad y ecosistema mixto

## Objetivo

Crear un ejemplo simple de interoperabilidad con:

- contrato neutral en `Protobuf`
- servidor y cliente `gRPC` en Python
- publicación de evento `OrderCreated`
- integración sencilla con `Redis` como broker de eventos

## Qué incluye

- `proto/orders.proto`: contrato del servicio Orders
- `src/lab_interop/generated/`: stubs simples incluidos para el laboratorio
- `src/lab_interop/server.py`: servidor gRPC
- `src/lab_interop/client.py`: cliente gRPC
- `src/lab_interop/publisher.py`: publicación de evento `OrderCreated`
- `tests/`: pruebas básicas

## Flujo del laboratorio

1. El cliente llama `CreateOrder`
2. El servidor recibe el request gRPC
3. Guarda la orden en memoria
4. Publica el evento `OrderCreated`
5. El cliente consulta la orden con `GetOrder`

## Contrato Protobuf

El archivo `proto/orders.proto` define:

- `OrdersService`
- `CreateOrder`
- `GetOrder`
- mensajes `Order`, `OrderItem`, `CreateOrderRequest`, `CreateOrderResponse`

## Broker de eventos

Se usa `Redis` de forma simple.

Si Redis está disponible en `localhost:6379`, el evento se publica en el canal:

- `orders.events`

Si Redis no está disponible, el laboratorio sigue funcionando y conserva el evento en memoria para fines didácticos.

> No es obligatorio tener Redis levantado para probar el flujo gRPC.

## Cómo probarlo

### 1. Instalar dependencias

Desde `Advance/Lab19`:

- `poetry install`

### 2. Ejecutar pruebas

- `poetry run pytest`

### 3. Levantar el servidor gRPC

En una terminal:

- `poetry run grpc-server`

Debes ver algo similar a:

- `gRPC server running on port 50051`

### 4. Ejecutar el cliente gRPC

En otra terminal:

- `poetry run grpc-client`

Esto hará:

- crear una orden
- consultar la orden creada

### 5. Regenerar stubs desde el .proto

Si quieres regenerarlos:

- `poetry run generate-stubs`

> Para el laboratorio ya se incluyen stubs simples listos para entender el flujo. Si generas stubs reales con `grpcio-tools`, pueden reemplazarse después.

### 6. Probar publicación en Redis

Si tienes Redis local, puedes ejecutarlo y suscribirte al canal `orders.events`.

Por ejemplo, con `redis-cli`:

- `SUBSCRIBE orders.events`

Luego ejecuta otra vez el cliente:

- `poetry run grpc-client`

Deberías ver el evento `OrderCreated` publicado en el canal.

## Resultado esperado

Este laboratorio cumple lo esencial de la práctica:

- define un contrato neutral con `.proto`
- usa gRPC entre cliente y servidor
- serializa con Protobuf
- publica un evento `OrderCreated`
- integra mensajería de forma simple con Redis

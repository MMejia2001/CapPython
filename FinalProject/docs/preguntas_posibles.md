# Preguntas posibles y respuestas

## 1. ¿Por qué usaste arquitectura hexagonal?
Porque permite separar la lógica de negocio de la tecnología. Así el dominio no depende de FastAPI ni de SQLAlchemy.

## 2. ¿Qué son los puertos y adaptadores?
Los puertos son interfaces que define la aplicación. Los adaptadores son implementaciones concretas para base de datos, API o eventos.

## 3. ¿Dónde está la lógica de negocio?
En `domain` y en los casos de uso de `application`.

## 4. ¿Qué ventaja tiene usar casos de uso?
Centralizan acciones del sistema y hacen más fácil probar el comportamiento.

## 5. ¿Por qué el dominio no usa SQLAlchemy?
Porque el dominio debe ser independiente de infraestructura para ser más limpio, reusable y fácil de probar.

## 6. ¿Qué tipo de pruebas tiene el proyecto?
Unitarias, de contrato, de integración y end-to-end.

## 7. ¿Qué hace Alembic?
Administra migraciones de base de datos para crear y versionar tablas.

## 8. ¿Qué hace Docker aquí?
Empaqueta la aplicación para ejecutarla de forma consistente en cualquier entorno.

## 9. ¿Qué valida la API key?
Que solo clientes autorizados puedan consumir la API.

## 10. ¿Cómo aseguras calidad?
Con pruebas, lint, formateo, tipado, pipeline CI y auditoría de dependencias.

## 11. ¿Qué podrías mejorar después?
Agregar autenticación JWT, observabilidad con logs estructurados, métricas, cache, colas de eventos y mejor manejo transaccional.

## 12. ¿Por qué este proyecto es sencillo?
Porque está pensado para aprender y exponer claramente cada capa sin agregar demasiada complejidad.

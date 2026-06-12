# Lab18 - Seguridad y mantenimiento

## Objetivo

Aplicar lo esencial de seguridad y mantenimiento en un proyecto Python usando Poetry:

- configuración con `pydantic-settings`
- secretos fuera del código
- auditoría con `pip-audit` y `safety`
- contenedor con usuario no root y permisos mínimos

## Estructura

- `app.py`: API mínima con endpoints de verificación
- `src/lab_security/settings.py`: configuración centralizada
- `src/lab_security/audit.py`: chequeos simples del laboratorio
- `tests/`: pruebas básicas
- `Dockerfile`: imagen endurecida de forma sencilla

## Configuración

1. Copia `.env.example` a `.env`
2. Cambia el valor de `API_TOKEN`

Ejemplo de variables:

- `APP_NAME=Lab Security`
- `APP_ENV=dev`
- `DEBUG=false`
- `API_TOKEN=un-valor-seguro`

## Qué demuestra este laboratorio

### 1) Gestión de secretos

Se usa `pydantic-settings` para cargar variables desde `.env`.

Punto importante:

- el secreto `API_TOKEN` no se deja como texto plano en la lógica
- se maneja como `SecretStr`

### 2) Auditoría de dependencias

Se agregaron herramientas de auditoría en `pyproject.toml`:

- `pip-audit`
- `safety`

Comandos sugeridos:

- `poetry install`
- `poetry run pip-audit`
- `poetry run safety scan`

Si aparece un hallazgo, la idea del laboratorio es:

1. identificar el paquete vulnerable
2. subir a una versión compatible siguiendo PEP 440
3. volver a ejecutar la auditoría

En este lab ya se dejaron versiones modernas y acotadas para mantener compatibilidad.

### 3) Compatibilidad y actualizaciones

Las dependencias usan rangos como:

- `>=0.128.0,<0.129.0`

Esto ayuda a:

- aceptar parches seguros
- evitar saltos mayores inesperados

### 4) Hardening del contenedor

El `Dockerfile` aplica lo básico:

- imagen slim
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`
- usuario `appuser` sin privilegios
- exclusión de `.env` en `.dockerignore`

## Endpoints

- `GET /` información general
- `GET /health` estado simple
- `GET /security` resumen del estado de seguridad del laboratorio

## Pruebas

Ejecuta:

- `poetry run pytest`

## Resultado esperado

Este laboratorio cumple con lo pedido de forma simple:

- integra `pydantic-settings`
- deja lista la auditoría con `pip-audit` y `safety`
- usa dependencias con versiones compatibles
- ejecuta Docker sin root y con permisos mínimos

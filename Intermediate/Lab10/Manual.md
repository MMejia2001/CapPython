# Manual de estudio - Lab10: Pruebas y TDD

## 1. Propósito del laboratorio
Este laboratorio se enfoca en diseñar código guiado por pruebas y construir una suite confiable usando herramientas modernas del ecosistema Python.

La práctica implementa lógica de pricing para órdenes y la valida con distintos tipos de pruebas:

- pruebas unitarias con `pytest`
- fixtures y parametrización
- mocking con `unittest.mock`
- property-based testing con `Hypothesis`
- soporte para cobertura con `pytest-cov`

El objetivo no es solo probar, sino demostrar una forma disciplinada de construir software con retroalimentación rápida.

---

## 2. ¿Qué hace el código?
El módulo `pricing.py` implementa reglas de negocio para calcular:

- subtotal
- costo de envío
- descuento por cupón
- impuesto
- total final de una orden

Además define:
- una entidad simple `Item`
- un contrato `TaxProvider` para desacoplar el cálculo del impuesto

Las pruebas validan estas reglas desde varios ángulos.

---

## 3. Archivos importantes
- `src/lab_tdd/pricing.py`: lógica de negocio.
- `tests/test_pricing_unit.py`: pruebas unitarias y con mocks.
- `tests/test_pricing_property.py`: pruebas basadas en propiedades con Hypothesis.
- `pytest.ini`: definición de markers.
- `pyproject.toml`: dependencias y herramientas de calidad.

---

## 4. Conceptos clave que debo entender

## 4.1 TDD
TDD significa **Test-Driven Development**.

La idea básica es trabajar en ciclos cortos:
1. escribir una prueba que falle
2. escribir el código mínimo para hacerla pasar
3. refactorizar manteniendo la prueba en verde

### Qué aporta
- diseño más claro
- menor sobreingeniería
- retroalimentación rápida
- mayor confianza al refactorizar

### Importante
Aunque el repositorio ya contiene el resultado final, el laboratorio representa una solución que encaja muy bien con ese enfoque.

---

## 4.2 `pytest`
`pytest` es el framework principal de pruebas usado aquí.

### Ventajas
- sintaxis simple
- asserts legibles
- fixtures integradas
- parametrización cómoda
- ecosistema amplio

---

## 4.3 Fixtures
En `test_pricing_unit.py` aparece:

```python
@pytest.fixture
def sample_items():
```

### Qué hace
Prepara un conjunto de datos reutilizable para varias pruebas.

### Ventaja
Evita duplicar setup y hace las pruebas más limpias.

---

## 4.4 Parametrización
Se usa `@pytest.mark.parametrize(...)` para probar múltiples casos con una sola función.

### Ejemplo
```python
@pytest.mark.parametrize(
    "sub,expected_shipping",
    [
        (0.0, 0.0),
        (10.0, 99.0),
        ...
    ],
)
```

### Qué aporta
Permite cubrir varias combinaciones de entrada/salida sin repetir código.

---

## 4.5 Markers
En `pytest.ini` se define:

```ini
[pytest]
markers =
    slow: pruebas más lentas (property-based / integración)
```

### Qué significa
Las pruebas marcadas como `slow` pueden filtrarse o ejecutarse por separado.

### En este laboratorio
Las pruebas con Hypothesis se marcan como lentas.

---

## 4.6 `unittest.mock`
En pruebas unitarias se usa:

```python
from unittest.mock import Mock
```

### Para qué sirve
Permite simular dependencias externas.

### En este laboratorio
Se mockea `tax_provider` para controlar la tasa de impuesto sin depender de una implementación real.

Ejemplo:
```python
tax_provider = Mock()
tax_provider.get_tax_rate.return_value = 0.16
```

### Ventaja
La prueba se enfoca en la lógica de `order_total`, no en cómo se obtiene la tasa.

---

## 4.7 Property-based testing con Hypothesis
En `test_pricing_property.py` se usa Hypothesis.

### Idea principal
En lugar de probar solo ejemplos fijos, se generan muchos datos automáticamente para verificar propiedades generales.

### Estrategia definida
```python
valid_items = st.lists(
    st.builds(
        Item,
        ...
    ),
    min_size=1,
    max_size=50,
)
```

### Qué genera
Listas válidas de `Item` con:
- `sku` no vacío
- `unit_price` no negativo
- `qty` mayor a 0

---

## 4.8 Propiedades verificadas
### `test_subtotal_is_never_negative`
Verifica que el subtotal nunca sea negativo para entradas válidas.

### `test_subtotal_equals_sum_of_lines`
Verifica que el subtotal sea igual a la suma de cada línea `unit_price * qty`.

### Por qué esto es poderoso
No valida solo casos concretos; valida reglas matemáticas generales.

---

## 4.9 Cobertura
El laboratorio incluye `pytest-cov` como dependencia de desarrollo.

### Qué permite
Medir qué porcentaje del código está cubierto por pruebas.

### Por qué es útil
Ayuda a detectar zonas no ejercitadas por la suite.

### Importante
Cobertura alta no garantiza calidad por sí sola, pero sí ofrece una señal útil.

---

## 4.10 Integración en CI
Aunque no hay pipeline CI explícito en esta carpeta, el laboratorio está preparado para integrarse fácilmente.

### Qué podrías decir en exposición
Los tests, la cobertura y los checks de calidad pueden ejecutarse automáticamente en CI para evitar regresiones en cada cambio.

---

## 4.11 Revisión del código de negocio
En `pricing.py` hay varias funciones clave.

### `subtotal(items)`
Calcula la suma de líneas.

Reglas:
- si no hay items, regresa `0.0`
- si `unit_price < 0`, lanza `ValueError`
- si `qty <= 0`, lanza `ValueError`

### `shipping_cost(subtotal_amount)`
Reglas:
- subtotal >= 1000 → envío gratis
- subtotal > 0 → envío 99
- subtotal == 0 → envío 0

### `discount_amount(subtotal_amount, coupon)`
Reglas:
- sin cupón → 0
- `SAVE10` → 10% con tope de 200
- `SAVE50` → 50 pesos si subtotal > 0
- cupón desconocido → 0

### `order_total(...)`
Calcula el desglose completo:
- subtotal
- shipping
- discount
- tax
- total
- tax_rate

---

## 4.12 `Protocol` para desacoplar dependencias
En `pricing.py` aparece:

```python
class TaxProvider(Protocol):
    def get_tax_rate(self, customer_country: str) -> float: ...
```

### Qué aporta
Define un contrato para la dependencia externa del impuesto.

### Ventaja
Hace el código más testeable y flexible.

---

## 4.13 Validaciones de negocio
El laboratorio también prueba errores esperados.

### Casos cubiertos
- precio negativo
- cantidad no positiva
- tasa de impuesto fuera de rango

### Idea importante
Una buena suite no solo valida el camino feliz, también valida entradas inválidas.

---

## 5. Explicación de las pruebas unitarias

## `test_subtotal_ok`
Verifica el cálculo básico del subtotal.

## `test_shipping_rules`
Valida reglas de envío con varios escenarios.

## `test_discount_amount`
Valida descuentos por cupón con parametrización.

## `test_order_total_uses_tax_provider_and_returns_breakdown`
Verifica:
- que se use el `tax_provider`
- que el desglose final sea correcto

## `test_subtotal_rejects_negative_price`
Asegura que un precio negativo lance error.

## `test_subtotal_rejects_non_positive_qty`
Asegura que una cantidad inválida lance error.

---

## 6. Explicación de las pruebas de propiedades

## Estrategia de generación
Hypothesis genera múltiples listas válidas de items.

## Propiedad 1
El subtotal nunca debe ser negativo.

## Propiedad 2
El subtotal debe coincidir con la suma de líneas.

### Qué valor tiene esto
Detecta errores sutiles que podrían no aparecer en pocos casos escritos a mano.

---

## 7. Cómo ejecutar el laboratorio
Dentro de `Intermediate/Lab10`:

### Instalar dependencias
```bash
poetry install
```

### Ejecutar pruebas
```bash
poetry run pytest
```

### Ejecutar solo pruebas lentas
```bash
poetry run pytest -m slow
```

### Excluir pruebas lentas
```bash
poetry run pytest -m "not slow"
```

### Ejecutar cobertura
```bash
poetry run pytest --cov=src/lab_tdd --cov-report=term-missing
```

### Generar reporte HTML de cobertura
```bash
poetry run pytest --cov=src/lab_tdd --cov-report=html
```

### Ejecutar herramientas de calidad
```bash
poetry run isort .
poetry run black .
poetry run ruff check . --fix
poetry run pre-commit run --all-files --config .pre-commit-config.yaml
```

---

## 8. Qué salida produce
### En pruebas
`pytest` mostrará pruebas aprobadas o fallidas.

### En cobertura
Se puede generar:
- reporte en terminal
- reporte HTML en `htmlcov/`

De hecho, esta carpeta ya contiene un reporte HTML generado.

---

## 9. Buenas prácticas aplicadas
- separar lógica pura y dependencias externas
- usar mocks para aislar pruebas
- parametrizar casos repetitivos
- usar property-based testing para reglas generales
- marcar pruebas lentas
- medir cobertura
- preparar la suite para CI

---

## 10. Posibles preguntas en la presentación

### ¿Qué diferencia hay entre prueba unitaria y property-based testing?
La prueba unitaria valida ejemplos concretos; la property-based valida propiedades generales sobre muchos datos generados automáticamente.

### ¿Para qué sirve un fixture?
Para reutilizar setup común entre pruebas.

### ¿Para qué sirve `Mock`?
Para simular dependencias y controlar su comportamiento en pruebas.

### ¿Por qué usar `Protocol` con `TaxProvider`?
Porque desacopla la lógica de negocio de una implementación concreta y facilita el mocking.

### ¿Qué significa que una prueba esté marcada como `slow`?
Que puede tardar más y conviene filtrarla en algunos escenarios.

### ¿Qué ventaja tiene `parametrize`?
Permite cubrir muchos casos con menos duplicación de código.

### ¿Cobertura alta significa ausencia de bugs?
No. Solo indica cuánto código fue ejecutado por pruebas, no garantiza corrección total.

### ¿Qué aporta Hypothesis que no aporta pytest normal?
Explora una gran variedad de entradas automáticamente y puede encontrar casos borde inesperados.

### ¿Por qué es importante probar errores esperados?
Porque valida robustez y comportamiento correcto ante entradas inválidas.

### ¿Cómo se relaciona esto con CI?
La suite puede ejecutarse automáticamente en cada cambio para evitar regresiones.

---

## 11. Qué podría mejorarse
Si te preguntan cómo evolucionarías este laboratorio, puedes responder:

- agregar más propiedades para `order_total`
- probar explícitamente `tax_rate` fuera de rango
- agregar pruebas de regresión para cupones futuros
- fijar thresholds mínimos de cobertura en CI
- separar pruebas unitarias, integración y propiedades por carpetas o markers más finos

---

## 12. Resumen ejecutivo
Este laboratorio aplica pruebas automatizadas como una herramienta de diseño. Implementa una lógica de pricing y la valida con pruebas unitarias, parametrización, fixtures, mocks y property-based testing con Hypothesis. Además, incorpora soporte para cobertura, dejando la suite lista para integrarse en CI y sostener un enfoque de TDD confiable.

---

## 13. Frase corta para exposición
> Este laboratorio demuestra que probar no es el paso final, sino parte del diseño: se valida la lógica con ejemplos concretos, propiedades generales y cobertura para construir una suite confiable.

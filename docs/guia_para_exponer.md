# Guía sencilla para explicar el proyecto

## ¿Qué hace el programa?

Registra el menú, clientes, pedidos y pagos de Sabor Valluno. Se usa desde un menú de consola que aparece al ejecutar `main.py`.

## ¿Para qué sirve cada archivo?

- `main.py`: muestra las opciones, pregunta datos y conecta las otras partes.
- `modelo/productos.py`: define productos. `Plato`, `Bebida` y `Combo` heredan de `Producto`. El combo contiene otros productos y calcula el descuento del 10 %.
- `modelo/clientes.py`: guarda nombre y teléfono, y valida el teléfono.
- `modelo/pedidos.py`: define pedidos `Local`, `ParaLlevar` y `Delivery`. Controla productos, cargos y estados.
- `modelo/pagos.py`: define pagos `Efectivo`, `QR` y `Tarjeta`; cada forma procesa el pago a su manera.
- `restaurante.py`: tiene funciones de apoyo. `main.py` las usa para filtrar el menú por día, buscar una opción, mostrar pedidos y calcular el reporte de ventas. No se ejecuta por separado.
- `pruebas.py`: contiene 16 comprobaciones automáticas con `assert`.

## ¿Qué es `restaurante.cpython-314.pyc`?

Es un archivo temporal que Python genera al ejecutar el programa para cargar módulos más rápido. No es código fuente: no lo abras ni lo edites. El archivo que corresponde revisar es `restaurante.py`. La carpeta `__pycache__` puede quedarse; está excluida de Git por `.gitignore`.

## Demostración básica

1. Ejecuta `python main.py`.
2. Elige `1` y registra dos productos, por ejemplo un plato y una bebida.
3. Elige `2` si quieres mostrar cómo se arma un combo.
4. Elige `4` y registra un cliente.
5. Elige `5`, crea un pedido y sigue las preguntas.
6. Elige `10` para cobrarlo; luego usa `8` para avanzar su estado y `11` para el reporte.

Los datos se guardan en memoria mientras el programa está abierto. Si eliges `0` y lo vuelves a ejecutar, vuelve a empezar sin productos ni clientes.

## Respuestas cortas para la defensa

- **¿Por qué hay varios archivos?** Para separar productos, clientes, pedidos, pagos y la interacción con la persona.
- **¿Qué significa heredar?** Una clase hija reutiliza atributos y métodos de una clase base, y puede definir su propia versión de un método.
- **¿Qué es el polimorfismo aquí?** El pedido llama a `calcular_precio()` o `calcular_cargos()` sin necesitar saber los detalles internos de cada clase.
- **¿Cómo funciona un combo?** Recorre sus productos, suma sus precios y aplica el 10 %. Como cada producto sabe contar sus platos, también cuenta los platos dentro de combos anidados.
- **¿Qué hace `restaurante.py`?** Son funciones auxiliares que importa `main.py`; no es el archivo que inicia la aplicación.

Practica las respuestas con tus palabras y verifica cada explicación mirando el código. No memorices algo que todavía no entiendes.

# Sistema de pedidos Sabor Valluno

Proyecto de Programación Orientada a Objetos para gestionar el menú, clientes, pedidos y pagos del restaurante ficticio Sabor Valluno.

## Variante

Este proyecto aplica la Variante A:

- Combos con 10 % de descuento.
- Para llevar cobra Bs 2 por cada plato, también cuando el plato está dentro de un combo.
- El envío cuesta Bs 8 en Cercado, Bs 15 en Quillacollo, Bs 15 en Sacaba y Bs 20 en Vinto.
- El envío es gratis desde Bs 150 únicamente en Cercado.
- El pedido mínimo de delivery es Bs 40.
- El chicharrón solo está disponible los domingos.
- Efectivo calcula el cambio; QR valida un código de 10 dígitos; tarjeta agrega 3 % y no se acepta en delivery.

## Archivos

- `modelo/productos.py`: Producto, Plato, Bebida y Combo.
- `modelo/clientes.py`: Cliente y teléfono.
- `modelo/pedidos.py`: Pedido, Local, ParaLlevar y Delivery.
- `modelo/pagos.py`: MetodoPago, Efectivo, QR y Tarjeta.
- `restaurante.py`: funciones para mostrar detalles, menús y reportes.
- `main.py`: menú de consola.
- `pruebas.py`: 16 casos de prueba con assert; ejecutados el 24/11/2026, los 16 terminaron correctamente.
- `docs/diagrama_v1.png`: foto del diagrama firmado y aprobado.
- `docs/diagrama_v2.png`: reconstrucción legible de clases, relaciones y reglas de Variante A; indica los cambios respecto a v1.
- `docs/bitacora_ia.md`: registro de asistencia de IA.
- `docs/registro_ia_Suyo_Jaita.md`: registro personal de Cristopher Jesus Suyo Jaita; falta completar la semana y firmarlo.
- `docs/acta_consultas.md`: preguntas de reglas para el docente.
- `docs/guia_para_exponer.md`: explicación sencilla de los módulos y una demostración paso a paso.

## Ejecutar

Desde una terminal abierta en esta carpeta:

```text
python main.py
```

Si el menú te confunde, elige la opción `12. Ayuda: cómo empezar`. La opción `2` arma combos y requiere registrar primero dos productos con la opción `1`.

Para ejecutar los casos de prueba cuando estés listo:

```text
python pruebas.py
```

El código se generó con ayuda de IA. Revísalo y asegúrate de poder explicar cada clase antes de entregarlo. Última comprobación: `python pruebas.py` completó los 16 casos el 24/11/2026.

## Pendiente de consulta

## Revisión frente al documento del proyecto

Al comparar el sistema con el documento original, encontré estos puntos para cerrar o confirmar:

- La regla oficial indica que hay retraso cuando el delivery tarda más de 60 minutos y que se devuelve el costo del envío. El programa todavía no aplica esa regla automáticamente al entregar el pedido.
- Guardar y cargar datos en JSON es opcional; por ahora el sistema trabaja en memoria y los datos se borran al salir.
- El documento menciona una clase gestora `Restaurante`. En este proyecto, `restaurante.py` contiene funciones de apoyo. El ingeniero indicó que Restaurante no debía agregarse como clase relacionada en el diagrama, así que no se cambia el diagrama sin consultarle esa diferencia.
- El documento espera al menos cuatro commits en las fases 2 y 3. El historial actual no demuestra esa distribución semanal; no se deben crear commits con fechas falsas. Hay que consultar al docente cómo registrar el trabajo ya realizado.

El acta conserva la pregunta sobre retraso como pendiente de confirmación directa con el docente; no se presenta una consulta como realizada si no ocurrió.

## Antes de entregar

- Completa la semana y firma tu registro personal de IA cuando ya hayas revisado el código.
- Consulta al docente la regla de retraso y registra la respuesta en el acta.
- Revisa el diagrama v2 con el ingeniero, especialmente las relaciones y sus multiplicidades.
- Si haces más cambios al código, vuelve a ejecutar `python pruebas.py` y confirma que los 16 casos pasan.
- Explica con tus palabras las clases y reglas del programa para la defensa individual.

## Git y entrega

Repositorio público: https://github.com/jaitasuyocristophersimon-alt/sabor-valluno-variante-a

Los commits son puntos de guardado con un mensaje que resume un cambio. El primer commit registra el estado actual del proyecto; no reconstruye ni inventa el historial de semanas anteriores. Desde ahora, guarda cambios reales en commits pequeños mientras estudias y corriges el código. Consulta al ingeniero cómo proceder con el requisito de commits de semanas pasadas.

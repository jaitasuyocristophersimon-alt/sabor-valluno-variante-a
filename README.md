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
- `pruebas.py`: 18 casos de prueba con assert. Revisa reglas de Variante A, pagos, pedidos y retraso en delivery.
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

El código se generó con ayuda de IA. Revísalo y asegúrate de poder explicar cada clase antes de entregarlo. Última comprobación: `python pruebas.py` completó los 18 casos el 24/11/2026.

## Revisión frente al documento del proyecto

Al comparar el sistema con el documento original, estos son los resultados:

- **Retraso en delivery:** si se entrega después de 60 minutos, el pedido devuelve el costo del envío. Se aplica automáticamente al pasar a ENTREGADO y tiene dos pruebas.
- Guardar y cargar datos en JSON es opcional; por ahora el sistema trabaja en memoria y los datos se borran al salir.
- El documento menciona una clase gestora `Restaurante`. En este proyecto, `restaurante.py` contiene funciones de apoyo. El ingeniero indicó que Restaurante no debía agregarse como clase relacionada en el diagrama, así que no se cambia el diagrama sin consultarle esa diferencia.
- El documento espera al menos cuatro commits en las fases 2 y 3. El historial actual no demuestra esa distribución semanal; no se deben crear commits con fechas falsas. Hay que consultar al docente cómo registrar el trabajo ya realizado.

El acta conserva la pregunta sobre retraso pendiente de confirmación directa; el código usa la regla que figura en el documento original.

## Antes de entregar

- Completa la semana y firma tu registro personal de IA cuando ya hayas revisado el código.
- Consulta al docente la regla de retraso y registra la respuesta en el acta.
- Revisa el diagrama v2 con el ingeniero, especialmente las relaciones y sus multiplicidades.
- Si haces más cambios al código, vuelve a ejecutar `python pruebas.py` y confirma que los 16 casos pasan.
- Explica con tus palabras las clases y reglas del programa para la defensa individual.

## Git y entrega

Repositorio público: https://github.com/jaitasuyocristophersimon-alt/sabor-valluno-variante-a

Los commits son puntos de guardado con un mensaje que resume un cambio. El historial registra trabajo hecho desde ahora; no se reconstruyen ni inventan commits de semanas anteriores. Consulta al ingeniero cómo proceder con la distribución semanal que pide el documento.

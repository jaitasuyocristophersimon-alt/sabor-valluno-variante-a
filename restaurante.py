"""Funciones de apoyo que usa main.py para mostrar y consultar datos.

Este archivo no inicia el programa ni contiene el menú de consola. main.py
llama a estas funciones cuando necesita filtrar productos, buscar una opción,
mostrar un pedido o resumir ventas.
"""

from datetime import date
from decimal import Decimal


def listar_menu(productos, dia):
    """Devuelve solo los productos disponibles en el día indicado."""
    return [producto for producto in productos if producto.esta_disponible(dia)]


def buscar_por_numero(lista, numero):
    """Convierte un número que eligió la persona en un elemento de la lista."""
    if numero < 1 or numero > len(lista):
        raise ValueError("Número fuera de la lista.")
    return lista[numero - 1]


def detalle_pedido(pedido):
    """Prepara un texto claro con productos, cargos, comisión y total."""
    detalle = pedido.detalle()
    lineas = [
        "Pedido " + detalle["tipo"] + " — " + detalle["estado"],
        "Cliente: " + detalle["cliente"],
        "Productos:"
    ]
    if not detalle["items"]:
        lineas.append("  (sin productos)")
    for item in detalle["items"]:
        lineas.append("  " + str(item["cantidad"]) + " x " + item["producto"] +
                      " — Bs " + format(item["importe"], ".2f"))
    lineas.append("Subtotal (descuentos de combo ya aplicados): Bs " + format(detalle["subtotal"], ".2f"))
    lineas.append("Descuentos de combos incluidos: Bs " + format(detalle["descuentos"], ".2f"))
    for nombre_cargo, monto_cargo in detalle["cargos_detalle"].items():
        lineas.append(nombre_cargo + ": Bs " + format(monto_cargo, ".2f"))
    if detalle["comision_pago"] > 0:
        lineas.append("Comisión de tarjeta: Bs " + format(detalle["comision_pago"], ".2f"))
    lineas.extend([
        "Cargos totales: Bs " + format(detalle["cargos"], ".2f"),
        "Total: Bs " + format(detalle["total"], ".2f"),
        "Pagado: " + ("Sí" if detalle["pagado"] else "No")
    ])
    return "\n".join(lineas)


def reporte_ventas(pedidos, dia=None):
    """Suma las ventas pagadas y entregadas del día, separadas por pedido."""
    if dia is None:
        dia = date.today()
    pedidos_del_dia = [pedido for pedido in pedidos
                       if pedido.fecha_registro.date() == dia
                       and pedido.estado == "ENTREGADO" and pedido.pagado]
    por_tipo = {"Local": Decimal("0.00"), "ParaLlevar": Decimal("0.00"), "Delivery": Decimal("0.00")}
    mas_vendidos = {}
    total = Decimal("0.00")
    for pedido in pedidos_del_dia:
        importe = pedido.calcular_total()
        por_tipo[pedido.tipo_pedido] += importe
        total += importe
        for producto, cantidad in pedido.items:
            mas_vendidos[producto.nombre] = mas_vendidos.get(producto.nombre, 0) + cantidad
    principales = sorted(mas_vendidos.items(), key=lambda elemento: elemento[1], reverse=True)[:3]
    lineas = ["Reporte de ventas — " + dia.strftime("%d/%m/%Y")]
    for tipo, monto in por_tipo.items():
        lineas.append(tipo + ": Bs " + format(monto, ".2f"))
    lineas.append("Total vendido: Bs " + format(total, ".2f"))
    lineas.append("Tres productos más vendidos:")
    if principales:
        for nombre, cantidad in principales:
            lineas.append("  " + nombre + ": " + str(cantidad))
    else:
        lineas.append("  Todavía no hay ventas entregadas y pagadas.")
    return "\n".join(lineas)

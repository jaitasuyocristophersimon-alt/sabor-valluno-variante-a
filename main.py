from datetime import datetime
from modelo.clientes import Cliente
from modelo.productos import Plato, Bebida, Combo, redondear_monto
from modelo.pedidos import Local, ParaLlevar, Delivery
from modelo.pagos import Efectivo, QR, Tarjeta
from restaurante import listar_menu, buscar_por_numero, detalle_pedido, reporte_ventas

productos = []
clientes = []
pedidos = []
DIAS_SEMANA = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")


def leer_entero(mensaje):
    return int(input(mensaje).strip())


def mostrar_productos(lista=None):
    lista = productos if lista is None else lista
    if not lista:
        print("Todavía no registraste productos.")
        return
    for numero, producto in enumerate(lista, start=1):
        try:
            precio = producto.calcular_precio()
            precio_texto = "Bs " + format(precio, ".2f")
        except ValueError:
            precio_texto = "incompleto: faltan productos"
        print(str(numero) + ". " + producto.nombre + " — " + precio_texto)


def agregar_producto():
    print("1. Plato\n2. Bebida")
    opcion = leer_entero("Tipo: ")
    nombre = input("Nombre: ").strip()
    precio = redondear_monto(input("Precio: Bs ").strip())
    if opcion == 1:
        dias_texto = input("Días disponibles separados por coma (Enter = todos; chicharrón solo domingo): ").strip()
        dias = [dia.strip() for dia in dias_texto.split(",") if dia.strip()] if dias_texto else None
        producto = Plato(nombre, precio, dias)
    elif opcion == 2:
        tipo = input("Tipo de bebida (por ejemplo, natural o gaseosa): ").strip()
        presentacion = input("Presentación (vaso o jarra): ").strip().lower()
        producto = Bebida(nombre, precio, tipo, presentacion)
    else:
        raise ValueError("Elige 1 o 2.")
    productos.append(producto)
    print("Producto agregado.")


def armar_combo():
    if len(productos) < 2:
        print("Todavía no puedes armar un combo.")
        print("Primero elige 1 y registra por lo menos dos platos o bebidas.")
        print("Después vuelve a elegir 2 para crear el combo con descuento del 10 %.")
        return
    nombre = input("Nombre del combo: ").strip()
    combo = Combo(nombre, nombre, descuento="0.10")
    print("Elige los productos del combo. Escribe 0 cuando termines.")
    while True:
        mostrar_productos()
        print("Escribe 0 cuando hayas terminado de elegir.")
        numero = leer_entero("Número del producto que irá dentro del combo: ")
        if numero == 0:
            break
        combo.agregar_producto(buscar_por_numero(productos, numero))
    precio = combo.calcular_precio()
    productos.append(combo)
    print("Combo agregado. Precio con 10 % de descuento: Bs " + format(precio, ".2f"))


def registrar_cliente():
    nombre = input("Nombre del cliente: ").strip()
    telefono = input("Teléfono (8 dígitos, empieza con 6 o 7): ").strip()
    clientes.append(Cliente(nombre, telefono))
    print("Cliente registrado.")


def seleccionar_cliente():
    if not clientes:
        raise ValueError("Primero registra un cliente.")
    for numero, cliente in enumerate(clientes, start=1):
        print(str(numero) + ". " + cliente.nombre + " — " + cliente.telefono)
    return buscar_por_numero(clientes, leer_entero("Cliente: "))


def crear_pedido():
    if not productos:
        print("Primero registra productos con la opción 1; después podrás crear un pedido.")
        return
    if not clientes:
        print("Primero registra un cliente con la opción 4; después podrás crear un pedido.")
        return
    cliente = seleccionar_cliente()
    print("1. Local\n2. Para llevar\n3. Delivery")
    tipo = leer_entero("Tipo de pedido: ")
    mesa = None
    if tipo == 1:
        pedido = Local(cliente)
        mesa = leer_entero("Mesa (1 a 15): ")
    elif tipo == 2:
        pedido = ParaLlevar(cliente)
    elif tipo == 3:
        zona = input("Zona (Cercado, Quillacollo, Sacaba o Vinto): ").strip()
        pedido = Delivery(cliente, zona)
    else:
        raise ValueError("Elige 1, 2 o 3.")

    dia_hoy = DIAS_SEMANA[datetime.now().weekday()]
    while True:
        mostrar_productos()
        print("Escribe 0 cuando termines de agregar productos.")
        numero = leer_entero("Producto: ")
        if numero == 0:
            break
        producto = buscar_por_numero(productos, numero)
        if not producto.esta_disponible(dia_hoy):
            raise ValueError(producto.nombre + " no está disponible hoy (" + dia_hoy + ").")
        cantidad = leer_entero("Cantidad (1 a 20): ")
        pedido.agregar_producto(producto, cantidad)

    if not pedido.items:
        raise ValueError("El pedido debe tener por lo menos un producto.")
    pedido.calcular_total()
    if mesa is not None:
        pedido.asignar_mesa(mesa)
    pedidos.append(pedido)
    print("Pedido registrado.")
    print(detalle_pedido(pedido))
    elegir_pago(pedido)


def elegir_pago(pedido):
    print("1. Efectivo\n2. QR\n3. Tarjeta")
    opcion = leer_entero("Método de pago: ")
    if opcion == 1:
        recibido = redondear_monto(input("Monto recibido: Bs ").strip())
        metodo = Efectivo(recibido)
    elif opcion == 2:
        recibido = redondear_monto(input("Monto recibido por QR: Bs ").strip())
        codigo = input("Código de transacción (10 dígitos): ").strip()
        metodo = QR(recibido, codigo)
    elif opcion == 3:
        metodo = Tarjeta()
    else:
        raise ValueError("Elige 1, 2 o 3.")
    pedido.metodo_pago = metodo
    print("Total a pagar: Bs " + format(pedido.calcular_total(), ".2f"))


def quitar_producto_pedido():
    pedidos_abiertos = [pedido for pedido in pedidos if pedido.estado == "REGISTRADO"]
    if not pedidos_abiertos:
        print("No hay pedidos REGISTRADOS.")
        return
    for numero, pedido in enumerate(pedidos_abiertos, start=1):
        print(str(numero) + ". " + pedido.tipo_pedido + " — " + pedido.cliente.nombre)
    pedido = buscar_por_numero(pedidos_abiertos, leer_entero("Pedido: "))
    if not pedido.items:
        print("El pedido todavía no tiene productos.")
        return
    for numero, (producto, cantidad) in enumerate(pedido.items, start=1):
        print(str(numero) + ". " + producto.nombre + " — cantidad: " + str(cantidad))
    numero_producto = leer_entero("Producto que quieres quitar: ")
    producto, cantidad_actual = pedido.items[numero_producto - 1]
    cantidad = leer_entero("Cantidad a quitar (1 a " + str(cantidad_actual) + "): ")
    pedido.quitar_producto(producto, cantidad)
    print("Producto quitado del pedido.")


def ver_detalle():
    if not pedidos:
        print("Todavía no hay pedidos.")
        return
    for numero, pedido in enumerate(pedidos, start=1):
        print(str(numero) + ". " + pedido.tipo_pedido + " — " + pedido.estado)
    pedido = buscar_por_numero(pedidos, leer_entero("Pedido: "))
    print(detalle_pedido(pedido))


def cambiar_estado():
    if not pedidos:
        print("Todavía no hay pedidos.")
        return
    for numero, pedido in enumerate(pedidos, start=1):
        print(str(numero) + ". " + pedido.tipo_pedido + " — " + pedido.estado)
    pedido = buscar_por_numero(pedidos, leer_entero("Pedido: "))
    if pedido.estado == "REGISTRADO":
        print("1. EN_PREPARACION\n2. CANCELAR")
        opcion = leer_entero("Acción: ")
        pedido.cambiar_estado("EN_PREPARACION" if opcion == 1 else "CANCELADO" if opcion == 2 else "INVALIDO")
    elif pedido.estado == "EN_PREPARACION":
        pedido.cambiar_estado("LISTO")
    elif pedido.estado == "LISTO":
        pedido.cambiar_estado("ENTREGADO")
    else:
        raise ValueError("Este pedido ya está cerrado.")
    print("Estado actualizado: " + pedido.estado)
    if pedido.tipo_pedido == "Delivery" and pedido.estado == "ENTREGADO":
        print("La compensación por retraso queda pendiente de la regla que confirme el ingeniero.")


def cambiar_metodo_pago():
    pendientes = [pedido for pedido in pedidos if not pedido.pagado and pedido.estado != "CANCELADO"]
    if not pendientes:
        print("No hay pedidos que necesiten método de pago.")
        return
    for numero, pedido in enumerate(pendientes, start=1):
        print(str(numero) + ". " + pedido.tipo_pedido + " — " + pedido.cliente.nombre)
    pedido = buscar_por_numero(pendientes, leer_entero("Pedido: "))
    elegir_pago(pedido)


def cobrar_pedido():
    no_pagados = [pedido for pedido in pedidos if not pedido.pagado and pedido.estado != "CANCELADO"]
    if not no_pagados:
        print("No hay pedidos pendientes de pago.")
        return
    for numero, pedido in enumerate(no_pagados, start=1):
        print(str(numero) + ". " + pedido.tipo_pedido + " — Bs " + format(pedido.calcular_total(), ".2f"))
    pedido = buscar_por_numero(no_pagados, leer_entero("Pedido: "))
    comprobante = pedido.cobrar()
    print("Comprobante:")
    for campo, valor in comprobante.items():
        print("  " + campo + ": " + str(valor))


def mostrar_menu_del_dia():
    dia = input("Día de la semana: ").strip()
    menu = listar_menu(productos, dia)
    print("Menú disponible:")
    mostrar_productos(menu)


def mostrar_ayuda():
    print("\n=== GUÍA RÁPIDA ===")
    print("1. Registra al menos dos platos o bebidas.")
    print("2. (Opcional) Arma un combo; se aplica automáticamente 10 % de descuento.")
    print("3. Registra un cliente con teléfono de 8 dígitos que empiece en 6 o 7.")
    print("4. Registra un pedido: local, para llevar o delivery; agrega productos y elige el pago.")
    print("5. Cobra el pedido con la opción 10.")
    print("6. Cambia el estado con la opción 8: EN_PREPARACION, LISTO y ENTREGADO.")
    print("7. Revisa las ventas del día con la opción 11.")
    print("\nSi eliges 2 sin registrar productos, el programa te indicará qué hacer.")
    print("Los datos se guardan solo mientras el programa está abierto; al salir se borran.")
    print("Para volver al menú, presiona Enter.")
    input()


def menu_principal():
    while True:
        print("\n=== SABOR VALLUNO — VARIANTE A ===")
        print("¿Primera vez? Registra productos (1), luego cliente (4) y pedido (5).")
        print("1. Registrar plato o bebida")
        print("2. Armar combo")
        print("3. Ver menú disponible para un día")
        print("4. Registrar cliente")
        print("5. Registrar pedido")
        print("6. Quitar producto de un pedido registrado")
        print("7. Ver detalle de pedido")
        print("8. Cambiar estado de pedido")
        print("9. Elegir o cambiar método de pago")
        print("10. Cobrar pedido y mostrar comprobante")
        print("11. Reporte de ventas de hoy")
        print("12. Ayuda: cómo empezar")
        print("0. Salir")
        try:
            opcion = leer_entero("Opción: ")
            if opcion == 0:
                print("Hasta luego.")
                break
            if opcion == 1:
                agregar_producto()
            elif opcion == 2:
                armar_combo()
            elif opcion == 3:
                mostrar_menu_del_dia()
            elif opcion == 4:
                registrar_cliente()
            elif opcion == 5:
                crear_pedido()
            elif opcion == 6:
                quitar_producto_pedido()
            elif opcion == 7:
                ver_detalle()
            elif opcion == 8:
                cambiar_estado()
            elif opcion == 9:
                cambiar_metodo_pago()
            elif opcion == 10:
                cobrar_pedido()
            elif opcion == 11:
                print(reporte_ventas(pedidos))
            elif opcion == 12:
                mostrar_ayuda()
            else:
                print("Opción no válida.")
        except (ValueError, TypeError, IndexError) as error:
            print("No se pudo completar la operación: " + str(error))


if __name__ == "__main__":
    menu_principal()

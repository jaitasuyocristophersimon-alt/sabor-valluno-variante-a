from decimal import Decimal

from modelo.clientes import Cliente
from modelo.productos import Plato, Bebida, Combo
from modelo.pedidos import Delivery, Local, ParaLlevar
from modelo.pagos import Efectivo, QR, Tarjeta


def probar_validacion_precio():
    try:
        Plato("Silpancho", 0)
        assert False, "El precio cero debió rechazarse."
    except ValueError:
        assert True


def probar_chicharron_solo_domingo():
    plato = Plato("Chicharrón", 25)
    assert plato.esta_disponible("domingo")
    assert not plato.esta_disponible("lunes")


def probar_jarra_tres_veces_vaso():
    bebida = Bebida("Mocochinchi", 6, "natural", "jarra")
    assert bebida.calcular_precio() == Decimal("18.00")


def probar_combo_con_descuento_variante_a():
    plato = Plato("Silpancho", 35)
    bebida = Bebida("Mocochinchi", 6, "natural")
    combo = Combo("Combo Valluno", productos=[plato, bebida])
    assert combo.calcular_precio() == Decimal("36.90")


def probar_combo_dentro_de_otro_combo():
    plato = Plato("Silpancho", 35)
    bebida = Bebida("Mocochinchi", 6, "natural")
    combo_interno = Combo("Combo pequeño", productos=[plato, bebida])
    bebida_extra = Bebida("Gaseosa", 5, "gaseosa")
    combo_externo = Combo("Combo grande", productos=[combo_interno, bebida_extra])
    assert combo_externo.calcular_precio() == Decimal("37.71")


def probar_delivery_caso_de_referencia():
    cliente = Cliente("Ana", "71234567")
    combo = Combo("Combo Valluno", productos=[Plato("Silpancho", 35), Bebida("Mocochinchi", 6, "natural")])
    pedido = Delivery(cliente, "Quillacollo")
    pedido.agregar_producto(combo, 2)
    assert pedido.calcular_subtotal() == Decimal("73.80")
    assert pedido.calcular_total() == Decimal("88.80")


def probar_envase_cuenta_platos_dentro_de_combo():
    cliente = Cliente("Luis", "61234567")
    combo = Combo("Combo", productos=[Plato("Pique macho", 40), Bebida("Refresco", 5, "natural")])
    pedido = ParaLlevar(cliente)
    pedido.agregar_producto(combo, 2)
    assert pedido.calcular_envase() == Decimal("4.00")
    assert pedido.calcular_total() == Decimal("4.00") + combo.calcular_precio() * 2


def probar_envio_gratis_solo_cercado():
    cliente = Cliente("Mara", "71234567")
    producto = Plato("Silpancho", 50)
    cercado = Delivery(cliente, "Cercado")
    cercado.agregar_producto(producto, 3)
    quillacollo = Delivery(cliente, "Quillacollo")
    quillacollo.agregar_producto(producto, 3)
    assert cercado.calcular_envio() == Decimal("0.00")
    assert quillacollo.calcular_envio() == Decimal("15.00")


def probar_pedido_minimo_delivery():
    pedido = Delivery(Cliente("Nora", "61234567"), "Sacaba")
    pedido.agregar_producto(Plato("Sopa", 39), 1)
    try:
        pedido.calcular_total()
        assert False, "El pedido menor a Bs 40 debió rechazarse."
    except ValueError:
        assert True


def probar_cambio_de_estado_invalido():
    pedido = Local(Cliente("Paz", "71234567"), mesa=15)
    try:
        pedido.cambiar_estado("ENTREGADO")
        assert False, "No se debe pasar directamente de REGISTRADO a ENTREGADO."
    except ValueError:
        assert pedido.estado == "REGISTRADO"
    pedido.cancelar_pedido()


def probar_telefono_invalido():
    try:
        Cliente("Rene", "51234567")
        assert False, "El teléfono que empieza con 5 debió rechazarse."
    except ValueError:
        assert True


def probar_cambio_efectivo():
    pago = Efectivo(100)
    comprobante = pago.procesar_pago(76.50)
    assert comprobante["cambio"] == Decimal("23.50")


def probar_codigo_qr_de_diez_digitos():
    pago = QR(50, "1234567890")
    assert pago.validar_codigo()
    assert pago.procesar_pago(50)["metodo"] == "QR"


def probar_comision_tarjeta():
    pago = Tarjeta()
    total = pago.calcular_total(100)
    assert pago.calcular_comision(100) == Decimal("3.00")
    assert total == Decimal("103.00")


def probar_tarjeta_no_se_acepta_en_delivery():
    pedido = Delivery(Cliente("Sol", "61234567"), "Vinto")
    try:
        pedido.metodo_pago = Tarjeta()
        assert False, "Delivery no debe aceptar tarjeta."
    except ValueError:
        assert pedido.metodo_pago is None


def probar_mesa_no_se_repite_en_pedidos_abiertos():
    cliente = Cliente("Eva", "71234567")
    primero = Local(cliente, mesa=14)
    try:
        Local(cliente, mesa=14)
        assert False, "La mesa ocupada debió rechazarse."
    except ValueError:
        assert primero.mesa == 14
    primero.cancelar_pedido()


def ejecutar_pruebas():
    pruebas = [
        probar_validacion_precio,
        probar_chicharron_solo_domingo,
        probar_jarra_tres_veces_vaso,
        probar_combo_con_descuento_variante_a,
        probar_combo_dentro_de_otro_combo,
        probar_delivery_caso_de_referencia,
        probar_envase_cuenta_platos_dentro_de_combo,
        probar_envio_gratis_solo_cercado,
        probar_pedido_minimo_delivery,
        probar_cambio_de_estado_invalido,
        probar_telefono_invalido,
        probar_cambio_efectivo,
        probar_codigo_qr_de_diez_digitos,
        probar_comision_tarjeta,
        probar_tarjeta_no_se_acepta_en_delivery,
        probar_mesa_no_se_repite_en_pedidos_abiertos
    ]
    for prueba in pruebas:
        prueba()
    print(str(len(pruebas)) + " casos de prueba completados.")


if __name__ == "__main__":
    ejecutar_pruebas()

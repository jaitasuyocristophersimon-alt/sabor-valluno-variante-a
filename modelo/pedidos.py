from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import unicodedata


def dinero(valor):
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def normalizar_zona(zona):
    texto = unicodedata.normalize("NFD", str(zona).strip().lower())
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")


class Pedido(ABC):
    TRANSICIONES = {
        "REGISTRADO": ("EN_PREPARACION", "CANCELADO"),
        "EN_PREPARACION": ("LISTO",),
        "LISTO": ("ENTREGADO",),
        "ENTREGADO": (),
        "CANCELADO": ()
    }

    def __init__(self, tipo_pedido, cliente, metodo_pago=None):
        self._tipo_pedido = tipo_pedido
        self._estado = "REGISTRADO"
        self._cliente = cliente
        self._metodo_pago = None
        self._items = []
        self._fecha_registro = datetime.now()
        self._pagado = False
        if metodo_pago is not None:
            self.metodo_pago = metodo_pago
        if cliente is not None:
            cliente.realizar_pedido(self)

    @property
    def tipo_pedido(self):
        return self._tipo_pedido

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def metodo_pago(self):
        return self._metodo_pago

    @metodo_pago.setter
    def metodo_pago(self, valor):
        if self._pagado:
            raise ValueError("El pedido ya fue pagado.")
        if valor is not None:
            self._validar_metodo_pago(valor)
        self._metodo_pago = valor

    @property
    def items(self):
        return tuple((producto, cantidad) for producto, cantidad in self._items)

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @property
    def pagado(self):
        return self._pagado

    def _validar_metodo_pago(self, metodo_pago):
        pass

    def agregar_producto(self, producto, cantidad=1):
        if self.estado != "REGISTRADO":
            raise ValueError("Solo se agregan productos cuando el pedido está REGISTRADO.")
        if cantidad < 1 or cantidad > 20:
            raise ValueError("La cantidad de un producto debe estar entre 1 y 20.")
        producto.calcular_precio()
        self._items.append([producto, cantidad])

    def quitar_producto(self, producto, cantidad=1):
        if self.estado != "REGISTRADO":
            raise ValueError("Solo se quitan productos cuando el pedido está REGISTRADO.")
        if cantidad < 1 or cantidad > 20:
            raise ValueError("La cantidad debe estar entre 1 y 20.")
        for item in self._items:
            if item[0] is producto:
                if cantidad >= item[1]:
                    self._items.remove(item)
                else:
                    item[1] -= cantidad
                return
        raise ValueError("Ese producto no está en el pedido.")

    def calcular_subtotal(self):
        subtotal = sum((producto.calcular_precio() * cantidad for producto, cantidad in self._items), Decimal("0.00"))
        return dinero(subtotal)

    @abstractmethod
    def calcular_cargos(self):
        pass

    def calcular_descuentos(self):
        ahorro = sum((producto.calcular_descuento() * cantidad for producto, cantidad in self._items), Decimal("0.00"))
        return dinero(ahorro)

    def detalle_cargos(self):
        return {"Cargos": self.calcular_cargos()}

    def calcular_total(self):
        total_base = dinero(self.calcular_subtotal() + self.calcular_cargos())
        if self.metodo_pago is not None:
            return self.metodo_pago.calcular_total(total_base)
        return total_base

    def cambiar_estado(self, nuevo_estado):
        nuevo_estado = str(nuevo_estado).strip().upper()
        estados_permitidos = self.TRANSICIONES.get(self.estado, ())
        if nuevo_estado not in estados_permitidos:
            raise ValueError("Cambio de estado inválido: " + self.estado + " a " + nuevo_estado)
        self._estado = nuevo_estado
        self._al_cambiar_estado(nuevo_estado)

    def _al_cambiar_estado(self, nuevo_estado):
        pass

    def cancelar_pedido(self):
        self.cambiar_estado("CANCELADO")

    def detalle(self):
        lineas = []
        for producto, cantidad in self.items:
            precio_unitario = producto.calcular_precio()
            lineas.append({
                "producto": producto.nombre,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "importe": dinero(precio_unitario * cantidad)
            })
        subtotal = self.calcular_subtotal()
        cargos = self.calcular_cargos()
        total_antes_pago = dinero(subtotal + cargos)
        comision_pago = Decimal("0.00")
        if self.metodo_pago is not None:
            comision_pago = self.metodo_pago.calcular_comision(total_antes_pago)
        return {
            "tipo": self.tipo_pedido,
            "estado": self.estado,
            "cliente": self.cliente.nombre if self.cliente else "Sin cliente",
            "items": lineas,
            "subtotal": subtotal,
            "descuentos": self.calcular_descuentos(),
            "comision_pago": comision_pago,
            "cargos": cargos,
            "cargos_detalle": self.detalle_cargos(),
            "total": self.calcular_total(),
            "pagado": self.pagado
        }

    def cobrar(self):
        if self.estado == "CANCELADO":
            raise ValueError("No se puede cobrar un pedido cancelado.")
        if self.pagado:
            raise ValueError("El pedido ya fue cobrado.")
        if self.metodo_pago is None:
            raise ValueError("Primero elige un método de pago.")
        total = self.calcular_total()
        comprobante = self.metodo_pago.procesar_pago(total)
        self._pagado = True
        return comprobante


class Local(Pedido):
    _mesas_ocupadas = {}

    def __init__(self, cliente, mesa=None, metodo_pago=None):
        self._mesa = None
        super().__init__("Local", cliente, metodo_pago)
        if mesa is not None:
            self.asignar_mesa(mesa)

    @property
    def mesa(self):
        return self._mesa

    def asignar_mesa(self, mesa):
        mesa = int(mesa)
        if mesa < 1 or mesa > 15:
            raise ValueError("La mesa debe estar entre 1 y 15.")
        ocupante = self._mesas_ocupadas.get(mesa)
        if ocupante is not None and ocupante is not self:
            raise ValueError("Esa mesa ya tiene un pedido abierto.")
        if self._mesa is not None and self._mesa != mesa:
            self._liberar_mesa()
        self._mesa = mesa
        self._mesas_ocupadas[mesa] = self

    def _liberar_mesa(self):
        if self._mesa is not None and self._mesas_ocupadas.get(self._mesa) is self:
            del self._mesas_ocupadas[self._mesa]
        self._mesa = None

    def _al_cambiar_estado(self, nuevo_estado):
        if nuevo_estado in ("ENTREGADO", "CANCELADO"):
            self._liberar_mesa()

    def cerrar_pedido(self):
        self.cambiar_estado("ENTREGADO")

    def calcular_cargos(self):
        return Decimal("0.00")


class ParaLlevar(Pedido):
    COSTO_ENVASE_POR_PLATO = Decimal("2.00")

    def __init__(self, cliente, metodo_pago=None):
        super().__init__("ParaLlevar", cliente, metodo_pago)

    def calcular_envase(self):
        platos = sum(producto.contar_platos() * cantidad for producto, cantidad in self.items)
        return dinero(self.COSTO_ENVASE_POR_PLATO * platos)

    def detalle_cargos(self):
        return {"Envases": self.calcular_envase()}

    def calcular_cargos(self):
        return self.calcular_envase()

    def entregar_pedido(self):
        self.cambiar_estado("ENTREGADO")


class Delivery(Pedido):
    ENVIOS_POR_ZONA = {
        "cercado": Decimal("8.00"),
        "quillacollo": Decimal("15.00"),
        "sacaba": Decimal("15.00"),
        "vinto": Decimal("20.00")
    }
    ENVIO_GRATIS_DESDE = Decimal("150.00")
    PEDIDO_MINIMO = Decimal("40.00")

    def __init__(self, cliente, zona, metodo_pago=None):
        self._zona = str(zona).strip()
        self._zona_clave = normalizar_zona(zona)
        if self._zona_clave not in self.ENVIOS_POR_ZONA:
            raise ValueError("Zona no válida. Usa Cercado, Quillacollo, Sacaba o Vinto.")
        self._envio = self.ENVIOS_POR_ZONA[self._zona_clave]
        self._compensacion = Decimal("0.00")
        super().__init__("Delivery", cliente, metodo_pago)

    @property
    def zona(self):
        return self._zona

    @property
    def envio(self):
        return self._envio

    @property
    def compensacion(self):
        return self._compensacion

    def _validar_metodo_pago(self, metodo_pago):
        if not metodo_pago.acepta_delivery():
            raise ValueError("Delivery solo acepta efectivo o QR.")

    def calcular_envio(self):
        if self.calcular_subtotal() >= self.ENVIO_GRATIS_DESDE and self._zona_clave == "cercado":
            return Decimal("0.00")
        return self._envio

    def detalle_cargos(self):
        return {"Envío": self.calcular_envio(), "Compensación": self.compensacion}

    def calcular_cargos(self):
        subtotal = self.calcular_subtotal()
        if subtotal < self.PEDIDO_MINIMO:
            raise ValueError("El pedido mínimo para delivery es Bs 40.00.")
        return dinero(self.calcular_envio() - self.compensacion)

    def lugar_pedido(self):
        return self.zona

    def registrar_compensacion(self, monto):
        monto = dinero(monto)
        if monto < 0 or monto > self.calcular_envio():
            raise ValueError("La compensación debe estar entre Bs 0 y el costo del envío.")
        self._compensacion = monto
        return self._compensacion

    def _al_cambiar_estado(self, nuevo_estado):
        if nuevo_estado != "ENTREGADO":
            return
        minutos_transcurridos = (datetime.now() - self.fecha_registro).total_seconds() / 60
        if minutos_transcurridos > 60:
            self._compensacion = self.calcular_envio()

    def entregar_pedido(self):
        self.cambiar_estado("ENTREGADO")


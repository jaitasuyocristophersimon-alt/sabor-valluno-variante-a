from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
import unicodedata


def convertir_decimal(valor):
    return Decimal(str(valor))


def redondear_monto(valor):
    return convertir_decimal(valor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", str(texto).strip().lower())
    return "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")


def normalizar_dia(dia):
    dia = normalizar_texto(dia)
    dias = {
        "lunes": "lunes", "martes": "martes", "miercoles": "miércoles",
        "jueves": "jueves", "viernes": "viernes", "sabado": "sábado",
        "domingo": "domingo"
    }
    if dia not in dias:
        raise ValueError("El día debe ser uno de los siete días de la semana.")
    return dias[dia]


class Producto(ABC):
    def __init__(self, nombre, precio):
        self._nombre = ""
        self._precio = Decimal("0.00")
        self.nombre = nombre
        self.precio = precio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not str(valor).strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = str(valor).strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        valor = redondear_monto(valor)
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        self._precio = valor

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass

    def calcular_descuento(self):
        return Decimal("0.00")

    def contiene(self, producto):
        return self is producto


class Plato(Producto):
    DIAS_SEMANA = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")

    def __init__(self, nombre, precio, dias_disponibles=None):
        super().__init__(nombre, precio)
        if dias_disponibles is None or len(dias_disponibles) == 0:
            dias = list(self.DIAS_SEMANA)
        else:
            dias = [normalizar_dia(dia) for dia in dias_disponibles]
        if normalizar_texto(nombre) == "chicharron":
            dias = ["domingo"]
        self._dias_disponibles = tuple(dict.fromkeys(dias))

    @property
    def dias_disponibles(self):
        return self._dias_disponibles

    @dias_disponibles.setter
    def dias_disponibles(self, dias):
        nuevos_dias = tuple(dict.fromkeys(normalizar_dia(dia) for dia in dias))
        if normalizar_texto(self.nombre) == "chicharron":
            nuevos_dias = ("domingo",)
        if not nuevos_dias:
            raise ValueError("El plato debe estar disponible al menos un día.")
        self._dias_disponibles = nuevos_dias

    def calcular_precio(self):
        return self.precio

    def esta_disponible(self, dia):
        dia = normalizar_dia(dia)
        if normalizar_texto(self.nombre) == "chicharron":
            return dia == "domingo"
        return dia in self.dias_disponibles

    def contar_platos(self):
        return 1


class Bebida(Producto):
    def __init__(self, nombre, precio_vaso, tipo, presentacion="vaso"):
        self._precio_vaso = redondear_monto(precio_vaso)
        if self._precio_vaso <= 0:
            raise ValueError("El precio por vaso debe ser mayor que cero.")
        self._tipo = str(tipo).strip()
        if not self._tipo:
            raise ValueError("El tipo de bebida no puede estar vacío.")
        self._presentacion = "vaso"
        self.presentacion = presentacion
        precio_final = self._precio_vaso
        if self._presentacion == "jarra":
            precio_final = redondear_monto(self._precio_vaso * 3)
        super().__init__(nombre, precio_final)

    @property
    def precio_vaso(self):
        return self._precio_vaso

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if not str(valor).strip():
            raise ValueError("El tipo de bebida no puede estar vacío.")
        self._tipo = str(valor).strip()

    @property
    def presentacion(self):
        return self._presentacion

    @presentacion.setter
    def presentacion(self, valor):
        valor = normalizar_texto(valor)
        if valor not in ("vaso", "jarra"):
            raise ValueError("La presentación debe ser vaso o jarra.")
        self._presentacion = valor

    def calcular_precio(self):
        if self.presentacion == "jarra":
            return redondear_monto(self.precio_vaso * 3)
        return self.precio_vaso

    def esta_disponible(self, dia):
        normalizar_dia(dia)
        return True

    def contar_platos(self):
        return 0


class Combo(Producto):
    def __init__(self, nombre, combo="", productos=None, descuento=Decimal("0.10")):
        self._productos = []
        self._combo = str(combo).strip() if combo else str(nombre).strip()
        self._descuento = Decimal("0.10")
        super().__init__(nombre, Decimal("0.01"))
        self.descuento = descuento
        if productos:
            for producto in productos:
                self.agregar_producto(producto)

    @property
    def combo(self):
        return self._combo

    @combo.setter
    def combo(self, valor):
        if not str(valor).strip():
            raise ValueError("El nombre o descripción del combo no puede estar vacío.")
        self._combo = str(valor).strip()

    @property
    def productos(self):
        return tuple(self._productos)

    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, valor):
        valor = convertir_decimal(valor)
        if valor < 0 or valor >= 1:
            raise ValueError("El descuento debe ser desde 0 hasta menos de 1.")
        self._descuento = valor

    @property
    def precio(self):
        if len(self._productos) >= 2:
            return self.calcular_precio()
        return self._precio

    @precio.setter
    def precio(self, valor):
        valor = redondear_monto(valor)
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        self._precio = valor

    def agregar_producto(self, producto):
        if producto.contiene(self):
            raise ValueError("Un combo no puede contenerse a sí mismo ni crear ciclos.")
        self._productos.append(producto)

    def calcular_combo(self):
        if len(self._productos) < 2:
            raise ValueError("Un combo debe contener por lo menos dos productos.")
        subtotal = sum((producto.calcular_precio() for producto in self._productos), Decimal("0"))
        return redondear_monto(subtotal)

    def calcular_precio(self):
        subtotal = self.calcular_combo()
        return redondear_monto(subtotal * (Decimal("1") - self.descuento))

    def calcular_descuento(self):
        subtotal = sum((producto.calcular_precio() for producto in self._productos), Decimal("0.00"))
        ahorro_propio = redondear_monto(subtotal * self.descuento)
        ahorro_anidado = sum((producto.calcular_descuento() for producto in self._productos), Decimal("0.00"))
        return redondear_monto(ahorro_propio + ahorro_anidado)

    def esta_disponible(self, dia):
        normalizar_dia(dia)
        if len(self._productos) < 2:
            return False
        return all(producto.esta_disponible(dia) for producto in self._productos)

    def contar_platos(self):
        return sum(producto.contar_platos() for producto in self._productos)

    def contiene(self, producto):
        if self is producto:
            return True
        return any(componente.contiene(producto) for componente in self._productos)

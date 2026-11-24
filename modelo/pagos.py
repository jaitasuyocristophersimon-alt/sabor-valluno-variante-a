from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


def dinero(valor):
    return Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class MetodoPago(ABC):
    def __init__(self, monto=0):
        self._monto = dinero(monto)
        if self._monto < 0:
            raise ValueError("El monto no puede ser negativo.")

    @property
    def monto(self):
        return self._monto

    def calcular_total(self, monto_base):
        self._monto = dinero(monto_base)
        return self._monto

    def calcular_comision(self, monto_base):
        return Decimal("0.00")

    def acepta_delivery(self):
        return True

    @abstractmethod
    def procesar_pago(self, monto):
        pass


class Efectivo(MetodoPago):
    def __init__(self, monto_recibido):
        super().__init__()
        self._monto_recibido = dinero(monto_recibido)
        self._cambio = Decimal("0.00")

    @property
    def monto_recibido(self):
        return self._monto_recibido

    def calcular_monto(self, monto):
        monto = dinero(monto)
        if self.monto_recibido < monto:
            raise ValueError("El monto recibido no cubre el total.")
        self._cambio = dinero(self.monto_recibido - monto)
        return self._cambio

    def procesar_pago(self, monto):
        total = self.calcular_total(monto)
        cambio = self.calcular_monto(total)
        return {"metodo": "Efectivo", "total": total, "recibido": self.monto_recibido, "cambio": cambio}


class QR(MetodoPago):
    def __init__(self, monto_recibido, codigo):
        super().__init__()
        self._monto_recibido = dinero(monto_recibido)
        self._codigo = str(codigo).strip()

    @property
    def monto_recibido(self):
        return self._monto_recibido

    def validar_codigo(self):
        return len(self._codigo) == 10 and self._codigo.isdigit()

    def procesar_pago(self, monto):
        total = self.calcular_total(monto)
        if not self.validar_codigo():
            raise ValueError("El código QR debe tener exactamente 10 dígitos.")
        if self.monto_recibido < total:
            raise ValueError("El monto recibido por QR no cubre el total.")
        return {"metodo": "QR", "total": total, "recibido": self.monto_recibido, "codigo": self._codigo}


class Tarjeta(MetodoPago):
    def __init__(self, comision=Decimal("0.03")):
        super().__init__()
        self._comision = Decimal(str(comision))
        if self._comision < 0 or self._comision >= 1:
            raise ValueError("La comisión debe ser desde 0 hasta menos de 1.")
        self._comision_actual = Decimal("0.00")
        self._monto_base = Decimal("0.00")

    @property
    def comision(self):
        return self._comision

    def acepta_delivery(self):
        return False

    def calcular_comision(self, monto_base):
        return dinero(dinero(monto_base) * self.comision)

    def calcular_total(self, monto_base):
        self._monto_base = dinero(monto_base)
        self._comision_actual = self.calcular_comision(self._monto_base)
        self._monto = dinero(self._monto_base + self._comision_actual)
        return self._monto

    def procesar_pago(self, monto):
        total = dinero(monto)
        if self._monto != total:
            self.calcular_total(total)
        return {"metodo": "Tarjeta", "subtotal": self._monto_base, "comision": self._comision_actual, "total": self._monto}

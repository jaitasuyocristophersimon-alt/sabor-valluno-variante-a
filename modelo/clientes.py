class Cliente:
    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono
        self._pedidos = []
        self.nombre = nombre
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not str(valor).strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = str(valor).strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor).strip()
        if len(valor) != 8 or not valor.isdigit() or valor[0] not in "67":
            raise ValueError("El teléfono debe tener 8 dígitos y comenzar con 6 o 7.")
        self._telefono = valor

    @property
    def pedidos(self):
        return tuple(self._pedidos)

    def validar_telefono(self):
        return len(self.telefono) == 8 and self.telefono.isdigit() and self.telefono[0] in "67"

    def realizar_pedido(self, pedido):
        if pedido not in self._pedidos:
            self._pedidos.append(pedido)
        return pedido

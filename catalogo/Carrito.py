class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get('carrito')  # Cambiado de 'carro' a 'carrito'
        if not carro:
            self.session['carrito'] = {}
            self.carro = self.session['carrito']
        else:
            self.carro = carro

    def agregar_producto(self, producto):
        id = str(producto.id_producto)
        if id not in self.carro:
            self.carro[id] = {
                'nombre': producto.nombre_producto,
                'precio': int(producto.precio),
                'cantidad': 1,
                'imagen': producto.imagen.url if producto.imagen else '',
                'precio_final': int(producto.precio),
                'stock': producto.stock
            }
        else:
            if self.carro[id]['cantidad'] < producto.stock:
                self.carro[id]['cantidad'] += 1
                self.carro[id]['precio_final'] += producto.precio
        self.session['carrito'] = self.carro
        self.session.modified = True

    def sumar(self, producto):
        id = str(producto.id_producto)
        if id not in self.carro:
            self.carro[id] = {
                'nombre': producto.nombre_producto,
                'precio': int(producto.precio),
                'cantidad': 1,
                'imagen': producto.imagen.url if producto.imagen else '',
                'precio_final': int(producto.precio),
                'stock': producto.stock
            }
        else:
            self.carro[id]['cantidad'] += 1
            self.carro[id]['precio_final'] += producto.precio
        self.session['carrito'] = self.carro
        self.session.modified = True


    def guardar_carro(self):
        self.session['carrito'] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        id = str(producto.id_producto)
        if id in self.carro:
            del self.carro[id]
            self.guardar_carro()

    def restar_producto(self, producto):
        id = str(producto.id_producto)
        if id in self.carro.keys():
            self.carro[id]['cantidad'] -= 1
            self.carro[id]['precio_final'] -= producto.precio
            if self.carro[id]['cantidad'] <= 0:
                self.eliminar(producto)
            self.guardar_carro()

    def limpiar(self):
        self.session['carrito'] = {}
        self.session.modified = True
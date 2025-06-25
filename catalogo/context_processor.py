def total_carrito(request):
    total = 0
    if 'carrito' in request.session:
        for value in request.session['carrito'].values():
            total += float(value.get('precio_final', value.get('precio', 0)))
    return {'total_carrito': total}
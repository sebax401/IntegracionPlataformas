from django.http import HttpResponseForbidden

def solo_ferromax(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.email.lower().endswith('@ferromax.cl'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Acceso exclusivo para correos @ferromax.cl")
    return _wrapped_view
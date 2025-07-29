from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def check_perfil(perfil_list):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.perfil in perfil_list:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden()
        return wrapper
    return decorator

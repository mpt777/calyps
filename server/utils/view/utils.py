from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator



def superuser_required(view_func):
    """
    Decorator that checks if the user is a superuser.
    If the user is not a superuser, it returns a HttpResponseForbidden.
    """
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You don't have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


from functools import wraps
from rest_framework.exceptions import PermissionDenied

def check_owner_permission(obj_attr='created_by'):
    """
    Decorator to check if the user is the owner of an object.
    
    :param obj_attr: The attribute on the object that represents the owner (default is 'created_by').
    """
    def decorator(view_method):
        @wraps(view_method)
        def _wrapped_view(self, request, *args, **kwargs):
            # Get the object instance (recipe or ingredient)
            instance = self.get_object()
            
            # Check if the user is the owner
            if getattr(instance, obj_attr) != request.user:
                raise PermissionDenied("You do not have permission to access this resource.")
            
            # Proceed with the original view method if user is the owner
            return view_method(self, request, *args, **kwargs)
        
        return _wrapped_view
    return decorator

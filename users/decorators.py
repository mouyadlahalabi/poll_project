from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import login_required

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # التحقق من دور المستخدم
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        # التوجيه إلى صفحة خطأ عند عدم الصلاحية
        return redirect('users:error_403')  
    return _wrapped_view


def user_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # التحقق من دور المستخدم
        if hasattr(request.user, 'role') and request.user.role == 'customer':
            return view_func(request, *args, **kwargs)
        # التوجيه إلى صفحة خطأ عند عدم الصلاحية
        return redirect('users:error_403')  
    return _wrapped_view
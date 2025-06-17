from django.shortcuts import redirect , render ,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import login , logout , get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count

User = get_user_model()
from .decorators import admin_required , user_required 


@login_required
def redirect_after_login(request):
    if request.user.is_admin():
        return redirect('users:admin_dashboard')
    elif request.user.is_customer():
        return redirect('users:user_dashboard')
    else:
        return redirect('users:login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request," تم تسجيل الدخول بنجاح")
            return redirect('users:redirect_after_login')
        else:
            messages.error(request,"يوجد خطأ في اسم المستخدم أو كلمة المرور")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('users:login')




@admin_required
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')



def admin_required(user):
    return user.is_authenticated and user.is_admin  # أو user.is_staff


@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    User = get_user_model()
    users = User.objects.annotate(survey_count=Count('surveys')).order_by('date_joined')
    return render(request, 'users/admin_dashboard.html', {'users': users})



@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.user == user:
        # منع حذف نفسه
        return redirect('users:admin_dashboard')  # غيّر حسب اسم صفحة الإدارة

    user.delete()
    return redirect('users:admin_dashboard')



@user_required
def error_403(request):
    return render(request, 'users/error_403.html', status=403)




def user_dashboard(request):  # ⚠️ يجب أن يكون الاسم مطابقًا تمامًا
    return render(request, 'users/user_dashboard.html')




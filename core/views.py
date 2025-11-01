from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test ,login_required
# Create your views here.
@login_required
def home(request):
    admin = request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()
    return render(request,'home.html',{"user_is_admin":admin})

def no_permission(request):
    return render(request,"no-permission.html")
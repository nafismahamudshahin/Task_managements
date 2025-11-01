from django.shortcuts import render , redirect , HttpResponse
from django.contrib.auth import login , logout ,authenticate
from users.forms import CustomRegisterForm , RoleAssignedForm , CreateGroupForm , CustomPasswordChangeForm , CustomPasswordConfirmForm, CustomPasswordResetForm
from django.contrib import messages
from django.contrib.auth.models import User , Group
from django.contrib.auth.tokens import default_token_generator
from users.forms import LoginForm ,EditProfileForm
from django.contrib.auth.decorators import user_passes_test ,login_required
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView , PasswordChangeView , PasswordResetView , PasswordResetConfirmView
from django.views.generic import TemplateView , UpdateView
from django.urls import reverse_lazy
from users.models import CustomUser
def is_admin(user):
   return user.groups.filter(name="Admin").exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_user(user):
    return user.groups.filter(name="User").exists()

def is_manager_or_admin(user):
    return  is_manager(user) or is_admin(user)

# Create your views here.
def sign_up(request):
    form = CustomRegisterForm()  
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request,"A cofirmation message send. please check your email.")
            return redirect("sign-in")
    return render(request,"registration/register.html",{'form':form})

def sign_in(request):
    form= LoginForm()
    if request.method == "POST":
        form  = LoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect("home")
    return render(request,'login.html' ,{"form":form} )

class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()
    
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")

# activate user account by default token:
def activateUser(request,id,token):
    try:
        user = CustomUser.objects.get(id=id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect("sign-in")  
        else:
            return HttpResponse("Invalid id or token")
    except Exception as e:
        return HttpResponse(f"{e}")

# admin dashboard:
@login_required
@user_passes_test(is_admin , login_url="no-permission")
def admin_dashboard(request):
    users = CustomUser.objects.prefetch_related(
        Prefetch('groups' , queryset=Group.objects.all(), to_attr="all_groups")
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0]
        else:
            user.group_name = "no assigned"
    return render(request,"admin/dashboard.html",{'users':users})

@login_required
@user_passes_test(is_admin , login_url="no-permission")
def assign_role(request,id):
    user = CustomUser.objects.get(id=id)
    form = RoleAssignedForm()
    print(user)
    if request.method == "POST":
        form = RoleAssignedForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,"Successfully asigned role")
        return redirect("admin-dashboard")
    return render(request,"admin/assigne_role.html",{'form':form})

@login_required
@user_passes_test(is_admin , login_url="no-permission")
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Successfully created a new Group")
            return redirect('create-group')
    return render(request,"admin/assigne_group.html",{"form":form})

@login_required
@user_passes_test(is_admin, login_url="no-permission")
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request,"admin/group_list.html",{'groups':groups})

@login_required
@user_passes_test(is_admin, login_url="no-permission")
def task_details(request):
    return render(request,"admin/task_details.html")

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "account/password_change.html"
    success_url = reverse_lazy("sign-in")

class ProfileView(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
# password reset view:
class PasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = "registration/password_reset.html"
    success_url = reverse_lazy('sign-in')
    html_email_template_name = "registration/reset_mail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = self.request.get_host()
        return context
    

    def form_valid(self, form):
        messages.success(self.request,"A reset email send .Please check your email.")
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordConfirmForm
    template_name = "registration/password_reset.html"
    success_url = reverse_lazy('sign-in')
    def form_valid(self, form):
        messages.success(self.request,"Password Reset successfully.")
        return super().form_valid(form)

# Edit profile
"""
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'account/edit_profile.html'
    context_object_name = "form"

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user= self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userprofile = UserProfile.objects.get(user=self.request.user)
        print("view",userprofile)
        context['form'] = self.form_class(instance = self.object, userprofile = userprofile)
        return context
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect("profile")    
"""
class EditProfileView(UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = "account/edit_profile.html"
    template_name_field = "form"

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect("profile")    
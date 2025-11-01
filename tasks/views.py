from django.shortcuts import render ,redirect ,get_object_or_404
from datetime import datetime
from tasks.models import *
from django.db.models import Q , Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test ,login_required , permission_required
from users.views import is_manager , is_admin ,is_user
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic.base import ContextMixin 
from django.views.generic import ListView ,DetailView ,CreateView , DeleteView
# form:
from tasks.forms import CreateProject ,CreateTask , CreateEmployee , CreateTaskDetails
from django.urls import reverse_lazy
# Create your views here.
create_detorator = [login_required,user_passes_test(is_manager)]

""" Function base view"""
@login_required
@user_passes_test(is_manager, login_url="no-permission")
def new_project_create(request):
    if request.method == "POST":
        form = CreateProject(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'form.html',{'form':form})
    else:
        form = CreateProject()
    return render(request,'form.html',{'form':form})

# create new project:
@method_decorator(create_detorator , name="dispatch")
class CreateProject(CreateView):
    model = Project
    fields = "__all__"
    template_name = "form.html"
    success_url = reverse_lazy("view-project")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = context['form']
        return context
    
# view Project:
class ViewProject(ListView):
    model = Project
    template_name = "all_projects.html"
    context_object_name ="projects"

    def get_queryset(self):
        return Project.objects.annotate( count = Count("task"))


# task:
@login_required
@user_passes_test(is_manager, login_url="no-permission")
def new_task_create(request):
    if request.method == "POST":
        task_form = CreateTask(request.POST)
        details_form = CreateTaskDetails(request.POST , request.FILES)
        if task_form.is_valid() and details_form.is_valid():
            task = task_form.save()
            task_details = details_form.save(commit=False)
            task_details.task = task
            task_details.save()
        
        messages.success(request,"task create successfully")
        return redirect('create_task')   
        
    else:
        task_form = CreateTask()
        details_form = CreateTaskDetails()
    return render(request,'task_form.html',{'task_form':task_form,'details_form':details_form})
create_decorator = [login_required,user_passes_test(is_manager, login_url="no-permission")]

# class base create task:
# @method_decorator(create_decorator, name='dispatch')
class CreateTaskView(LoginRequiredMixin,View):

    def get(self,request,*args,**kwargs):
        task_form = CreateTask()
        details_form = CreateTaskDetails()
        context = {
            'task_form': task_form,
            'details_form': details_form,
        }
        return render(request,"task_form.html",context)
    
    def post(self,request,*args,**keargs):
        task_form = CreateTask(request.POST)
        detasils_form = CreateTaskDetails(request.POST ,request.FILES)
        if task_form.is_valid() and detasils_form.is_valid():
            task = task_form.save()
            details = detasils_form.save(commit=False)
            details.task = task
            details.save()
            messages.success(request,"Task Created Successfully")
            return redirect("create_task")

# details task:
class DetailsTaskView(DetailView):
    model = Task
    template_name = "task_details.html"
    context_object_name = "task"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allstatus'] = Task.TASK_STATUS
        return context
    
    def post(self, request , *args,**keargs):
        task = self.get_object()
        select_status = request.POST.get('task_status')
        task.status = select_status
        task.save()
        return redirect('task', task.id)
    
# updated task:
@login_required
@user_passes_test(is_manager, login_url="no-permission")
def updated_task(request , id):
    # find the task by id:
    instance_task = get_object_or_404(Task,id=id)
    # details_form = CreateTaskDetails()
    instance_task_details = getattr(instance_task,'details',None)

    if request.method == "POST":
        task_form = CreateTask(request.POST ,instance=instance_task)
        details_form = CreateTaskDetails(request.POST ,instance= instance_task_details)
        if task_form.is_valid() and details_form.is_valid():
            task = task_form.save()
            task_details = details_form.save(commit=False)
            task_details.task = task
            task_details.save()
        messages.success(request,"task updated successfully")
        return redirect('task',id)   
    else:
        # populate the task and details:
        task_form = CreateTask(instance=instance_task)
        details_form = CreateTaskDetails(instance=instance_task_details)

    return render(request,'form.html',{'task_form':task_form,'details_form':details_form})

@method_decorator(create_decorator,name="dispatch")
class UpdateTask(LoginRequiredMixin, ContextMixin,View):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form',CreateTask())
        context['details_form'] = kwargs.get('details_form',CreateTaskDetails())
        return context
    
    def get(self,request,id,*args,**kwargs):
        task = get_object_or_404(Task,id=id)
        instance_task_details = getattr(task,'details',None)
        task_form = CreateTask(instance = task)
        details_form = CreateTaskDetails(instance=instance_task_details)
        return render(request,"form.html", self.get_context_data(task_form=task_form,details_form=details_form))

    def post(self,request,id,*args,**kwargs):
        task = get_object_or_404(Task,id=id)
        instance_task_details = getattr(task,'details',None)
        task_form = CreateTask(request.POST ,instance=task)
        details_form = CreateTaskDetails(request.POST ,instance= instance_task_details)
        if task_form.is_valid() and details_form.is_valid():
            task = task_form.save()
            task_details = details_form.save(commit=False)
            task_details.task = task
            task_details.save()
            messages.success(request,"task updated successfully")
            return redirect('task',id)   

# delete task:
@login_required
@user_passes_test(is_manager, login_url="no-permission")
def delete_task(request,id):
    if request.method == "POST":
        task = Task.objects.get(id = id)
        task.delete()
        messages.success(request,"Task Deleted Successfully")
        return redirect("dashboard")
    else:
        messages.error(request,"Somthing wrong found")
        return redirect('dashboard')

class DeleteTask(DeleteView):
    medel = Task


@login_required
@user_passes_test(is_manager, login_url="no-permission")
def EmployeeRegister(request):
    if request.method == "POST":
        form = CreateEmployee(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'form.html',{'form':form,'message':"Successfully Submitted"})
    else:
        form = CreateEmployee()
    return render(request,'form.html',{'form':form})

@login_required
@user_passes_test(is_manager, login_url="no-permission")
def makeDetails(request):
    if request.method == "POST":
        form = CreateTaskDetails(request.POST)
        if form.is_valid():
            form.save()
        return render(request,'form.html',{'form':form,'message':"Successfully Submitted"})
    else:
        form = CreateTaskDetails()
    return render(request,'form.html',{'form':form})

def Test(request):
    # data = Task.objects.all()
    # data = Task.objects.filter(due_date = datetime.today())
    # data = Task.objects.filter(status = "COMPLETED")
    # data = Task.objects.filter(status = "IN-PROCESS")
    # data = Task.objects.exclude(status = "PENDING")
    # data = Task.objects.filter(status__icontains = "pendinG")
    # data = Task.objects.filter(Q(status = "PENDING") | Q(status = "IN_PROCESS"))
    data = Task.objects.select_related('details').all()
    data = TaskDetails.objects.select_related('task').all()

    
    data = Task.objects.prefetch_related('assigne_to').all()
    
    data = Task.objects.aggregate(num_task = Count('id'))
    
    data = Task.objects.annotate(num_task = Count('id'))
    return render(request,'test.html',{'tests':data})


# manager dashboard:
@method_decorator(user_passes_test(is_manager, login_url="no-permission") , name="dispatch")
class ManagerView(LoginRequiredMixin , View):
    def get(self,request,*args,**kwargs):
        type = request.GET.get('type',"all")
        base_tasks = Task.objects.select_related('details').all().prefetch_related('assigne_to').order_by('due_date')

        if type == "completed":
            tasks = base_tasks.filter(status = "COMPLETED")
        elif type == "in-progress":
            tasks = base_tasks.filter(status = "IN-PROCESS")
        elif type == "pending":
            tasks = base_tasks.filter(status = "PENDING")
        elif type == "all":
            tasks = base_tasks

        counts = Task.objects.aggregate(
            total = Count('id'),
            in_process = Count('id', filter=Q(status = "IN-PROCESS")),
            pending = Count('id', filter=Q(status = "PENDING")),
            completed = Count('id',filter=Q(status = "COMPLETED")),
        )

        return render(request,'dashboard/manager.html',{
            'tasks': tasks,
            'counts': counts,
            })
    
# render user:
def User(request):
    tasks = Task.objects.all()
    # tasks cnt:
    total_task = tasks.count()
    # in process tasks cnt:
    in_cnt = 0
    completed_task =0
    pending_task = 0
    for task in tasks:
        if task.status == "IN-PROCESS":
            in_cnt +=1
        elif task.status =="COMPLETED":
            completed_task +=1
        else:
            pending_task +=1

    return render(request,'dashboard/user.html',{
        'total_task':total_task,
        'in_process':in_cnt,
        'completed_task':completed_task,
        'pending_task':pending_task,
        })

def task_details(request,id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        selected_status = request.POST.get("task_status")
        task.status = selected_status
        task.save()
        return redirect("task", id)
    context ={
        "task":task,
        "allstatus": Task.TASK_STATUS
    }
    return render(request,"task_details.html",context)

@login_required
def dashboard(request):
    if is_admin(request.user):
        print("worked this filed name of admin-dashboard")
        return redirect("admin-dashboard")
    elif is_manager(request.user):
        print("manager:____")
        return redirect("manager-dashboard")
    elif is_user(request.user):
        return redirect('user-dashboard')

    return redirect("no-permission")
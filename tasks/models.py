from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Project(models.Model):
    name = models.CharField()
    start_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField()
    position = models.CharField()
    salary = models.IntegerField()
    email = models.EmailField(default="patirer765@etenx.com", null=True ,blank=True)
    def __str__(self):
        return self.name
    
class Task(models.Model):
    TASK_STATUS = [
        ('PENDING',"Pending"),
        ('IN-PROCESS',"In-Prodess"),
        ('COMPLETED','completed')
    ]
    
    task_name = models.CharField()
    description = models.TextField()
    due_date = models.DateField()
    # asset = models.ImageField(upload_to="task_asset", blank=True, null=True)
    status = models.CharField(choices=TASK_STATUS,default="Pending")
    project = models.ForeignKey(Project,on_delete=models.CASCADE,default=3 , related_name="task")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigne_to = models.ManyToManyField(settings.AUTH_USER_MODEL , related_name="task")
    
class TaskDetails(models.Model):
    high = 'H'
    medium = 'M'
    low = 'L'
    PRIORITY_OPTION =(
        (high,'H'),
        (medium,'M'),
        (low,'L')
    )
    asset = models.ImageField(upload_to="task_asset", blank=True, null=True , default="task_asset/default_img.jpg")
    task = models.OneToOneField(Task,on_delete=models.CASCADE , related_name="details") # onetoone relation with task
    assigne_to = models.CharField(null=True,blank=True,default="NAN")
    priority = models.CharField(max_length=1,choices=PRIORITY_OPTION,default= medium)
    note = models.TextField(blank=True,null=True)


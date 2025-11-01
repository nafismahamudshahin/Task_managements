from django.dispatch import receiver
from django.db.models.signals import pre_delete , post_save , pre_save , m2m_changed
from django.core.mail import send_mail
from tasks.models import Task


@receiver(pre_delete,sender = Task)
def alart_for_task_delate(sender,instance,**kwargs):
    assigne_email = [emp.email for emp in instance.assigne_to.all()]
    # assigne_email.append("mogil85942@bllibl.com")
    # assigne_email.append("nafismahamud.info@gmail.com")
    print(assigne_email)
    send_mail(
        "delete task",
        f"Your task is deleted: {instance.task_name}.",
        "nafismahamudshahin@gmail.com",
        assigne_email,
        fail_silently=False,
    )

# post signal:
@receiver(post_save,sender=Task)
def alart_for_task_creation(sender,instance, **kwargs):
    print("sender: ",sender)
    print("instance: ",instance)
    print(kwargs)


# pre_save signal:
@receiver(pre_save,sender = Task)
def notify(sender,instance,**kwargs):
    print(instance.task_name)
    instance.is_completed = True

# pass:
# 


@receiver(m2m_changed,sender = Task.assigne_to.through)
def notify_employee_on_task_creation(sender,instance,action,**kwargs):
    if action == "post_add":
        assigne_email = [emp.email for emp in instance.assigne_to.all()]
        send_mail(
            "Assigned new task for you.",
            f"Assigned new task for you: task task: {instance.task_name}.",
            "nafismahamudshahin@gmail.com",
            assigne_email,
            fail_silently=False,
        )
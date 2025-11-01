from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User , Group , Permission
from users.models import CustomUser
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives


        # text_content = strip_tags(html_content)
        # message = f"Hi. {instance.username}\nPlease activate your account\nLink: {activation_url}"
@receiver(post_save, sender= CustomUser)
def send_activation_mail(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FORNTEND_URL}/activate/{instance.id}/{token}/" 
        subject = "Activate Your account"
        context = {
        'user_name': f"{instance.first_name} {instance.last_name}",
        'username': instance.username,
        'link': activation_url,
        }
        html_content = render_to_string("registration/activation_mail.html",context)
        recipient_email = [instance.email]
        text_content = ""

        try:
            # Use EmailMultiAlternatives for HTML mail
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_email,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            print(f"Failed to send Email to {instance.email}: {str(e)}")
            
@receiver(post_save,sender=CustomUser)
def assign_role(sender,instance,created,**kwargs):
    if created:
        user_group , created = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()
"""
@receiver(post_save,sender = User)
def create_or_update_user_profile(sender,instance,created,**kwargs):
    if created:
        profile = UserProfile.objects.create(user = instance)
    instance.userprofile.save()
"""
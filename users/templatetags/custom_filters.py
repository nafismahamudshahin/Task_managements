from django import template
from datetime import datetime
from django.utils import timezone
register = template.Library()

@register.filter
def humanized_date(value):  

    value = timezone.localtime(value)
    today = datetime.now().date()
    
    if value.date() == today:
        return f"Today at {value.strftime('%I:%M %p')}"
    elif value.date() == today.replace(day=today.day - 1) :
        return f"Yeastarday at {value.strftime('%I:%M %p')}"
    else:
        return f"{value.date()} {value.strftime('%I:%M %p')}"
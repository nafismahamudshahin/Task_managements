from django.urls import path
from viewbase.views import Gretting , HiGreeting
urlpatterns = [
    path('greeting/',Gretting.as_view(),name="greeting"),
    path('higreeting',HiGreeting.as_view(),)
]

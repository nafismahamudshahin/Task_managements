
from django.contrib import admin
from django.urls import path,include
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings
from core.views import home
urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('admin/', admin.site.urls ),
    path('',include('tasks.urls')),
    path('',include('users.urls')),
    path('',home,name="home"),
    path('',include('viewbase.urls')),
] + debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
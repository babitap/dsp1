from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path, include


urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path('api/', include('api.urls')),


]

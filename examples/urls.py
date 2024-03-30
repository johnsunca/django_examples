"""
URL configuration for examples project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views
from django.views.generic import TemplateView

urlpatterns = [    
    # Homepage
    path("", TemplateView.as_view(template_name='index.html'), name='home'),    # this is at project level
    # Admin
    path('admin/', admin.site.urls),
    # Auth
    path('accounts/', include('django.contrib.auth.urls')), 
    path("accounts/profile/", views.profile, name="profile"), # not needed since login redirect set in settings
    path("signup/", views.signup, name="signup"), # this can be moved out to project level

    # Apps
    path("ecommerce/", include("ecommerce.urls")), 
    path("studentmgmtsys/", include("studentmgmtsys.urls")), 
    path("bmsapp/", include("bmsapp.urls")), 
    # path("modelsapp/", include("modelsapp.urls")),
    # path("helloworld/", include("helloworld.urls")),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:     # To serve media files only in development, not in production
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

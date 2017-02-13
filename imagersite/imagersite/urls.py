"""imagersite URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import (
    admin,
    auth
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from imager_api import views

router = DefaultRouter()
router.register(r'photos', views.PhotoViewSet, base_name="photos")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="imagersite/home.html"), name='homepage'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/', auth.views.login, name='login'),
    url(r'^logout/', auth.views.logout, {'next_page': '/'}, name='logout'),
    url(r'^profile/', include('imager_profile.urls')),
    url(r'^images/', include('imager_images.urls')),
    url(r'^api/v1/', include(router.urls)),
    url(r'^oauth/', include('social_django.urls', namespace='social'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

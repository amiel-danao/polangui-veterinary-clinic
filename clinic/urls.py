"""clinic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app import views
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.urls import re_path as url
from rest_framework import routers
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customer', views.CustomerViewSet)
router.register(r'device_token', views.DeviceTokenViewSet)
router.register(r'pet', views.PetViewSet)
# router.register(r'device', views.DeviceViewSet)
router.register(r'upload_pet_image', views.UploadPetImageViewSet)
router.register(r'upload_customer_image', views.UploadCustomerImageViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'))),
    path('admin/', admin.site.urls),
    path('api/', include((router.urls, 'app_name'), namespace='instance_name')),
    path('chat/', views.chat_all, name='chat'),
    path('video_call/<str:message_gc_id>/',
         views.video_call, name='video-call'),
    path('chat/<str:message_gc_id>/', views.chat),
    url(r'^api/petlist$', views.pet_list),
    url(r'^api/devicelist$', views.DeviceList.as_view()),
    url(r'^api/medicaldetails/(?P<pk>[0-9]+)$', views.medical_detail),
    url(r'^api/medicallist$', views.get_medical_by_pet),
    url(r'^api/immunizationlist$', views.get_immunization_by_pet),
    url(r'^api/breedlist$', views.get_breeds),
    url(r'^api/customerlist', views.customer_list),
    url(r'^api/veterinarylist', views.veterinary_list),
    url(r'^chaining/', include('smart_selects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

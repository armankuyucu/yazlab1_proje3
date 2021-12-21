from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.userPanel, name="userpanel"),
    path('info/', views.info, name="info"),
    path('upload/', views.upload, name="upload"),
    path('adminpanel/', views.adminPanel, name="adminpanel"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

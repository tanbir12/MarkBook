from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.indexPage,name='Indexpage'),
    path('Student/<str:roll_no>',views.markPage,name='Markpage'),
    path('accounts/',include("django.contrib.auth.urls"),name='admin'),
    path('accounts/',include('teacher.urls'),name='admin'),
]

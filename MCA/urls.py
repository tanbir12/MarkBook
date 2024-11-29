from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.indexPage,name='Indexpage'),
    path('about/',views.aboutPage,name='Aboutpage'),
    path('contact/',views.contactPage,name='Contactpage'),
    path('Student/<str:roll_no>',views.markPage,name='Markpage'),
    path('accounts/',include("django.contrib.auth.urls"),name='admin'),
    path('accounts/',include('teacher.urls'),name='admin'),
]


urlpatterns += staticfiles_urlpatterns()
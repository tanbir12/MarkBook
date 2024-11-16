from django.urls import path
from teacher import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('profile/',views.profilePage,name='profile_page'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page = 'profile_page'),name='logout'),

    path('add_teacher/',views.addTeacher,name='add_teacher'),
    path('delete_teacher/',views.deleteTeacher,name='delete_teacher'),
    path('manage_subjects/',views.manageSubject,name='manage_subjects'),

    #__________  Path for Students Changes ________________
    path('add_student/',views.addStudent,name='add-student'),
    path('add_marks/<str:year>/<str:teacher_id>/<str:subject_id>',views.add_marks_view,name='add-marks'),
]
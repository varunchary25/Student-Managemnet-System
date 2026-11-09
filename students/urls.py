from django.urls import path

from . import views
from . import api_views

urlpatterns = [
    path('',views.home, name='home'),

    path('students/', views.student_list, name='student_list'),

    path('students/register/', views.student_register, name='student_register'),


    path('api/students/',api_views.student_list_api, name='student_list_api'),

    path('api/students/create/', api_views.student_create_api, name='student_create_api'),

    path('api/students/<int:student_id>/delete/', api_views.student_delete_api, name='student_delete_api'),

  

    path('login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='user_logout'),
    path('save-student-name/', views.save_student_name, name='save_student_name'),
    path('show-student-name', views.show_student_name, name='show_student_name'),
    path('api/protected/', views.protected_view, name='protected_view'),

]
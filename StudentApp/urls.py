from django.urls import path
from StudentApp import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.Home,name="Home"),
    path('signup',views.signup,name="signup"),
    path('handlelogin',views.handlelogin,name="handlelogin"),
    path('change_password', views.change_password, name='change_password'),
    path('logout', views.logout_page, name="logout_page"),
    path('add_student', views.add_student, name="add_student"),
    path('student_list', views.student_list, name="students_list"),
    path('delete_student(?p<int:pid>)', views.Delete_Student, name='delete_student'),
    # path('view_student',views.View_Student,name='view_Student'),
    path('viewOneStudent(<int:adm_number>)', views.viewOneStudent, name='viewOneStudent'),
    path('update_student(?p<int:adm_number>)',views.update_student, name="update_Student"),
    #dashboard urls
    path('dashboard/', views.dashboard, name='dashboard'),
    
     #reset password urls
    path('password-reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
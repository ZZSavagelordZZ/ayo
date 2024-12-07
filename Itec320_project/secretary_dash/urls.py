from django.urls import path
from . import views
from django.urls import reverse
from django.http import HttpResponseRedirect

app_name = 'secretary_dash'

urlpatterns = [
    # Root and Authentication
    path('', views.root_redirect, name='root'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Secretary Routes
    path('secretary/', views.secretary_dashboard, name='secretary_dashboard'),
    path('secretary/appointments/', views.appointment_list, name='appointment_list'),
    path('secretary/appointments/create/', views.appointment_create, name='appointment_create'),
    path('secretary/appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    path('secretary/appointments/<int:pk>/edit/', views.appointment_edit, name='edit_appointment'),
    path('doctor/appointments/<int:pk>/cancel/', views.doctor_cancel_appointment, name='doctor_cancel_appointment'),

    # Doctor Routes
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/secretaries/', views.secretary_list, name='secretary_list'),
    path('doctor/secretaries/create/', views.secretary_create, name='secretary_create'),
    path('doctor/secretaries/<int:pk>/edit/', views.secretary_edit, name='secretary_edit'),
    path('doctor/secretaries/<int:pk>/delete/', views.secretary_delete, name='secretary_delete'),

    # Patient Management
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),

    # Medicine Management
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/create/', views.medicine_create, name='medicine_create'),
    path('medicines/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('medicines/<int:pk>/delete/', views.medicine_delete, name='medicine_delete'),

    # Examination Management
    path('examinations/', views.examination_list, name='examination_list'),
    path('examinations/create/', views.examination_create, name='examination_create'),
] 
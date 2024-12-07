from django.contrib import admin
from .models import Secretary, Patient, Appointment, Medicine, Examination, Prescription

@admin.register(Secretary)
class SecretaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'phone')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'date_of_birth')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('created_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'time', 'created_by', 'is_cancelled')
    list_filter = ('date', 'is_cancelled')
    search_fields = ('patient__name',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'created_by')
    list_filter = ('date', 'created_by')
    search_fields = ('patient__name', 'symptoms', 'diagnosis')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('examination', 'medicine', 'dosage', 'duration')
    search_fields = ('examination__patient__name', 'medicine__name')

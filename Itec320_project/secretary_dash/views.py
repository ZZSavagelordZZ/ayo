from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.forms import inlineformset_factory
from .models import Patient, Appointment, Secretary, Medicine, Examination, Prescription
from .forms import (
    PatientForm, AppointmentForm, MedicineForm, 
    ExaminationForm, SecretaryCreationForm, PrescriptionForm
)
from datetime import datetime, timedelta

def is_secretary(user):
    return Secretary.objects.filter(user=user).exists()

def is_doctor(user):
    return user.is_superuser

def root_redirect(request):
    if not request.user.is_authenticated:
        return redirect('secretary_dash:login')
    
    if request.user.is_superuser:
        return redirect('secretary_dash:doctor_dashboard')
    
    if is_secretary(request.user):
        return redirect('secretary_dash:secretary_dashboard')
    
    return redirect('secretary_dash:login')

@login_required
def logout_view(request):
    logout(request)
    return redirect('secretary_dash:login')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('secretary_dash:root')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('secretary_dash:root')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'secretary_dash/login.html')

# Common views for both roles
@login_required
@user_passes_test(lambda u: u.is_superuser or is_secretary(u))
def patient_list(request):
    patients = Patient.objects.all()
    template = 'secretary_dash/doctor/patient_list.html' if request.user.is_superuser else 'secretary_dash/secretary/patient_list.html'
    return render(request, template, {'patients': patients})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient created successfully!')
            return redirect('secretary_dash:patient_list')
    else:
        form = PatientForm()
    return render(request, 'secretary_dash/common/patient_form.html', {'form': form})

@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('secretary_dash:patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'secretary_dash/common/patient_form.html', {'form': form})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully!')
        return redirect('secretary_dash:patient_list')
    return render(request, 'secretary_dash/common/patient_confirm_delete.html', {'patient': patient})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    examinations = Examination.objects.filter(patient=patient)
    context = {
        'patient': patient,
        'examinations': examinations
    }
    return render(request, 'secretary_dash/doctor/patient_detail.html', context)

# Appointment Management Views
@login_required
@user_passes_test(lambda u: u.is_superuser or is_secretary(u))
def appointment_list(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    template = 'secretary_dash/doctor/appointment_list.html' if request.user.is_superuser else 'secretary_dash/secretary/appointment_list.html'
    return render(request, template, {'appointments': appointments})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment scheduled successfully!')
            return redirect('secretary_dash:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'secretary_dash/common/appointment_form.html', {'form': form, 'title': 'Schedule New Appointment'})

@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.is_cancelled = True
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
    return redirect('secretary_dash:appointment_list')

# Doctor-specific appointment views
@login_required
@user_passes_test(is_doctor)
def appointment_edit(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully!')
            return redirect('secretary_dash:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'secretary_dash/common/appointment_form.html', {'form': form, 'title': 'Edit Appointment'})

@login_required
@user_passes_test(is_doctor)
def doctor_cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.is_cancelled = True
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
    return redirect('secretary_dash:appointment_list')

# Secretary-specific views
@login_required
@user_passes_test(is_secretary)
def secretary_dashboard(request):
    today = datetime.now().date()
    context = {
        'today_appointments': Appointment.objects.filter(date=today).order_by('time'),
        'upcoming_appointments': Appointment.objects.filter(
            date__gt=today
        ).order_by('date', 'time')[:5]
    }
    return render(request, 'secretary_dash/secretary/dashboard.html', context)

# Additional Secretary Views
@login_required
@user_passes_test(is_doctor)
def secretary_list(request):
    """
    View to list all secretaries.
    Accessible only by doctors.
    """
    secretaries = Secretary.objects.all()
    return render(request, 'secretary_dash/doctor/secretary_list.html', {'secretaries': secretaries})

@login_required
@user_passes_test(is_secretary)
def secretary_create(request):
    if request.method == 'POST':
        form = SecretaryCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Secretary created successfully!')
            return redirect('secretary_dash:secretary_list')
    else:
        form = SecretaryCreationForm()
    return render(request, 'secretary_dash/common/secretary_form.html', {'form': form, 'title': 'Create Secretary'})

@login_required
@user_passes_test(is_secretary)
def secretary_edit(request, pk):
    secretary = get_object_or_404(Secretary, pk=pk)
    if request.method == 'POST':
        form = SecretaryCreationForm(request.POST, instance=secretary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Secretary updated successfully!')
            return redirect('secretary_dash:secretary_list')
    else:
        form = SecretaryCreationForm(instance=secretary)
    return render(request, 'secretary_dash/common/secretary_form.html', {'form': form, 'title': 'Edit Secretary'})

@login_required
@user_passes_test(is_doctor)
def secretary_delete(request, pk):
    secretary = get_object_or_404(Secretary, pk=pk)
    if request.method == 'POST':
        secretary.user.delete()  # This will also delete the secretary due to CASCADE
        messages.success(request, 'Secretary deleted successfully!')
        return redirect('secretary_dash:secretary_list')
    return render(request, 'secretary_dash/common/secretary_confirm_delete.html', {'secretary': secretary})

# Doctor Dashboard View
@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    """
    View for the doctor's dashboard.
    """
    today = datetime.now().date()
    appointments_today = Appointment.objects.filter(date=today).order_by('time')
    upcoming_appointments = Appointment.objects.filter(
        date__gt=today
    ).order_by('date', 'time')[:5]
    
    context = {
        'today_appointments': appointments_today,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'secretary_dash/doctor/dashboard.html', context)

@login_required
@user_passes_test(is_doctor)
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'secretary_dash/doctor/medicine_list.html', {'medicines': medicines})

@login_required
def medicine_create(request):
    """
    View to create a new medicine.
    """
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine created successfully!')
            return redirect('secretary_dash:medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'secretary_dash/doctor/medicine_form.html', {'form': form, 'title': 'Create Medicine'})

@login_required
def medicine_edit(request, pk):
    """
    View to edit an existing medicine.
    """
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine updated successfully!')
            return redirect('secretary_dash:medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'secretary_dash/doctor/medicine_form.html', {'form': form, 'title': 'Edit Medicine'})

@login_required
def medicine_delete(request, pk):
    """
    View to delete an existing medicine.
    """
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        try:
            medicine.delete()
            messages.success(request, 'Medicine deleted successfully!')
        except Exception as e:
            messages.error(request, 'Unable to delete medicine. It may be referenced by other records.')
        return redirect('secretary_dash:medicine_list')
    return render(request, 'secretary_dash/doctor/medicine_confirm_delete.html', {'medicine': medicine})

@login_required
@user_passes_test(is_doctor)
def examination_list(request):
    examinations = Examination.objects.all().order_by('-date', '-time')
    return render(request, 'secretary_dash/doctor/examination_list.html', {'examinations': examinations})

@login_required
def examination_create(request):
    """
    View to create a new examination.
    """
    if request.method == 'POST':
        form = ExaminationForm(request.POST)
        if form.is_valid():
            examination = form.save(commit=False)
            examination.doctor = request.user
            examination.save()
            messages.success(request, 'Examination created successfully!')
            return redirect('secretary_dash:examination_list')
    else:
        form = ExaminationForm()
    return render(request, 'secretary_dash/common/examination_form.html', {'form': form})

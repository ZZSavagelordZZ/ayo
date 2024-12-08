from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Appointment, DoctorBusyHours, Examination, Prescription

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat(),
            }
        )
    )
    
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control',
                'step': '1800'
            }
        )
    )

    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'time']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control select2'})
        }

class DoctorBusyHoursForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat(),
            }
        )
    )
    
    start_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control',
                'step': '1800'
            }
        )
    )
    
    end_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control',
                'step': '1800'
            }
        )
    )

    class Meta:
        model = DoctorBusyHours
        fields = ['date', 'start_time', 'end_time', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Enter the reason for busy hours'
            })
        }

class ExaminationForm(forms.ModelForm):
    class Meta:
        model = Examination
        fields = ['symptoms', 'diagnosis', 'notes']
        widgets = {
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Enter patient symptoms'
            }),
            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Enter diagnosis'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Enter any additional notes'
            })
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicine', 'dosage', 'duration', 'notes']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-control select2'}),
            'dosage': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1 tablet twice daily'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 7 days'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '2',
                'placeholder': 'Additional instructions'
            })
        }

PrescriptionFormSet = forms.inlineformset_factory(
    Examination,
    Prescription,
    form=PrescriptionForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

class SecretaryForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
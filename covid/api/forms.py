from django import forms
from api.models import Doctor, Especialidad, Examen, Medicamento

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'especialidades']

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre']


class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nombre', 'descripcion']

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'descripcion']
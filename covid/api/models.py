# models.py
from django.db import models
from django.contrib.auth.models import User
from centro_medico.api import admin


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medico')
    especialidades = models.ManyToManyField(Especialidad, blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)  # Ej: '11111111-1'
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"


class FichaMedica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='ficha')

    def __str__(self):
        return f"Ficha de {self.paciente}"


class Medicamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Examen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


class Atencion(models.Model):
    ficha = models.ForeignKey(FichaMedica, on_delete=models.CASCADE, related_name='atenciones')
    medico = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='atenciones')
    fecha_atencion = models.DateTimeField(auto_now_add=True)
    anamnesis = models.TextField()
    diagnostico = models.TextField()
    medicamentos = models.ManyToManyField(Medicamento, blank=True, related_name='atenciones')
    examenes = models.ManyToManyField(Examen, blank=True, related_name='atenciones')

    def __str__(self):
        return f"Atención ID: {self.id} - Paciente: {self.ficha.paciente.rut} - Médico: {self.medico}"
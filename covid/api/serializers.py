#serializers
from rest_framework import serializers
from .models import Especialidad, Doctor, Paciente, FichaMedica, Atencion, Medicamento, Examen
from django.contrib.auth.models import User

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ['id', 'nombre', 'descripcion']

class ExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examen
        fields = ['id', 'nombre', 'descripcion']

class DoctorSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    especialidades = EspecialidadSerializer(many=True, read_only=True)
    especialidades_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=Especialidad.objects.all(),
        source='especialidades'
    )
    
    class Meta:
        model = Doctor
        fields = ['id', 'nombre_completo', 'especialidades', 'especialidades_ids']
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name()
    
class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['id', 'rut', 'nombre', 'fecha_nacimiento']

class AtencionSerializer(serializers.ModelSerializer):
    medico = DoctorSerializer(read_only=True)
    medico_id = serializers.PrimaryKeyRelatedField(
        queryset=Doctor.objects.all(),
        write_only=True,
        source='medico'
    )
    medicamentos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Medicamento.objects.all(),
        required=False
    )
    examenes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Examen.objects.all(),
        required=False
    )

    class Meta:
        model = Atencion
        fields = [
            'id', 'fecha_atencion', 'anamnesis', 'diagnostico',
            'medico', 'medico_id', 'medicamentos', 'examenes'
        ]

    def create(self, validated_data):
        return super().create(validated_data)

class FichaMedicaSerializer(serializers.ModelSerializer):
    paciente = PacienteSerializer(read_only=True)
    atenciones = AtencionSerializer(many=True, read_only=True)

    class Meta:
        model = FichaMedica
        fields = ['id', 'paciente', 'atenciones']

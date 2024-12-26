# views.py
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Especialidad, Doctor, Paciente, FichaMedica, Atencion, Medicamento, Examen
from .serializers import EspecialidadSerializer, DoctorSerializer, PacienteSerializer, FichaMedicaSerializer, AtencionSerializer, MedicamentoSerializer, ExamenSerializer
from .permissions import IsAdminUserCustom, IsMedicoUser
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .permissions import IsAdminUserCustom, IsMedicoUser
from api.forms import DoctorForm, EspecialidadForm, ExamenForm, MedicamentoForm

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user',) 


def is_medico_user(user):
    return hasattr(user, 'medico') and not user.is_staff

@login_required
@user_passes_test(is_medico_user)
def medico_dashboard(request):
    return render(request, 'medico/dashboard.html')

@login_required
@user_passes_test(is_medico_user)
def pacientes_atendidos(request):
    atenciones = Atencion.objects.filter(medico=request.user.medico).select_related('ficha', 'ficha__paciente')
    return render(request, 'medico/pacientes_atendidos.html', {'atenciones': atenciones})


@login_required
@user_passes_test(is_medico_user)
def nueva_atencion(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')  # Obtener el RUT del formulario
        anamnesis = request.POST.get('anamnesis')
        diagnostico = request.POST.get('diagnostico')
        medicamentos_ids = request.POST.getlist('medicamentos')
        examenes_ids = request.POST.getlist('examenes')

        # Buscar o crear paciente
        try:
            paciente = Paciente.objects.get(rut=rut)
        except Paciente.DoesNotExist:
            paciente = Paciente.objects.create(rut=rut, nombre="Paciente Desconocido")

        # Buscar o crear ficha médica
        ficha, created = FichaMedica.objects.get_or_create(paciente=paciente)

        # Crear la nueva atención
        atencion = Atencion.objects.create(
            ficha=ficha,
            medico=request.user.medico,
            anamnesis=anamnesis,
            diagnostico=diagnostico
        )
        atencion.medicamentos.set(medicamentos_ids)
        atencion.examenes.set(examenes_ids)
        atencion.save()

        return redirect('detalle_ficha', ficha_id=ficha.id)

    # Pasar medicamentos y exámenes al contexto
    medicamentos = Medicamento.objects.all()
    examenes = Examen.objects.all()  # Asegúrate de que este modelo existe
    return render(request, 'medico/nueva_atencion.html', {
        'medicamentos': medicamentos,
        'examenes': examenes,
    })

@login_required
@user_passes_test(is_medico_user)
def detalle_ficha(request, ficha_id):
    ficha = get_object_or_404(FichaMedica, id=ficha_id)
    return render(request, 'medico/detalle_ficha.html', {'ficha': ficha})

@login_required
@user_passes_test(is_medico_user)
def obtener_ficha_por_rut(request):
    ficha = None
    error = None
    if request.method == 'GET' and 'rut' in request.GET:
        rut = request.GET['rut']
        try:
            ficha = FichaMedica.objects.select_related('paciente').get(paciente__rut=rut)
        except FichaMedica.DoesNotExist:
            error = f"No se encontró ficha médica para el RUT {rut}."
    return render(request, 'medico/ficha_paciente.html', {'ficha': ficha, 'error': error})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Verificar si es administrador
def is_admin_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin_user)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
@user_passes_test(is_admin_user)
def lista_examenes(request):
    examenes = Examen.objects.all()
    return render(request, 'admin/examenes.html', {'examenes': examenes})

@login_required
@user_passes_test(is_admin_user)
def crear_examen(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_examenes')
    else:
        form = ExamenForm()
    return render(request, 'admin/crear_examen.html', {'form': form})

@login_required
@user_passes_test(is_admin_user)
def editar_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            return redirect('lista_examenes')
    else:
        form = ExamenForm(instance=examen)
    return render(request, 'admin/formulario_entidad.html', {
        'accion': 'Editar',
        'titulo_singular': 'Examen',
        'form': form,
        'url_volver': reverse('lista_examenes'),
    })

@login_required
@user_passes_test(is_admin_user)
def borrar_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        examen.delete()
        return redirect('lista_examenes')
    return render(request, 'admin/confirmar_borrar.html', {
        'titulo_singular': 'Examen',
        'objeto': examen.nombre,
        'url_volver': reverse('lista_examenes'),
    })


@login_required
@user_passes_test(is_admin_user)
def lista_especialidades(request):
    especialidades = Especialidad.objects.all()
    return render(request, 'admin/especialidades.html', {'especialidades': especialidades})

@login_required
@user_passes_test(is_admin_user)
def crear_especialidad(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_especialidades')
    else:
        form = EspecialidadForm()
    return render(request, 'admin/crear_especialidad.html', {'form': form})

@login_required
@user_passes_test(is_admin_user)
def editar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            return redirect('lista_especialidades')
    else:
        form = EspecialidadForm(instance=especialidad)
    return render(request, 'admin/formulario_entidad.html', {
        'accion': 'Editar',
        'titulo_singular': 'Especialidad',
        'form': form,
        'url_volver': reverse('lista_especialidades'),
    })

@login_required
@user_passes_test(is_admin_user)
def borrar_especialidad(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk)
    if request.method == 'POST':
        especialidad.delete()
        return redirect('lista_especialidades')
    return render(request, 'admin/confirmar_borrar.html', {
        'titulo_singular': 'Especialidad',
        'objeto': especialidad.nombre,
        'url_volver': reverse('lista_especialidades'),
    })


@login_required
@user_passes_test(is_admin_user)
def lista_doctores(request):
    doctores = Doctor.objects.select_related('user').prefetch_related('especialidades')
    objetos = [
        {
            'valores': [doctor.user.username, 
                        ", ".join([especialidad.nombre for especialidad in doctor.especialidades.all()])],
            'url_editar': reverse('editar_doctor', args=[doctor.id]),
            'url_borrar': reverse('borrar_doctor', args=[doctor.id]),
        }
        for doctor in doctores
    ]
    return render(request, 'admin/lista_entidades.html', {
        'titulo': 'Doctores',
        'titulo_singular': 'Doctor',
        'encabezados': ['Usuario', 'Especialidades'],
        'objetos': objetos,
        'url_crear': reverse('crear_doctor'),
    })

@login_required
@user_passes_test(is_admin_user)
def crear_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_doctores')
    else:
        form = DoctorForm()
    return render(request, 'admin/formulario_entidad.html', {
        'accion': 'Crear',
        'titulo_singular': 'Doctor',
        'form': form,
        'url_volver': reverse('lista_doctores'),
    })

@login_required
@user_passes_test(is_admin_user)
def editar_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('lista_doctores')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'admin/formulario_entidad.html', {
        'accion': 'Editar',
        'titulo_singular': 'Doctor',
        'form': form,
        'url_volver': reverse('lista_doctores'),
    })

@login_required
@user_passes_test(is_admin_user)
def borrar_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('lista_doctores')
    return render(request, 'admin/confirmar_borrar.html', {
        'titulo_singular': 'Doctor',
        'objeto': f"{doctor.user.get_full_name()}",
        'url_volver': reverse('lista_doctores'),
    })


@login_required
@user_passes_test(is_admin_user)
def lista_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    objetos = [
        {
            'valores': [medicamento.nombre, medicamento.descripcion],
            'url_editar': reverse('editar_medicamento', args=[medicamento.id]),
            'url_borrar': reverse('borrar_medicamento', args=[medicamento.id]),
        }
        for medicamento in medicamentos
    ]
    return render(request, 'admin/lista_entidades.html', {
        'titulo': 'Medicamentos',
        'titulo_singular': 'Medicamento',
        'encabezados': ['Nombre', 'Descripción'],
        'objetos': objetos,
        'url_crear': reverse('crear_medicamento'),  # PASANDO LA URL CORRECTA
    })

@login_required
@user_passes_test(is_admin_user)
def crear_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_medicamentos')
    else:
        form = MedicamentoForm()
    return render(request, 'admin/crear_medicamento.html', {'form': form})

@login_required
@user_passes_test(is_admin_user)
def editar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('lista_medicamentos')
    else:
        form = MedicamentoForm(instance=medicamento)
    return render(request, 'admin/formulario_entidad.html', {
        'accion': 'Editar',
        'titulo_singular': 'Medicamento',
        'form': form,
        'url_volver': reverse('lista_medicamentos'),
    })

@login_required
@user_passes_test(is_admin_user)
def borrar_medicamento(request, pk):
    medicamento = get_object_or_404(Medicamento, pk=pk)
    if request.method == 'POST':
        medicamento.delete()
        return redirect('lista_medicamentos')
    return render(request, 'admin/confirmar_borrar.html', {
        'titulo_singular': 'Medicamento',
        'objeto': medicamento.nombre,
        'url_volver': reverse('lista_medicamentos'),
    })

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        # Verificar si el usuario es administrador
        if IsAdminUserCustom().has_permission(self.request, self):
            return '/admin-dashboard/'  # Redirigir a la página de administración

        # Verificar si el usuario es médico
        elif IsMedicoUser().has_permission(self.request, self):
            return '/medico-dashboard/'  # Redirigir al panel del médico

        # Redirigir a una página predeterminada si no pertenece a ninguno
        return '/'

def custom_logout(request):
    logout(request)  # Invalida la sesión activa
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('login')


class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user').prefetch_related('especialidades')
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [IsAuthenticated, IsMedicoUser]

class FichaMedicaViewSet(viewsets.ModelViewSet):
    queryset = FichaMedica.objects.select_related('paciente')
    serializer_class = FichaMedicaSerializer
    permission_classes = [IsAuthenticated, IsMedicoUser]
    
    @action(detail=False, methods=['get'], url_path='por-rut')
    def por_rut(self, request):
        rut = request.query_params.get('rut')
        if rut:
            try:
                ficha = FichaMedica.objects.select_related('paciente').get(paciente__rut=rut)
                serializer = self.get_serializer(ficha)
                return Response(serializer.data)
            except FichaMedica.DoesNotExist:
                return Response({'detail': 'No se encontró la ficha para el RUT especificado.'}, status=404)
        else:
            return Response({'detail': 'Debe proporcionar un RUT como parámetro de consulta.'}, status=404)

class AtencionViewSet(viewsets.ModelViewSet):
    queryset = Atencion.objects.select_related('ficha', 'medico')
    serializer_class = AtencionSerializer
    permission_classes = [IsAuthenticated, IsMedicoUser]

    @action(detail=False, methods=['get'], url_path='filtrar-por-fecha')
    def filtrar_por_fecha(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            atenciones = self.queryset.filter(
                fecha_atencion__date__range=[fecha_inicio, fecha_fin]
            )
            serializer = self.get_serializer(atenciones, many=True)
            return Response(serializer.data)
        return Response(
            {'detail': 'Debe proporcionar los parámetros fecha_inicio y fecha_fin.'},
            status=400
        )

    @action(detail=False, methods=['get'], url_path='pacientes-por-medico')
    def pacientes_por_medico(self, request):
        medico_id = request.query_params.get('medico_id')

        if medico_id:
            atenciones = self.queryset.filter(medico_id=medico_id)
            pacientes = Paciente.objects.filter(
                ficha__atenciones__in=atenciones
            ).distinct()
            serializer = PacienteSerializer(pacientes, many=True)
            return Response(serializer.data)
        return Response(
            {'detail': 'Debe proporcionar el parámetro medico_id.'},
            status=400
        )

    def perform_create(self, serializer):
        ficha_id = self.request.data.get('ficha_id')
        medicamentos_ids = self.request.data.get('medicamentos', [])
        examenes_ids = self.request.data.get('examenes', [])

        if not ficha_id:
            raise ValueError("Se requiere 'ficha_id' para crear una atención.")

        try:
            ficha = FichaMedica.objects.get(id=ficha_id)
        except FichaMedica.DoesNotExist:
            raise ValueError("La ficha con el ID proporcionado no existe.")

        medico = self.request.user.medico
        atencion = serializer.save(medico=medico, ficha=ficha)

        if medicamentos_ids:
            medicamentos = Medicamento.objects.filter(id__in=medicamentos_ids)
            atencion.medicamentos.set(medicamentos)

        if examenes_ids:
            examenes = Examen.objects.filter(id__in=examenes_ids)
            atencion.examenes.set(examenes)

        atencion.save()

class MedicamentoViewSet(viewsets.ModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]

class ExamenViewSet(viewsets.ModelViewSet):
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
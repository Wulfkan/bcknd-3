from django.http import HttpResponseRedirect
from django.urls import path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from api.views import custom_logout, admin_dashboard, dashboard, lista_medicamentos, lista_examenes, CustomLoginView, EspecialidadViewSet, DoctorViewSet, PacienteViewSet, FichaMedicaViewSet, AtencionViewSet, MedicamentoViewSet, ExamenViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls import include
from django.contrib.auth.views import LoginView, LogoutView
from api.views import (
    lista_medicamentos, crear_medicamento, editar_medicamento, borrar_medicamento,
    lista_examenes, crear_examen, editar_examen, borrar_examen,
    lista_especialidades, crear_especialidad, editar_especialidad, borrar_especialidad,
    lista_doctores, crear_doctor, editar_doctor, borrar_doctor, obtener_ficha_por_rut, nueva_atencion, pacientes_atendidos, medico_dashboard, detalle_ficha

)
from django.urls import path


router = DefaultRouter()
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'doctores', DoctorViewSet)
router.register(r'pacientes', PacienteViewSet, basename='pacientes')
router.register(r'fichas', FichaMedicaViewSet, basename='fichas')
router.register(r'atenciones', AtencionViewSet, basename='atenciones')
router.register(r'medicamentos', MedicamentoViewSet, basename='medicamentos')
router.register(r'examenes', ExamenViewSet, basename='examenes')

urlpatterns = [
    path('', lambda request: HttpResponseRedirect('/api/')),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'),
    path('api/', include(router.urls)),
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('medico-dashboard/', medico_dashboard, name='medico_dashboard'),
    path('medico/ficha/', obtener_ficha_por_rut, name='obtener_ficha'),
    path('medico/atencion/nueva/', nueva_atencion, name='nueva_atencion'),
    path('medico/pacientes/', pacientes_atendidos, name='pacientes_atendidos'),

    # Medicamentos
    path('panel-admin/medicamentos/', lista_medicamentos, name='lista_medicamentos'),
    path('panel-admin/medicamentos/crear/', crear_medicamento, name='crear_medicamento'),
    path('panel-admin/medicamentos/editar/<int:pk>/', editar_medicamento, name='editar_medicamento'),
    path('panel-admin/medicamentos/borrar/<int:pk>/', borrar_medicamento, name='borrar_medicamento'),
    
    # Exámenes
    path('panel-admin/examenes/', lista_examenes, name='lista_examenes'),
    path('panel-admin/examenes/crear/', crear_examen, name='crear_examen'),
    path('panel-admin/examenes/editar/<int:pk>/', editar_examen, name='editar_examen'),
    path('panel-admin/examenes/borrar/<int:pk>/', borrar_examen, name='borrar_examen'),
    
    # Especialidades
    path('panel-admin/especialidades/', lista_especialidades, name='lista_especialidades'),
    path('panel-admin/especialidades/crear/', crear_especialidad, name='crear_especialidad'),
    path('panel-admin/especialidades/editar/<int:pk>/', editar_especialidad, name='editar_especialidad'),
    path('panel-admin/especialidades/borrar/<int:pk>/', borrar_especialidad, name='borrar_especialidad'),
    
    # Doctores
    path('panel-admin/doctores/', lista_doctores, name='lista_doctores'),
    path('panel-admin/doctores/crear/', crear_doctor, name='crear_doctor'),
    path('panel-admin/doctores/editar/<int:pk>/', editar_doctor, name='editar_doctor'),
    path('panel-admin/doctores/borrar/<int:pk>/', borrar_doctor, name='borrar_doctor'),
]

from django.urls import path
from . import views
from .views import get_tclass_info, obtener_precio_grupo, InscripcionUpdateView, InscripcionUpdateV,pagos_todos
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register_member/', views.register_member, name='register_member'),
    path('update_member/', views.update_member, name='update_member'),
    path('update_member_admin/<int:id>/', views.update_member_admin, name='update_member_admin'),
    path('delete_member/<int:id>/', views.delete_member, name='delete_member'),
    path('list_members/', views.list_members, name='list_members'),
    
    path('list_instructors/', views.list_instructors, name='list_instructors'),
    path('create_instructor/', views.create_instructor , name='create_instructor'),
    path('update_instructor/<int:id>/', views.update_instructor, name='update_instructor'),

    path('calendar_instructor/', views.calendar_view, name='calendar_inst'),
    path('instructor_schedule/', views.instructor_schedule_view, name='instructor_schedule'),

    path('list_classes/', views.list_classes, name='list_classes'),
    path('create_class/', views.create_class , name='create_class'),
    path('update_class/<int:id>/', views.update_class, name='update_class'),

    path('list_groups/', views.list_group, name='list_groups'),
    path('create_group/', views.create_group , name='create_group'),
    path('update_group/<int:id>/', views.update_group, name='update_group'),
    path('get_tclass_info/', get_tclass_info, name='get_tclass_info'),
    path('obtener_precio_grupo/', obtener_precio_grupo, name='obtener_precio_grupo'),

    path('list_inscribes/', views.list_inscribe, name='list_inscribes'),
    path('create_inscription/', views.inscription_create, name='create_inscription'),

    path('update_inscription/<int:id>/', views.update_class, name='update_class'),

    path('inscripcion/<int:pk>/editar/', InscripcionUpdateView.as_view(), name='inscripcion_edit'),

    path('register_pay/', views.register_pay, name='register_pay'),
    path('inscripcionV/<int:pk>/editar/', InscripcionUpdateV.as_view(), name='inscripcion_editar'),

    path('pagos/', views.pagos_registrados_view, name='lista-pagos'),
    path('pagos/todos', views.pagos_todos , name='lista-pagos-todos'),
    path('pagos/validar/<int:pago_id>/', views.validar_pago, name='validar-pago'),
    path('pagos/invalidar/<int:pago_id>/', views.invalidar_pago, name='invalidar-pago'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MemberRegisterForm, InstructorForm, ClassForm, GroupForm, CalendarForm, InstructorForm1, InscribeForm, PagoForm
from .models import Member, Instructor, Tclass, Grupo, Inscripcion, Pago
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Inscripcion, Grupo
from .forms import InscripcionForm
from django.db import transaction
from django.utils.decorators import method_decorator


@login_required
def register_member(request):
    if hasattr(request.user, 'member'):
        return redirect('update_member')
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            return redirect('home')
    else:
        form = MemberRegisterForm()
    return render(request, 'members/register_member.html', {'form': form})

@login_required
def update_member(request):
    member = get_object_or_404(Member, user=request.user)
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MemberRegisterForm(instance=member)
    return render(request, 'members/update_member.html', {'form': form, 'member': member})

@login_required
def update_member_admin(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        form = MemberRegisterForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('list_members')
    else:
        form = MemberRegisterForm(instance=member)
    return render(request, 'members/update_member_admin.html', {'form': form, 'member': member})

@login_required
def list_members(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    members = Member.objects.all()
    return render(request, 'members/list_members.html', {'members': members})

@login_required
def delete_member(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'POST':
        member.delete()
        return redirect('list_members')
    return render(request, 'members/confirm_delete.html', {'member': member})

@login_required
def list_instructors(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    instructors = Instructor.objects.all()
    return render(request, 'members/list_instructor.html', {'instructors': instructors})

@login_required
def create_instructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_instructors')  # Redirige a la lista de instructores
    else:
        form = InstructorForm()

    return render(request, 'members/create_instructor.html', {'form': form})

@login_required
def update_instructor(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('list_instructors')
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'members/update_instructor.html', {'form': form, 'instructor': instructor})

@login_required
def list_classes(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    classes = Tclass.objects.all()
    return render(request, 'members/list_class.html', {'classes': classes})

@login_required
def create_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            nueva_clase = form.save(commit=False)  # commit=False es clave
            nueva_clase.creo = request.user
            nueva_clase.save()
            return redirect('list_classes')  # Redirige a la lista de clases
    else:
        form = ClassForm()

    return render(request, 'members/create_class.html', {'form': form})

@login_required
def update_class(request, id):
    classe = get_object_or_404(Tclass, id=id)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            return redirect('list_classes')
    else:
        form = ClassForm(instance=classe)
    return render(request, 'members/update_class.html', {'form': form, 'classe': classe})

@login_required
def list_group(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    groups = Grupo.objects.all()
    return render(request, 'members/list_group.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            nuevo_grupo = form.save(commit=False)  # commit=False es clave
            nuevo_grupo.creo = request.user
            nuevo_grupo.save()
            return redirect('list_groups')  # Redirige a la lista de clases
    else:
        form = GroupForm()

    return render(request, 'members/create_group.html', {'form': form})

@login_required
def update_group(request, id):
    group = get_object_or_404(Grupo, id=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('list_groups')
    else:
        form = GroupForm(instance=group)
    return render(request, 'members/update_group.html', {'form': form, 'group': group})

@login_required
def calendar_view(request):
    form = CalendarForm()
    groups = []

    if request.method == 'POST':
        form = CalendarForm(request.POST)
        if form.is_valid():
            instructor = form.cleaned_data['instructor']
            groups = Grupo.objects.filter(instructor=instructor)

    return render(request, 'members/calendar_inst.html', {'form': form, 'groups': groups})

@login_required
def instructor_schedule_view(request):
    form = InstructorForm1()
    schedule = {hour: {day: "" for day in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']} for hour in range(0, 24)}

    if request.method == 'POST':
        form = InstructorForm1(request.POST)
        if form.is_valid():
            instructor = form.cleaned_data['instructor']
            groups = Grupo.objects.filter(instructor=instructor,estatus=True)

            # Rellenar el horario con "X" en las intersecciones
            for group in groups:
                days = group.dias_semana
                print(f'dias_semana: {days}')  # Imprimir el contenido de dias_semana
                start_hour = group.horaInicio.hour
                start_minute = group.horaInicio.minute
                end_hour = group.horaTermino.hour
                end_minute = group.horaTermino.minute

                for day in days:
                    print(f'day: {day}')  # Imprimir el contenido de cada day
                    day_name = day  # Usar directamente el valor de day
                    # Mapeo de abreviaturas a nombres completos de días
                    day_map = {
                        'LU': 'Lunes',
                        'MA': 'Martes',
                        'MI': 'Miércoles',
                        'JU': 'Jueves',
                        'VI': 'Viernes',
                        'SA': 'Sábado',
                        'DO': 'Domingo'
                    }
                    if day_name in day_map:
                        day_name = day_map[day_name]  # Convertir abreviatura a nombre completo

                    for hour in range(start_hour, end_hour + 1):
                        if hour == start_hour:
                            schedule[hour][day_name] = "ocupado"  # Marcar la primera hora completa
                        elif hour == end_hour:
                            if end_minute > 0:
                                schedule[hour][day_name] = "ocupado"  # Marcar la última hora si está parcialmente ocupada
                        else:
                            schedule[hour][day_name] = "ocupado"  # Marcar las horas completas entre la primera y la última

    return render(request, 'members/instructor_schedule.html', {'form': form, 'schedule': schedule})

@login_required
def get_tclass_info(request):
    clase_id = request.GET.get('clase_id')
    
    if not clase_id:
        return JsonResponse({'error': 'No se proporcionó clase_id'}, status=400)
    try:
        clase = get_object_or_404(Tclass, id=clase_id)
        return JsonResponse({
            'minimo': clase.minimo,
            'maximo': clase.maximo,
            'duracion': clase.duracion
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
def obtener_precio_grupo(request):
    grupo_id = request.GET.get('grupo_id')
    if grupo_id:
        grupo = get_object_or_404(Grupo, id=grupo_id)
        return JsonResponse({'preciounitario': grupo.preciounitario})
    return JsonResponse({'error': 'Grupo no encontrado'}, status=400)

@login_required
def list_inscribe(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirigir a la página de inicio si no es superusuario
    inscribes = Inscripcion.objects.all()
    return render(request, 'members/list_inscribe.html', {'inscribes': inscribes})

@login_required
def inscription_create(request):
    user   = request.user
    member = get_object_or_404(Member, user=user)
    inscribes = Inscripcion.objects.filter(member=member)
    hoy = timezone.now().date()
    groups = Grupo.objects.filter(
        estatus=True,
        fec_ini__lt=hoy,
        fec_fin__gte=hoy
    )

    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        messages.error(request, "No puedes inscribirte hasta que completes tus datos como Miembro ")
        return redirect('perfil_update')  # Redirigir a la vista donde el usuario debe completar sus datos

    if request.method == "POST":
        form = InscribeForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.member = member  # Asignar el miembro automáticamente
            inscripcion.preciounitario = inscripcion.grupo.preciounitario  
            inscripcion.preciototal = inscripcion.preciounitario * inscripcion.cantidad  
            inscripcion.creo = user  # Asignar el usuario actual a 'creo'
            inscripcion.save()
            return redirect('create_inscription')
    else:
        form = InscribeForm(initial={'member': member})

    return render(request, 'members/inscripcion_form.html', 
                  {
                      'form': form,
                      'inscribes': inscribes,
                      'grupos': groups
                  } )

class InscripcionUpdateView(UpdateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'inscripcion_form.html'
    success_url = reverse_lazy('inscripcion_list')

@login_required
@transaction.atomic
def register_pay(request):
    user = request.user

    # Obtener el miembro vinculado al usuario
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        messages.error(request, "No puedes registrar pagos hasta completar tu perfil de Miembro.")
        return redirect('perfil_update')

    pagos = Pago.objects.filter(member=member)

    if request.method == "POST":
        form = PagoForm(request.POST, request.FILES)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.member = member
            pago.creo = user  # Si tienes ese campo en el modelo
            pago.genero = 'R'
            pago.save()

            # Actualizar campo pagos_real del miembro
            member.pagos_real += pago.pago
            member.save()

            return redirect('home')
    else:
        form = PagoForm(initial={'fecha_pago': timezone.now()})

    return render(request, 'members/register_pay.html', {
        'form': form,
        'pagos': pagos,
    })

@login_required
def pagos_registrados_view(request):
    pagos = Pago.objects.filter(genero='R').order_by('member', 'fecha_pago')
    return render(request, 'members/lista_pagos.html', 
                  {'pagos': pagos})

@login_required
def pagos_todos(request):
    pagos = Pago.objects.all()
    return render(request, 'members/lista_pagos_todos.html', 
                  {'pagos': pagos})


def invalidar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    pago.genero = 'N'
    pago.save()
    return redirect('lista-pagos')

@transaction.atomic
def validar_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    
    # Cambiar estatus del pago
    pago.genero = 'V'
    pago.save()

    # Actualizar campos del miembro
    member = pago.member
    member.pagos_validado += pago.pago
    member.saldo += pago.pago
    member.save()

    return redirect('lista-pagos')



@method_decorator(login_required, name='dispatch')
class InscripcionUpdateV(UpdateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'members/inscripcion_update.html'

    def form_valid(self, form):
        inscripcion = form.save(commit=False)

        # Obtener valor anterior de pagado
        original = Inscripcion.objects.get(pk=self.object.pk)
        diferencia = inscripcion.pagado - original.pagado

        # Actualizar precio total
        inscripcion.preciototal = inscripcion.cantidad * inscripcion.preciounitario
        inscripcion.save()

        # Actualizar valores del miembro
        miembro = inscripcion.member
        miembro.pagos_usados += diferencia
        miembro.saldo -= diferencia
        miembro.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list_inscribes')  # Ajusta al nombre de tu vista de retorno




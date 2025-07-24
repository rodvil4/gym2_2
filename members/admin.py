from django.contrib import admin

from .models import Member, Instructor, Tclass, Grupo, Inscripcion, Pago

admin.site.register(Member)

admin.site.register(Instructor)

admin.site.register(Tclass)

admin.site.register(Grupo)

admin.site.register(Inscripcion)

admin.site.register(Pago)

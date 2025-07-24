from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Instructor
from .utils import enviar_correo_nuevo_instructor  # Importa tu función

@receiver(post_save, sender=Instructor)
def instructor_guardado(sender, instance, created, **kwargs):
    print("Señal post_save ejecutada. Instructor creado:", instance.nombre) 
    if created:  # Solo envía el correo si se crea un nuevo registro
        enviar_correo_nuevo_instructor(instance)
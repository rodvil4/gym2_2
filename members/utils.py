from django.core.mail import send_mail

def enviar_correo_nuevo_instructor(instructor):
    asunto = 'Nuevo instructor registrado'
    mensaje = f'Se ha registrado un nuevo instructor: {instructor.nombre}'
    correo_remitente = 'rvilchisv@gmail.com'  # Reemplaza con tu correo
    correo_destinatario = ['meland.1424@gmail.com']  # Reemplaza con el correo del destinatario

    send_mail(asunto, mensaje, correo_remitente, correo_destinatario)
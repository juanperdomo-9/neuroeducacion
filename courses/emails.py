from django.conf import settings
import resend

resend.api_key = settings.RESEND_API_KEY


def enviar_mail_aprobado(user, course):

    resend.Emails.send({

        "from": "NeuroEducacion <onboarding@resend.dev>",

        "to": [user.email],

        "subject": "¡Tu curso ya está listo!",

        "html": f"""

        <div style="font-family:sans-serif;padding:40px;">

            <h1 style="color:#4B2E83;">
                ¡Pago aprobado! 🎉
            </h1>

            <p style="font-size:16px;color:#444;">
                Tu compra del curso
                <strong>{course.title}</strong>
                fue aprobada correctamente.
            </p>

            <p style="font-size:16px;color:#444;">
                Ya podés ingresar y comenzar el contenido 😄
            </p>

        </div>

        """
    })


def enviar_mail_transferencia(user, course):

    resend.Emails.send({

        "from": "NeuroEducacion <onboarding@resend.dev>",

        "to": [user.email],

        "subject": "Estamos verificando tu pago",

        "html": f"""

        <div style="font-family:sans-serif;padding:40px;">

            <h1 style="color:#4B2E83;">
                Comprobante recibido 😄
            </h1>

            <p style="font-size:16px;color:#444;">
                Recibimos tu comprobante para el curso
                <strong>{course.title}</strong>.
            </p>

            <p style="font-size:16px;color:#444;">
                Nuestro equipo verificará el pago y
                activará tu acceso a la brevedad.
            </p>

        </div>

        """
    })

resend.api_key = settings.RESEND_API_KEY


def enviar_mail_admin(compra):

    resend.Emails.send({

        "from": "NeuroEducacion <onboarding@resend.dev>",

        "to": [settings.ADMIN_NOTIFICATIONS_EMAIL],

        "subject": f"Nueva compra - {compra.curso.title}",

        "html": f"""

        <div style="font-family:sans-serif;padding:40px;">

            <h1>
                Nueva compra recibida 🎉
            </h1>

            <hr>

            <p><strong>Nombre:</strong> {compra.nombre}</p>

            <p><strong>Apellido:</strong> {compra.apellido}</p>

            <p><strong>Email:</strong> {compra.email}</p>

            <p><strong>DNI:</strong> {compra.dni}</p>

            <p><strong>Curso:</strong> {compra.curso.title}</p>

            <p><strong>Método:</strong> {compra.metodo_pago}</p>

            <p><strong>Estado:</strong> {compra.estado}</p>

        </div>

        """
    })
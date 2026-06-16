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

    pass

resend.api_key = settings.RESEND_API_KEY


def enviar_mail_admin(compra):

    pass
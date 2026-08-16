import logging

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

import resend

logger = logging.getLogger(__name__)


class ResendEmailBackend(BaseEmailBackend):
    """
    Backend de email que envía los mensajes de Django
    (por ejemplo el reset de contraseña) a través de la
    API de Resend, igual que courses/emails.py.
    """

    def send_messages(self, email_messages):

        if not email_messages:
            return 0

        resend.api_key = settings.RESEND_API_KEY

        sent_count = 0

        for message in email_messages:

            payload = {
                "from": "NeuroEducación <onboarding@resend.dev>",
                "to": list(message.to),
                "subject": message.subject,
                "text": message.body,
            }

            for content, mimetype in getattr(message, 'alternatives', []):

                if mimetype == 'text/html':
                    payload["html"] = content
                    break

            try:

                resend.Emails.send(payload)

                sent_count += 1

            except Exception:

                # Nunca se propaga: el flujo de "recuperar
                # contraseña" siempre debe mostrar la pantalla
                # de "revisá tu email" (no revelar si el envío
                # falló, ni romper la vista), aunque Resend
                # esté en modo sandbox o falle por otro motivo.
                logger.exception(
                    "Falló el envío de email a %s (asunto: %s)",
                    payload.get("to"),
                    payload.get("subject"),
                )

        return sent_count

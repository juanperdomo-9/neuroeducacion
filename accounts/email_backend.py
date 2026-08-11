from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

import resend


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

                if not self.fail_silently:
                    raise

        return sent_count

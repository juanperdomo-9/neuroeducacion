import json
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Course, Enrollment, Compra
from .utils import user_has_access


def make_course(**kwargs):

    defaults = dict(
        title='Curso de prueba',
        slug='curso-de-prueba',
        short_description='Descripción de prueba',
        thumbnail='courses/thumbnails/test',
        price=1000,
    )

    defaults.update(kwargs)

    return Course.objects.create(**defaults)


class UserHasAccessTests(TestCase):

    def test_no_access_without_paid_enrollment(self):

        user = User.objects.create_user(
            username='sinacceso',
            password='Pass12345!'
        )

        course = make_course(slug='curso-sin-acceso')

        self.assertFalse(user_has_access(user, course))

    def test_access_with_paid_enrollment(self):

        user = User.objects.create_user(
            username='conacceso',
            password='Pass12345!'
        )

        course = make_course(slug='curso-con-acceso')

        Enrollment.objects.create(
            user=user,
            course=course,
            paid=True
        )

        self.assertTrue(user_has_access(user, course))


class SuccessViewSecurityTests(TestCase):
    """
    Regresión: /success/<slug>/ NO debe otorgar acceso a partir
    de los parámetros de la URL (payment_id/status), porque esos
    los controla el navegador del comprador, no Mercado Pago.
    El único camino válido para inscribir es el webhook.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username='comprador',
            email='comprador@example.com',
            password='Pass12345!'
        )

        self.course = make_course(slug='curso-success')

        self.client = Client()

        self.client.login(
            username='comprador',
            password='Pass12345!'
        )

    def test_spoofed_success_url_does_not_grant_enrollment(self):

        url = reverse('success', args=[self.course.slug])

        response = self.client.get(
            url,
            {
                'payment_id': '999999',
                'status': 'approved',
            }
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Enrollment.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )


class MpWebhookTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='comprador2',
            email='comprador2@example.com',
            password='Pass12345!'
        )

        self.course = make_course(slug='curso-webhook')

        self.client = Client()

    @patch('courses.emails.resend.Emails.send')
    @patch('courses.views.sdk')
    def test_approved_payment_creates_enrollment(self, mock_sdk, mock_send):

        mock_sdk.payment.return_value.get.return_value = {
            'response': {
                'status': 'approved',
                'external_reference': f'{self.user.id}-{self.course.id}',
            }
        }

        url = reverse('mp_webhook')

        payload = {
            'type': 'payment',
            'data': {'id': '123'},
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            Enrollment.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    @patch('courses.views.sdk')
    def test_non_approved_payment_does_not_enroll(self, mock_sdk):

        mock_sdk.payment.return_value.get.return_value = {
            'response': {
                'status': 'rejected',
                'external_reference': f'{self.user.id}-{self.course.id}',
            }
        }

        url = reverse('mp_webhook')

        payload = {
            'type': 'payment',
            'data': {'id': '124'},
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Enrollment.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )


class TransferenciaViewTests(TestCase):
    """
    Regresión: si el envío del email (Resend) falla -por ejemplo
    porque la cuenta está en modo sandbox y no puede mandarle a
    cualquier destinatario- la compra por transferencia no debe
    tirar 500. El comprobante ya se guardó en la base y eso es
    lo que importa; el mail es un extra.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username='transfer',
            email='transfer@example.com',
            password='Pass12345!'
        )

        self.course = make_course(slug='curso-transferencia')

        self.client = Client()

        self.client.login(
            username='transfer',
            password='Pass12345!'
        )

        session = self.client.session

        session['checkout_data'] = {
            'course_id': self.course.id,
            'nombre': 'Juan',
            'apellido': 'Perez',
            'dni': '12345678',
            'email': 'transfer@example.com',
        }

        session.save()

    @patch(
        'courses.emails.resend.Emails.send',
        side_effect=Exception('Resend en modo sandbox')
    )
    def test_falla_de_email_no_rompe_la_compra(self, mock_send):

        response = self.client.post('/transferencia/', {})

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Compra.objects.filter(
                usuario=self.user,
                curso=self.course,
                metodo_pago='transferencia'
            ).exists()
        )


class CheckoutViewTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='yaenrolado',
            email='yaenrolado@example.com',
            password='Pass12345!'
        )

        self.course = make_course(slug='curso-checkout')

        self.client = Client()

        self.client.login(
            username='yaenrolado',
            password='Pass12345!'
        )

    def test_already_enrolled_user_is_redirected_away(self):

        Enrollment.objects.create(
            user=self.user,
            course=self.course,
            paid=True
        )

        url = reverse('checkout', args=[self.course.slug])

        response = self.client.get(url)

        self.assertRedirects(
            response,
            reverse('course_detail', args=[self.course.slug])
        )

    def test_requires_login(self):

        self.client.logout()

        url = reverse('checkout', args=[self.course.slug])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

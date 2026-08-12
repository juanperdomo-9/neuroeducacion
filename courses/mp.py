import os

import mercadopago

from django.conf import settings


sdk = mercadopago.SDK(
    settings.MERCADO_PAGO_ACCESS_TOKEN
)


def crear_preferencia(course, request):

    # SITE_URL se define por variable de entorno (la URL pública
    # real del deploy activo). Sin esto, el webhook y los
    # back_urls de Mercado Pago apuntarían a un dominio que puede
    # no existir más (ya pasó una vez con Railway). En local cae
    # a la URL de la propia request, aunque ahí MP igual no va a
    # poder pegarle al webhook por no ser pública.
    base_url = os.getenv(
        'SITE_URL',
        request.build_absolute_uri('/').rstrip('/')
    )

    preference_data = {

        "items": [
            {
                "title": course.title,
                "quantity": 1,
                "currency_id": "ARS",
                "unit_price": float(course.price),
            }
        ],

        "external_reference": f"{request.user.id}-{course.id}",

        "notification_url": f"{base_url}/webhook/mp/",

        "back_urls": {

            "success": f"{base_url}/success/{course.slug}/",

            "failure": f"{base_url}/checkout/{course.slug}/",

            "pending": f"{base_url}/checkout/{course.slug}/",

        },

    }

    try:

        preference_response = sdk.preference().create(
            preference_data
        )

        preference = preference_response["response"]

        return preference.get("init_point")

    except Exception:

        return None
import mercadopago

from django.conf import settings


sdk = mercadopago.SDK(
    settings.MERCADO_PAGO_ACCESS_TOKEN
)


def crear_preferencia(course, request):

    base_url = "https://TU-URL.ngrok-free.app"

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

    preference_response = sdk.preference().create(
        preference_data
    )

    print(preference_response)

    preference = preference_response["response"]

    return preference.get("init_point")
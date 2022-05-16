#
#
# this is just for generating forms
# reason for separation so for my code will look a little cleaner
#


def generate_flutter_card_form(tx_ref, amount, currency, redirect_url, customer):
    form = {"tx_ref": tx_ref,
            "amount": float(amount),
            "currency": currency,
            "redirect_url": redirect_url,
            "payment_options": "card",
            "customer": customer,
            "customizations": {
                "title": "Pied Piper Payments",
                "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
            }
            }

    return form

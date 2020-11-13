import ssl
import config
import smtplib


def email_people(people_mapping: dict):
    messages = []
    for person, details in people_mapping.items():
        msg = _gen_message(person, details["recipient"])
        messages.append([details["email"], msg])

    _send_email(messages)


def _gen_message(email_name: str, gift_recip_name: str):
    return "Subject: Secret Santa\n\nHi {},\n\n###############\n\nFor Secret Santa, you are giving a gift to {}\n\n###############".format(
        email_name, gift_recip_name
    )


def _get_email_config():
    return (
        config.email["address"],
        config.email["password"],
        config.email["port"],
    )


def _send_email(messages: list):
    # Get config information
    base_addr, password, port = _get_email_config()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(base_addr, password)
        for message in messages:
            print(f"Sending:\n{message[1]}\nto:\n{message[0]}")
            server.sendmail(base_addr, message[0], message[1])

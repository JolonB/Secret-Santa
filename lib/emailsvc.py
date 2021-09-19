import ssl
import config
import smtplib


def email_people(people_mapping: dict):
    messages = []
    for person, details in people_mapping.items():
        msg = _gen_message(person, details["recipient"])
        messages.append([details["email"], msg])

    _send_email(messages)

def send_allocations(allocation_encoded: bytes):
    base_addr, _, _ = _get_email_config()

    allocation_encoded = "Subject: ALLOCATIONS\n\n" + allocation_encoded.decode("utf-8")

    _send_email([[base_addr, allocation_encoded]])

def remove_person(people_mapping: dict, to_remove: str, new_recipient: str, new_gifter: str):
    gifter_email_address = people_mapping[new_gifter]["email"]
    message = _gen_realloc_message(new_gifter, new_recipient, to_remove)

    email_message = [[gifter_email_address, message]]
    _send_email(email_message)


def _gen_message(email_name: str, gift_recip_name: str):
    return "Subject: Secret Santa\n\nHi {},\n\n###############\n\nFor Secret" \
            " Santa, you are giving a gift to {}.\n\n###############".format(
        email_name, gift_recip_name
    )

def _gen_realloc_message(email_name: str, gift_recip_name: str, old_recip_name:str):
    return "Subject: Secret Santa\n\nHi {},\n\n###############\n\nYour previous" \
            " giftee, {}, is no longer playing.\nYou now need to give a gift to" \
            " {}.\n\n###############".format(
        email_name, old_recip_name, gift_recip_name
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
            #print(f"Sending:\n{message[1]}\nto:\n{message[0]}")
            server.sendmail(base_addr, message[0], message[1])

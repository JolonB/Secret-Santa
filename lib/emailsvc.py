import os
import ssl
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config

def load_html_template(filename: str) -> str:
    filepath = os.path.join("email_templates", filename) + ".html"
    with open(filepath, 'r') as file:
        html_data = file.read()
    return html_data

def email_people(people_mapping: dict):
    messages = []
    for person, details in people_mapping.items():
        msg = _gen_message(person, details["recipient"])
        messages.append({"recipient": details["email"], "content": msg})

    _send_email("Secret Santa", messages)


def send_allocations(allocation_encoded: bytes):
    base_addr, _, _ = _get_email_config()

    allocation_encoded = {"text": allocation_encoded.decode("utf-8")}

    _send_email("ALLOCATIONS", [{"recipient": base_addr, "content": allocation_encoded}])


def remove_person(
    people_mapping: dict, to_remove: str, new_recipient: str, new_gifter: str
):
    gifter_email_address = people_mapping[new_gifter]["email"]
    message = _gen_realloc_message(new_gifter, new_recipient, to_remove)

    email_message = [{"recipient": gifter_email_address, "content": message}]
    _send_email("Secret Santa", email_message)


def _gen_message(email_name: str, gift_recip_name: str):
    text = "Hi {},\n\n###############\n\nFor Secret" \
        " Santa, you are giving a gift to {}.\n\n###############\n\n" \
        "{}".format(
            email_name, gift_recip_name, config.gift_ideas,
        )

    html = load_html_template("main")
    if config.gift_ideas:
        ideas = load_html_template("gift_ideas").format(ideas_link=config.gift_ideas)
    else:
        ideas = ""
    if config.budget:
        budget = load_html_template("budget").format(budget_value=config.budget)
    else:
        budget = ""
    html = html.format(email_recipient_name=email_name, gift_recipient_name=gift_recip_name, random_value=random.random(), gift_ideas=ideas, budget_info=budget)

    return {"text": text, "html": html}



def _gen_realloc_message(email_name: str, gift_recip_name: str, old_recip_name: str):
    text = (
        "Hi {},\n\n###############\n\nYour previous"
        " giftee, {}, is no longer playing.\nYou now need to give a gift to"
        " {}.\n\n###############".format(email_name, old_recip_name, gift_recip_name)
    )
    return {"text": text}


def _get_email_config():
    return (
        config.email["address"],
        config.email["password"],
        config.email["port"],
    )


def _send_email(subject, messages: list):
    # Get config information
    base_addr, password, port = _get_email_config()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(base_addr, password)
        for message in messages:
            # print(f"Sending:\n{message[1]}\nto:\n{message[0]}")
            content = message["content"]
            full_msg = MIMEMultipart("alternative")
            full_msg["Subject"] = subject
            full_msg["From"] = base_addr
            full_msg["To"] = message["recipient"]
            text_part = MIMEText(content["text"], "plain")
            full_msg.attach(text_part)
            if "html" in content.keys():
                html_part = MIMEText(content["html"], "html")
                full_msg.attach(html_part)
            server.sendmail(base_addr, message["recipient"], full_msg.as_string())

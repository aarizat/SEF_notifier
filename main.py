from dataclasses import dataclass
import os

from requests import post, get, Response
from bs4 import BeautifulSoup


@dataclass
class MailgunConfig:
    api_key: str
    domain: str


def get_url(url) -> str | None:
    response = get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        img_tag = soup.find(
            name='img',
            attrs={
                'src': 'Images/SemVisto.png',
                'class': 'img-fluid btn Botao'
            }
        )
        link = img_tag.find_parent('a').get("href")
        return link if link != "#" else None
    return None


def send_email(
        config: MailgunConfig,
        from_: str, to: list[str],
        subject: str,
        text: str
    ) -> Response:

    return post(
        url=f"https://api.mailgun.net/v3/{config.domain}.mailgun.org/messages",
        auth=("api", config.api_key),
        data={
            "from": from_,
            "to": to,
            "subject": subject,
            "text": text,
        }
    )


if __name__ == "__main__":
    WEBSITE_URL = 'https://cplp.sef.pt/Registo.aspx'
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
    RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS")

    config = MailgunConfig(MAILGUN_API_KEY, MAILGUN_DOMAIN)

    link = get_url(WEBSITE_URL)
    if link is not None:
        send_email(
            config=config,
            from_="User SEF",
            to=RECIPIENT_EMAILS.split(','),
            subject="SEF: Visto Consular Enabled!",
            text=f"Go to {link} to start Visto Consular proccess. :)"
        )
    else:
        print("Visto Consular option is not enabled yet. :(")

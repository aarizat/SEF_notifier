from dataclasses import dataclass
import os
from urllib.parse import urlparse, urlunparse

from requests import post, get, Response
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


DEFAULT_SCHEME = 'https'
DEFAULT_NETLOC = 'cplp.sef.pt'


@dataclass
class MailgunConfig:
    api_key: str
    domain: str


class MailgunError(Exception):
    """Mailgun exception occurred."""


class UnexpectedError(Exception):
    """Unexpected exception occurred."""


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

    try:
        response = post(
            url=f"https://api.mailgun.net/v3/{config.domain}.mailgun.org/messages",
            auth=("api", config.api_key),
            data={
                "from": from_,
                "to": to,
                "subject": subject,
                "text": text,
            }
        )
        response.raise_for_status()
    except HTTPError as exc:
        raise MailgunError from exc
    except Exception as exc:
        raise UnexpectedError from exc
    else:
        return response


def format_url(url: str) -> str:
    url_comps = urlparse(url)
    if url_comps.scheme and url_comps.netloc:
        return url
    else:
        return urlunparse(
            (
                DEFAULT_SCHEME,
                DEFAULT_NETLOC,
                url_comps.path,
                url_comps.params,
                url_comps.query,
                url_comps.fragment
            )
        )


if __name__ == "__main__":
    WEBSITE_URL = 'https://cplp.sef.pt/Registo.aspx'
    RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS")

    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")

    config = MailgunConfig(MAILGUN_API_KEY, MAILGUN_DOMAIN)

    link = get_url(WEBSITE_URL)
    if link is not None:
        formated_url = format_url(link)
        try:
            response = send_email(
                config=config,
                from_=f"User SEF <mailgun@{MAILGUN_DOMAIN}>",
                to=RECIPIENT_EMAILS.split(','),
                subject="SEF: Visto Consular Enabled!",
                text=f"Go to {formated_url} to start Visto Consular proccess. :)"
            )
        except MailgunError as exc:
            print(f"Mailgun request failed -> {exc.__cause__}")
        except UnexpectedError as exc:
            print(f"Unexpected error occurred -> {exc.__cause__}")
        else:
            print(f"[{response.status_code}]: Email sent successfully!")
    else:
        print("Visto Consular option is not enabled yet. :(")

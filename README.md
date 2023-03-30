# SEF (Serviço de Estrangeiros e Fronteiras): Visto Consular

## Description
In the new SEF website (https://cplp.sef.pt/Registo.aspx) there are currently three options for requesting a
Visto Consular, but one of them isn't enabled yet. The enabled option is what I need. I don't like the idea of going to the website daily to see if that option is enabed. To avoid this tedious task, I decided to automate it, I created a Python Script which goes to the website and look if the option is enabled, if so, an email telling me that the option is enable is sent to me. This script is executed three times per day.

## How does it work ?

The script uses the `requests` library for making a get request to https://cplp.sef.pt/Registo.aspx, then scrapes the web page using `beautifulsoup4` library, look for an HTML image tag whose src='Images/SemVisto.png' and class='img-fluid btn Botao', goes up for its parent, that's a <a> tag and grabs its `href` attribute, if this is a valid url so this means that no-visto Consular option is enabled, and finally sends an email with this link embeded to me, in order to send emails I am using MailGun library. In case there is no link enable in the website so the script only prints a message in the stdout saying that the option is not ready yet. To run the script three times daily I created a github workflow which run on a cron schedule.

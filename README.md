# SEF (Serviço de Estrangeiros e Fronteiras): Visto Consular

## Description

The new SEF website (https://cplp.sef.pt/Registo.aspx) currently offers three options for requesting a Visto Consular, but one of them is not yet enabled. Fortunately, the enabled option is the one I require. However, checking the website daily to see if the option is available is a time-consuming task that I prefer to avoid. To simplify the process, I created a Python script that automates the task. The script checks the website three times a day and sends me an email notification if the option becomes available.

## How does it work ?

The script is designed to streamline the process of checking for the availability of a Visto Consular option on the SEF website. It utilizes the `requests` library to make a GET request to https://cplp.sef.pt/Registo.aspx and the `beautifulsoup4` library to scrape the webpage for a specific HTML image tag. If the tag is found, the script goes up to its parent <a> tag and extracts the `href` attribute. If the attribute contains a valid URL, this means that the Visto Consular option is enabled, and the script sends an email to me with the link embedded using the MailGun library.

If the option is not enabled, the script will simply print a message to the stdout indicating that the option is not ready yet. To ensure that the script runs three times daily, I have created a GitHub workflow that executes on a cron schedule. This approach eliminates the need for manual checking and provides an efficient and automated solution.

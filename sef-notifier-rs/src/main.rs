use reqwest::blocking::Response;
use reqwest::Error;
use scraper::{Html, Selector};
use std::collections::HashMap;
use std::env;
use url::Url;

static DEFAULT_BASE: &str = "https://cplp.sef.pt";

struct MailgunConfig {
    api_key: String,
    domain: String,
}

fn get_embeded_url(url: &str) -> Option<String> {
    let response = reqwest::blocking::get(url).unwrap();

    if response.status().is_success() {
        let body = response.text().unwrap();
        let document = Html::parse_document(&body);
        let selector =
            Selector::parse(r#"img.img-fluid.btn.Botao[src="Images/SemVisto.png"]"#).unwrap();

        if let Some(img) = document.select(&selector).next() {
            let a = img.parent().unwrap();
            if let Some(href) = a.value().as_element().and_then(|el| el.attr("href")) {
                return if href != "#" {
                    Some(href.to_owned())
                } else {
                    None
                };
            } else {
                return None;
            }
        }
    }
    None
}

fn send_email(
    config: MailgunConfig,
    from: &str,
    to: String,
    subject: &str,
    text: String,
) -> Result<Response, Error> {
    let url = format!(
        "https://api.mailgun.net/v3/{domain}.mailgun.org/messages",
        domain = config.domain
    );
    let mut form_data = HashMap::new();
    form_data.insert("from", from);
    form_data.insert("to", &to);
    form_data.insert("subject", subject);
    form_data.insert("text", &text);

    let response = reqwest::blocking::Client::new()
        .post(url)
        .basic_auth("api", Some(config.api_key))
        .form(&form_data)
        .send()
        .unwrap();
    Ok(response)
}

fn format_url(url_string: &str) -> Url {
    let url = Url::parse(url_string);
    match url {
        Ok(u) => u,
        Err(_) => Url::parse(&format!("{}/{}", DEFAULT_BASE, url_string)).unwrap(),
    }
}

fn main() {
    let website_url = "https://cplp.sef.pt/Registo.aspx";
    let recipient_emails = env::var("RECIPIENT_EMAILS").unwrap();

    let config = MailgunConfig {
        api_key: env::var("MAILGUN_API_KEY").unwrap(),
        domain: env::var("MAILGUN_DOMAIN").unwrap(),
    };

    if let Some(link) = get_embeded_url(website_url) {
        let formated_url = format_url(&link);
        let response = send_email(
            config,
            "mailgun@fake.com",
            recipient_emails,
            "SEF: Visto Consular Enabled!",
            format!(
                "Go to {url} to start Visto Consular proccess.",
                url = formated_url.as_str()
            ),
        );
        match response {
            Ok(resp) => {
                if resp.status().is_success() {
                    println!("Email sent successfully!");
                } else {
                    println!(
                        "<{}>: Unexpected error ocurred: {}",
                        resp.status().clone().as_str(),
                        resp.text().unwrap()
                    );
                }
            }
            Err(err) => println!("Error: {}", err),
        }
    } else {
        println!("Link no enabled yet!")
    }
}

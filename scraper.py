import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_email(url):

    try:

        r = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",
            r.text
        )

        if emails:
            return emails[0]

    except:
        pass

    return "Not Found"


def find_contact_page(url):

    try:

        r = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a")

        for link in links:

            href = link.get("href")

            if href:

                if "contact" in href.lower():

                    if href.startswith("http"):
                        return href

                    return url + href

    except:
        pass

    return "Not Found"


def find_leads(service, location, keyword, amount):

    query = f"{service} {location} {keyword}"

    search_url = (
        "https://www.google.com/search?q="
        + query.replace(" ", "+")
    )

    results = []

    try:

        r = requests.get(
            search_url,
            headers=headers
        )

        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.find_all("a")

        websites = []

        for link in links:

            href = link.get("href")

            if href and "http" in href:

                if "google" not in href:

                    clean = href.split("&")[0]
                    clean = clean.replace("/url?q=", "")

                    if clean not in websites:

                        websites.append(clean)

        websites = websites[:int(amount)]

        for site in websites:

            email = extract_email(site)

            contact = find_contact_page(site)

            results.append({

                "business": site.split("//")[-1],

                "website": site,

                "email": email,

                "contact": contact,

                "status": "Ready"

            })

    except:

        pass

    return results
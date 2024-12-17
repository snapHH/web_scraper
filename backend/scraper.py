import requests
from bs4 import BeautifulSoup
import csv

def scrape_jobs(url, output_file):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    job_listings = []

    for job_card in soup.find_all("div", class_="grid--cell fl1"):
        title = job_card.find("h2").get_text(strip=True) if job_card.find("h2") else "N/A"
        company = job_card.find("h3").get_text(strip=True) if job_card.find("h3") else "N/A"
        location = job_card.find("span", class_="fc-black-500").get_text(strip=True) if job_card.find("span", class_="fc-black-500") else "N/A"
        link = job_card.find("a", href=True)["href"] if job_card.find("a", href=True) else "N/A"

        job_listings.append({"Title": title, "Company": company, "Location": location, "Link": link})

    # Write to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Company", "Location", "Link"])
        writer.writeheader()
        writer.writerows(job_listings)

"""
Python Job Listings Scraper
----------------------------
Scrapes job postings from the Fake Python Jobs practice site
(https://realpython.github.io/fake-jobs/) and saves them to a CSV file.

For each job posting it extracts:
    - Job title
    - Company name
    - Location
    - Job detail page URL (the "Apply" link)

Usage:
    python job_scraper.py
"""

import csv
import sys

import requests
from bs4 import BeautifulSoup

URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_FILE = "job_listings.csv"


def fetch_page(url: str) -> str:
    """Download the HTML content of the given URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an error for bad status codes (4xx/5xx)
    return response.text


def parse_jobs(html: str) -> list[dict]:
    """Parse job cards out of the page HTML and return a list of job dicts."""
    soup = BeautifulSoup(html, "html.parser")

    jobs = []
    # Each job posting is a <div class="card">, containing a "card-content"
    # block (title/company/location) and a "card-footer" block (the links).
    job_cards = soup.find_all("div", class_="card")

    for card in job_cards:
        # Use .find() defensively so a missing field doesn't crash the script
        title_tag = card.find("h2", class_="title")
        company_tag = card.find("h3", class_="company")
        location_tag = card.find("p", class_="location")

        # The card footer holds two links: "Learn" and "Apply".
        # The "Apply" link points at the full job detail page.
        apply_tag = card.find("a", string="Apply")

        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        company = company_tag.get_text(strip=True) if company_tag else "N/A"
        location = location_tag.get_text(strip=True) if location_tag else "N/A"
        job_url = apply_tag["href"].strip() if apply_tag and apply_tag.has_attr("href") else "N/A"

        jobs.append(
            {
                "title": title,
                "company": company,
                "location": location,
                "url": job_url,
            }
        )

    return jobs


def save_to_csv(jobs: list[dict], filename: str) -> None:
    """Write the list of job dicts to a CSV file."""
    fieldnames = ["title", "company", "location", "url"]

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)


def main() -> None:
    print(f"Fetching job listings from {URL} ...")
    try:
        html = fetch_page(URL)
    except requests.RequestException as exc:
        print(f"Failed to fetch the page: {exc}", file=sys.stderr)
        sys.exit(1)

    jobs = parse_jobs(html)

    if not jobs:
        print("No job postings were found on the page.")
        return

    save_to_csv(jobs, OUTPUT_FILE)
    print(f"Scraped {len(jobs)} job postings.")
    print(f"Results saved to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()

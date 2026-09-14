# Python Job Listings Scraper

A beginner-friendly Python web scraper that collects job listings from the
Fake Python Jobs practice site (https://realpython.github.io/fake-jobs/)
and saves them to a CSV file.

## Features

- Fetches the job listings page with requests
- Parses the HTML with BeautifulSoup
- Extracts for each job posting: title, company, location, and detail page URL
- Handles missing fields gracefully
- Saves all results to job_listings.csv

## Installation

pip install -r requirements.txt

## Usage

python job_scraper.py

This fetches the page, extracts all job postings, and saves them to job_listings.csv.

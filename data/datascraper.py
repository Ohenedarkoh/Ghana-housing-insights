import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class MeqasaScraper:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.all_data = []

    def fetch_page(self, url):
        """Fetch the HTML content of a page."""
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Failed to retrieve page: {url}. Status code: {response.status_code}")
            return None

    def parse_listing_page(self, html):
        """Parse the HTML content of a listing page and extract property details."""
        soup = BeautifulSoup(html, "html.parser")
        listings = soup.find_all("div", class_="mqs-prop-dt-wrapper")
        return listings

    def extract_listing_details(self, listing):
        """Extract details from a single listing."""
        title = listing.find("h2")
        title = title.text.strip() if title else "Title not found"

        price = listing.find("p", class_="h3")
        price = price.text.strip().replace("Price:", "").strip() if price else "Price not found"

        listing_url = listing.find("a", href=True)
        listing_url = "https://meqasa.com" + listing_url["href"] if listing_url else "URL not found"

        return {
            "Title": title,
            "Price": price,
            "URL": listing_url,
        }

    def scrape_listing_details(self, listing_url):
        """Scrape additional details from an individual listing page."""
        html = self.fetch_page(listing_url)
        if not html:
            return {}

        soup = BeautifulSoup(html, "html.parser")
        details = {}

        table = soup.find("table", class_="table table-hover table-bordered")
        if table:
            rows = table.find_all("tr")

            for row in rows:
                header = row.find("td", style="font-weight: bold;") or row.find("th")
                if header:
                    header_text = header.text.strip()
                    data_cell = header.find_next("td")

                    if data_cell:
                        data_text = data_cell.text.strip()

                        if header_text == "Commission":
                            details["Commission"] = data_text
                        elif header_text == "Bedrooms":
                            details["Bedrooms"] = data_text
                        elif header_text == "Bathrooms":
                            details["Bathrooms"] = data_text
                        elif header_text == "Garage":
                            details["Garage"] = data_text
                        elif header_text == "Furnished":
                            details["Furnished"] = data_text
                        elif header_text == "Area":
                            details["Area"] = data_text
                        elif header_text == "Amenities":
                            amenities = [li.text.strip() for li in data_cell.find_all("li")]
                            details["Amenities"] = ", ".join(amenities)
                        elif header_text == "Address":
                            details["Address"] = data_text
                        elif header_text == "Reference":
                            details["Reference"] = data_text

        description_div = soup.find("div", class_="description")
        if description_div:
            description = description_div.find("p").text.strip()
            details["Description"] = description
        else:
            details["Description"] = "Description not found"

        return details

    def scrape_page(self, page):
        """Scrape a single page of listings."""
        url = f"{self.base_url}?w={page}"
        print(f"Scraping page {page}: {url}")

        html = self.fetch_page(url)
        if not html:
            return

        listings = self.parse_listing_page(html)
        print(f"Found {len(listings)} listings on page {page}")

        for listing in listings:
            listing_data = self.extract_listing_details(listing)

            if listing_data["URL"] != "URL not found":
                additional_details = self.scrape_listing_details(listing_data["URL"])
            else:
                additional_details = {}

            # Combine the data
            listing_data.update(additional_details)
            self.all_data.append(listing_data)

    def scrape_all_pages(self, start_page=1, end_page=5):
        """Scrape all pages from start_page to end_page."""
        for page in range(start_page, end_page + 1):
            self.scrape_page(page)
            time.sleep(2)

    def save_to_csv(self, filename="raw.csv"):
        """Save the scraped data to a CSV file."""
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_csv(f"./data/raw/{filename}", index=False)
            print(f"Data saved to {filename}")
        else:
            print("No data found. CSV file not created.")


# Main function
if __name__ == "__main__":
    base_url = "https://meqasa.com/properties-for-rent-in-ghana"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    scraper = MeqasaScraper(base_url, headers)

    scraper.scrape_all_pages(start_page=1, end_page=2)

    scraper.save_to_csv()
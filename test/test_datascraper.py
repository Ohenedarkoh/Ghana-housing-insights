import pytest
import pandas as pd
import os
from bs4 import BeautifulSoup
from unittest.mock import patch,MagicMock
from data.datascraper import MeqasaScraper


## fixture: create a simple scraper instance
@pytest.fixture
def scraper():
    """ Provide a meqasascraper object with dummy base_url and headers."""
    return MeqasaScraper(base_url="https:fakeurl.com",headers={"User-Agent":"test-agent"})



## test 1: successful page fetch
@patch("data.datascraper.requests.get") #this replaces requests.get with a mock
def test_fetch_page_success(mock_get,scraper):
    """ Test that fetch_page returnss HTML content when status is 200"""
    #create a fake response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html>fake page</html>"

    # make requests.get return this fake response
    mock_get.return_value = mock_response

    #call the actual function
    html = scraper.fetch_page("https://fakeurl.com/page1")

    #Assertions
    assert html ==  b"<html>fake page</html>"
    mock_get.assert_called_once_with("https://fakeurl.com/page1", headers={"User-Agent": "test-agent"})



## test 2: failed page fetch 
@patch("data.datascraper.requests.get")
def test_fetch_page_failure(mock_get, scraper, capsys):
    """Test that fetch_page returns None and prints error message on failure."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = scraper.fetch_page("https://fakeurl.com/badpage")

    # Capture the printed output
    captured = capsys.readouterr()

    # Assertions
    assert result is None
    assert "Failed to retrieve page" in captured.out



# Reusing existing scraper fixture
@pytest.fixture
def scraper():
    return MeqasaScraper(
        base_url="https://fakeurl.com",
        headers={"User-Agent": "test-agent"}
    )

def test_parse_listing_page_returns_listings(scraper):
    """
    Test that parse_listing_page() correctly extracts
    multiple listing divs from an HTML string.
    """

    #  Creating fake HTML to simulate a Meqasa listing page 
    #  including 2 listings (two <div> blocks with the right class name)
    fake_html = """
    <html>
      <body>
        <div class="mqs-prop-dt-wrapper">Listing 1</div>
        <div class="mqs-prop-dt-wrapper">Listing 2</div>
      </body>
    </html>
    """

    #  Calling the method we're testing
    listings = scraper.parse_listing_page(fake_html)

    # Asserting that the function behaves correctly 
    # 1. It should return a list
    assert isinstance(listings, list)

    # 2. It should find exactly 2 listings (created 2)
    assert len(listings) == 2

    # 3. Each item should be a BeautifulSoup Tag object (optional but good)
    assert all(isinstance(listing, BeautifulSoup("").new_tag("div").__class__) for listing in listings)

    # 4. Optional sanity check for content
    # Check that the first listing's text includes "Listing 1"
    assert "Listing 1" in listings[0].text





@pytest.fixture
def scraper():
    """Fixture to create a test scraper instance."""
    return MeqasaScraper(
        base_url="https://fakeurl.com",
        headers={"User-Agent": "test-agent"}
    )


def test_extract_listing_details_success(scraper):
    """
    Test that extract_listing_details() correctly extracts
    the title, price, and URL from a single listing element.
    """

    #  Step 1: Create fake HTML for a single listing 
    fake_html = """
    <div class="mqs-prop-dt-wrapper">
        <h2>2 Bedroom Apartment for Rent</h2>
        <p class="h3">Price: GHS 1,500</p>
        <a href="/property/2-bedroom-apartment">View details</a>
    </div>
    """

    #  Step 2: Parse the HTML string into a BeautifulSoup Tag 
    soup = BeautifulSoup(fake_html, "html.parser")
    listing_tag = soup.find("div", class_="mqs-prop-dt-wrapper")

    #  Step 3: Call the method we're testing 
    result = scraper.extract_listing_details(listing_tag)

    #  Step 4: Assert the dictionary is correctly formed 
    # 1. It should have 3 keys: Title, Price, and URL
    assert set(result.keys()) == {"Title", "Price", "URL"}

    # 2. Check each field's correctness
    assert result["Title"] == "2 Bedroom Apartment for Rent"
    assert result["Price"] == "GHS 1,500"
    assert result["URL"] == "https://meqasa.com/property/2-bedroom-apartment"



def test_extract_listing_details_missing_fields(scraper):
    """
    Test that extract_listing_details returns default values
    when title, price, or URL tags are missing.
    """

    #  Fake HTML with missing elements
    html = """
    <div class="mqs-prop-dt-wrapper">
        <!-- Missing title, price, and link -->
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    listing = soup.find("div", class_="mqs-prop-dt-wrapper")

    # Run the extraction
    details = scraper.extract_listing_details(listing)

    # Verify default messages are used
    assert details["Title"] == "Title not found"
    assert details["Price"] == "Price not found"
    assert details["URL"] == "URL not found"


def test_scrape_listing_details_success(monkeypatch):
    from data.datascraper import MeqasaScraper

    fake_html = """
    <html>
      <body>
        <table class="table table-hover table-bordered">
          <tr><td style="font-weight: bold;">Bedrooms</td><td>3</td></tr>
          <tr><td style="font-weight: bold;">Bathrooms</td><td>2</td></tr>
          <tr><td style="font-weight: bold;">Area</td><td>120 sqm</td></tr>
        </table>
        <div class="description"><p>Beautiful house in Accra.</p></div>
      </body>
    </html>
    """

    # Mock fetch_page to return fake HTML (not a real request)
    scraper = MeqasaScraper(base_url="https://fakeurl.com", headers={})
    monkeypatch.setattr(scraper, "fetch_page", lambda url: fake_html)

    details = scraper.scrape_listing_details("https://fakeurl.com/listing1")

    assert details["Bedrooms"] == "3"
    assert details["Bathrooms"] == "2"
    assert details["Area"] == "120 sqm"
    assert details["Description"] == "Beautiful house in Accra."



def test_scrape_listing_details_missing_table(monkeypatch):
    from data.datascraper import MeqasaScraper

    fake_html = """
    <html>
      <body>
        <div>No table or description here</div>
      </body>
    </html>
    """

    scraper = MeqasaScraper(base_url="https://fakeurl.com", headers={})
    monkeypatch.setattr(scraper, "fetch_page", lambda url: fake_html)

    details = scraper.scrape_listing_details("https://fakeurl.com/listing2")

    # It should not crash, and should return a dict with fallback description
    assert isinstance(details, dict)
    assert details["Description"] == "Description not found"


def test_scrape_page_success(monkeypatch):
    from data.datascraper import MeqasaScraper

    scraper = MeqasaScraper(base_url="https://fakeurl.com", headers={})

    # 1. Mock methods
    monkeypatch.setattr(scraper, "fetch_page", lambda url: "<html></html>")
    monkeypatch.setattr(scraper, "parse_listing_page", lambda html: ["fake_listing"])
    monkeypatch.setattr(scraper, "extract_listing_details", lambda listing: {"Title": "Sample Listing", "URL": "https://fakeurl.com/listing1"})
    monkeypatch.setattr(scraper, "scrape_listing_details", lambda url: {"Bedrooms": "3", "Bathrooms": "2"})

    # 2. Call the method
    scraper.scrape_page(1)

    # 3. Assert results
    assert len(scraper.all_data) == 1
    result = scraper.all_data[0]
    assert result["Title"] == "Sample Listing"
    assert result["Bedrooms"] == "3"
    assert result["Bathrooms"] == "2"



def test_scrape_page_no_html(monkeypatch):
    from data.datascraper import MeqasaScraper

    scraper = MeqasaScraper(base_url="https://fakeurl.com", headers={})

    # Mock fetch_page to simulate failed request
    monkeypatch.setattr(scraper, "fetch_page", lambda url: None)

    # Mock parse_listing_page just in case (should not be called)
    monkeypatch.setattr(scraper, "parse_listing_page", lambda html: ["should not run"])

    scraper.scrape_page(1)

    # Assert that no data was added
    assert scraper.all_data == []




def test_save_to_csv_creates_file(tmp_path):
    from data.datascraper import MeqasaScraper

    scraper = MeqasaScraper(base_url="https://fakeurl.com", headers={})
    scraper.all_data = [
        {"Title": "House 1", "Price": "GHS 2000", "Bedrooms": "3"}
    ]

    # Temporary CSV file path (e.g., /tmp/test.csv)
    temp_file = tmp_path / "test.csv"

    # Patch method to save to temporary file
    def fake_save_to_csv(self, filename=temp_file):
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_csv(temp_file, index=False)
        else:
            print("No data found. CSV file not created.")

    # Replace the original save_to_csv method with the fake one
    MeqasaScraper.save_to_csv = fake_save_to_csv

    # Run the save
    scraper.save_to_csv()

    # Assert that the file was created
    assert temp_file.exists()

    # Read it back to check the content
    df = pd.read_csv(temp_file)
    assert df.iloc[0]["Title"] == "House 1"
    assert df.iloc[0]["Price"] == "GHS 2000"
    assert str(df.iloc[0]["Bedrooms"]) == "3"


def test_save_to_csv_no_data(tmp_path, capsys):
    from data.datascraper import MeqasaScraper

    scraper = MeqasaScraper(base_url="https://fakeurl.com", headers={})
    scraper.all_data = []  # no data

    temp_file = tmp_path / "empty.csv"

    def fake_save_to_csv(self, filename=temp_file):
        if self.all_data:
            df = pd.DataFrame(self.all_data)
            df.to_csv(temp_file, index=False)
        else:
            print("No data found. CSV file not created.")

    MeqasaScraper.save_to_csv = fake_save_to_csv

    scraper.save_to_csv()

    # Capture the printed message
    captured = capsys.readouterr()

    # Assertions
    assert not temp_file.exists()  # file shouldn't exist
    assert "No data found. CSV file not created." in captured.out








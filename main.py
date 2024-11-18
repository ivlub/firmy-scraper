import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import random

class FirmyScraper:
    def __init__(self):
        # Initialize base URL and session with headers
        self.base_url = "https://www.firmy.cz"
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def search_firmy(self, address):
        """
        Search for businesses on Firmy.cz using the given address.
        :param address: The address to search for businesses.
        :return: A list of dictionaries with business information.
        """
        # Replace spaces in the address with "+" for URL encoding
        search_query = address.replace(" ", "+")
        search_url = f"{self.base_url}/?q={search_query}"
        print(f"Searching: {search_url}")
        
        # Make a GET request to the search URL
        response = self.session.get(search_url)
        businesses = []

        # Check if the response is successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            business_entries = soup.find_all("div", class_="premiseBox")

            # Iterate through each business entry to extract information
            for entry in business_entries:
                business = {}
                
                # Extract company name
                name_elem = entry.find("h3").find("a", class_="companyTitle")
                business["Company"] = name_elem.text.strip() if name_elem else "N/A"

                # Extract address
                address_elem = entry.find("a", class_="address")
                business["Address"] = address_elem.text.strip() if address_elem else "N/A"

                # Extract description
                description_elem = entry.find("div", class_="description")
                business["Description"] = description_elem.text.strip() if description_elem else "N/A"

                # Extract link to detail page
                if name_elem and "href" in name_elem.attrs:
                    detail_link = name_elem["href"]
                    # Ensure the URL starts correctly
                    business["Detail_Link"] = detail_link if detail_link.startswith("http") else f"{self.base_url}{detail_link}"
                else:
                    business["Detail_Link"] = "N/A"

                # Append business to the list
                businesses.append(business)

        else:
            print(f"Failed to fetch search results for {address}. HTTP Status: {response.status_code}")

        return businesses

    def fetch_contact_details(self, detail_url):
        """
        Fetch contact details (phone, email, website) from the detail page.
        :param detail_url: The URL of the business detail page.
        :return: A dictionary with contact details.
        """
        response = self.session.get(detail_url)
        contact_details = {"Phone": "N/A", "Email": "N/A", "Website": "N/A"}

        # Check if the response is successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract phone number
            phone_elem = soup.find("div", class_="value detailPhone detailPhonePrimary")
            if phone_elem:
                phone_span = phone_elem.find("span", {"data-dot": "origin-phone-number"})
                if phone_span:
                    # Add an apostrophe before the phone number
                    contact_details["Phone"] = f"'{phone_span.text.strip()}"

            # Extract website
            website_elem = soup.find("a", class_="detailWebUrl")
            if website_elem and "href" in website_elem.attrs:
                raw_website = website_elem["href"]
                if "##" not in raw_website:
                    contact_details["Website"] = raw_website

            # Extract email
            email_elem = soup.find("a", href=lambda x: x and x.startswith("mailto:"))
            contact_details["Email"] = email_elem["href"].replace("mailto:", "") if email_elem else "N/A"

        else:
            print(f"Failed to fetch details from {detail_url}. HTTP Status: {response.status_code}")

        return contact_details


def main():
    # Initialize the scraper
    scraper = FirmyScraper()

    try:
        # Read addresses from file
        with open("places.txt", "r", encoding="utf-8") as file:
            addresses = [line.strip() for line in file if line.strip()]

        print(f"Found {len(addresses)} addresses to process")

        all_businesses = []

        # Loop through each address
        for index, address in enumerate(addresses, 1):
            print(f"\nProcessing address {index}/{len(addresses)}: {address}")

            # Scrape businesses for the address
            businesses = scraper.search_firmy(address)

            for business in businesses:
                # Add the original address to each business entry
                business["Original_Address"] = address

                # Fetch contact details from the detail page
                if business["Detail_Link"] != "N/A":
                    contact_details = scraper.fetch_contact_details(business["Detail_Link"])
                    business.update(contact_details)

                # Add the business to the results list
                all_businesses.append(business)

            print(f"Found {len(businesses)} businesses at this address")

            # Add a delay to avoid being flagged as a bot
            sleep(random.uniform(2, 4))

        if all_businesses:
            # Create a DataFrame from the results
            df = pd.DataFrame(all_businesses)

            # Reorder columns for clarity
            columns_order = ["Original_Address", "Company", "Address", "Description", "Phone", "Email", "Website", "Detail_Link"]
            df = df.reindex(columns=columns_order)

            # Export the data to an Excel file
            output_file = "output.xlsx"
            df.to_excel(output_file, index=False)

            print("\nProcessing Summary:")
            print(f"Total addresses processed: {len(addresses)}")
            print(f"Total businesses found: {len(df)}")
            print(f"Results exported to: {output_file}")

        else:
            print("\nNo results were found to export")

    except FileNotFoundError:
        print("Error: places.txt file not found!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

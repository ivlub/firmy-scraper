
# Firmy.cz Business Scraper

A Python-based web scraper to extract business details (company name, address, description, phone number, email, and website) from [Firmy.cz](https://www.firmy.cz). This script allows you to input a list of addresses and retrieve relevant business information, exporting the results to an Excel file.

---

## Features

- **Search businesses by address:** Automatically scrape business listings for specified locations.
- **Extract detailed information:** Fetch company details such as name, address, phone number, email, and website.
- **Export results to Excel:** Save all data in an organized Excel file for easy analysis.
- **Avoid bot detection:** Randomized delays are included between requests.

---

## Requirements

Before running the script, make sure you have the following installed:

- Python 3.7 or later
- The required dependencies (see [Installation](#installation))

---

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/ivlub/firmy-scraper.git
   cd firmy-scraper
   ```

2. **Install dependencies**:
   Use the provided `requirements.txt` file to install the necessary Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare input file**:
   Create a `places.txt` file in the project directory. Each line in the file should contain one address. For example:
   ```
   Karlovo náměstí 293/13
   Resslova 293/11
   Dittrichova 1543/2
   ```

---

## Usage

1. **Run the scraper**:
   ```bash
   python scraper.py
   ```

2. **Output**:
   - The script will read addresses from `places.txt`, scrape the business details from Firmy.cz, and save the results in an Excel file named `output.xlsx`.
   - A summary of processed addresses and businesses will be printed in the terminal.

---

## Output File Structure

The output Excel file will have the following columns:
- `Original_Address`: The input address used for the search.
- `Company`: The name of the business.
- `Address`: The address of the business.
- `Description`: A brief description of the business.
- `Phone`: The business's phone number (with an apostrophe to ensure correct formatting).
- `Email`: The business's email address.
- `Website`: The business's website URL.
- `Detail_Link`: The link to the business's detail page on Firmy.cz.

---

## Example Output

| Original_Address | Company              | Address          | Description       | Phone        | Email           | Website             | Detail_Link                          |
|-------------------|----------------------|------------------|-------------------|--------------|-----------------|---------------------|---------------------------------------|
| Prague            | Example Company     | Some Address 123 | Example Business  | '1234567890  | info@example.cz | https://example.com | https://www.firmy.cz/example-company |

---

## Notes

- Ensure your input file `places.txt` is formatted correctly, with one address per line.
- The script uses a random delay between requests to avoid being flagged as a bot.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Contributing

Feel free to fork this repository and submit pull requests with improvements or bug fixes!

---

## Acknowledgements

- This project uses the following libraries:
  - [Requests](https://docs.python-requests.org)
  - [BeautifulSoup](https://beautiful-soup-4.readthedocs.io)
  - [Pandas](https://pandas.pydata.org)
  - [OpenPyxl](https://openpyxl.readthedocs.io)

---

Happy scraping! 🚀

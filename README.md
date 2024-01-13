# SiteLink Web Scraper

This Python script is designed to scrape rental property data from the [Site](https://realtylink.org) website. It utilizes the Selenium library for web automation to collect information about rental properties, including their links, titles, regions, addresses, prices, descriptions, update dates, and images.

## Features

- **Web Scraping:** Extracts unique links from the website, collecting basic information about rental properties.
- **Pagination:** Utilizes pagination to navigate through multiple pages of rental listings.
- **Additional Details:** Retrieves additional details for each rental property, including descriptions, update dates, and image links.
- **Data Storage:** Stores the collected data in a JSON file (`data_website.json`).

## Usage

1. Run the script with `python script_name.py`.

*Note: Make sure to replace `link_scraper.py` with the actual name of your Python script.*

## Dependencies

- [Selenium](https://www.selenium.dev/)
- [Chrome WebDriver](https://sites.google.com/chromium.org/driver/)

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Selenium Documentation](https://www.selenium.dev/documentation/en/)

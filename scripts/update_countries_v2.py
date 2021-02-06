import os
from covid_updater.scraping import get_country_scraper


ISO_CODES = ["IT"]#['AT', 'IN', 'SE', 'US', 'BE', 'BR', 'CZ', 'DE', 'IT']
OUTPUT_PATH = os.path.join("data", "countries")


def main():
    for iso_code in ISO_CODES:
        print(iso_code)
        scraper = get_country_scraper(iso_code=iso_code)
        output_file = os.path.join(OUTPUT_PATH, f"{scraper.filename}2.csv")
        scraper.run(output_file=output_file)


if __name__ == "__main__":
    main()
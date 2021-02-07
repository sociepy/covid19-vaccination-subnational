from covid_updater.scraping import get_country_scraper


def main():
    scraper = get_country_scraper(iso_code="NO")
    output_file = f"data/countries/{scraper.filename}.csv"
    scraper.run(output_file=output_file)


if __name__ == "__main__":
    main()
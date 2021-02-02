from covid_updater.scraping.sweden import SwedenScraper


def main():
    scraper = SwedenScraper()
    output_file = f"data/countries/{scraper.filename}.csv"
    scraper.run(output_file=output_file)


if __name__ == "__main__":
    main()
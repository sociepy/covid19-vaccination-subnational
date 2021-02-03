from covid_updater.scraping import AustriaScraper


def main():
    scraper = AustriaScraper()
    output_file = f"data/countries/{scraper.filename}.csv"
    scraper.run(output_file=output_file)


if __name__ == "__main__":
    main()
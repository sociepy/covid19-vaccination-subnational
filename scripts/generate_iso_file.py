"""
File obtained from: https://www.ip2location.com/downloads/ip2location-iso3166-2.zip

License Agreement
=================

This works is licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

It is free for personal or commercial use with attribution required by mentioning the use of this works as follows: 
This site or product includes IP2Location™ ISO 3166-2 Subdivision Code which available from https://www.ip2location.com.
"""
import pandas as pd


def main():
    df_iso = pd.read_csv("scripts/countries/input/IP2LOCATION-ISO3166-2.CSV")
    df_iso = df_iso.rename(columns={
        "country_code": "location_iso",
        "code": "region_iso"
    })
    # Change names
    iso_replace = {
        "Friuli-Venezia Giulia": "Friuli Venezia Giulia",
        "Brussels Hoofdstedelijk Gewest": "Brussels"
    }
    df_iso.loc[:, "subdivision_name"] = df_iso.loc[:, "subdivision_name"].replace(iso_replace)

    # Add new elements
    new_items = [
        ["IT", "IT-TN", "Provincia autonoma di Trento"],
        ["IT", "IT-BZ", "Provincia autonoma di Bolzano - Alto Adige"],
        ["FR", "FR-RE", "La Reunion"],
        ["FR", "FR-YT", "Mayotte"],
        ["BE", "BE-VLG", "Flanders"],
        ["BE", "BE-WAL", "Wallonia"],
        ["US", "US-AS", "American Samoa"],
        ["US", "US-GU", "Guam"],
        ["US", "US-VI", "Virgin Islands"],
        ["US", "US-MP", "Northern Mariana Islands"],
        ["FR", "FR-MQ", "Martinique"],
        ["FR", "FR-GP", "Guadeloupe"],
        ["FR", "FR-GF", "Guyane"],
        ["NO", "NO-46", "Vestland"],
        ["NO", "NO-42", "Agder"],
        ["NO", "NO-30", "Viken"],
        ["NO", "NO-54", "Troms og Finnmark"],
        ["NO", "NO-50", "Trondelag"],
        ["NO", "NO-38", "Vestfold og Telemark"],
        ["NO", "NO-34", "Innlandet"],
        ["CL", "CL-NB", "Nuble"]
    ]
    new_items = pd.DataFrame(new_items, columns=["location_iso", "region_iso", "subdivision_name"])
    df_iso = df_iso.append(new_items, ignore_index=True)
    df_iso = df_iso.sort_values(["location_iso", "region_iso"])
    df_iso.to_csv("scripts/countries/input/ISO_3166_2.csv", index=False)


if __name__ == "__main__":
    main()
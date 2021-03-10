# -*- coding: utf-8 -*-
"""Generate ISO files."""


from covid_updater.iso import ISODB


def main():
    #  Load DB
    db = ISODB.create_from_source()

    # Renaming
    iso_rename = {
        "Friuli-Venezia Giulia": "Friuli Venezia Giulia",
        "Brussels Hoofdstedelijk Gewest": "Brussels",
        "Saha, Respublika": "Sakha, Respublika",
    }

    #  Add new entries
    items = [
        ["IT", "IT-TN", "Provincia autonoma di Trento"],
        ["IT", "IT-BZ", "Provincia autonoma di Bolzano - Alto Adige"],
        ["FR", "FR-RE", "La Reunion"],
        ["FR", "FR-YT", "Mayotte"],
        ["BE", "BE-VLG", "Flanders"],
        ["BE", "BE-WAL", "Wallonia"],
        ["US", "US-PR", "Puerto Rico"],
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
        ["CL", "CL-NB", "Nuble"],
        ["IN", "IN-LA", "Ladakh"],
        ["FI", "FI-01", "Aland"],
        ["KR", "KR-50", "Sejong-teukbyeoljachisi"],
    ]

    db.rename_values("subdivision_name", iso_rename)
    db.append(items)


if __name__ == "__main__":
    main()

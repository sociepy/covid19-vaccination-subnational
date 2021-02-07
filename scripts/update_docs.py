import argparse
import pandas as pd


def get_parser():
    parser = argparse.ArgumentParser(description="Merge all country data into single csv file.")
    parser.add_argument(
        "input_country_info_path",
        type=str,
        help="Path to country info file.",
        default="data/vaccination.csv"
    )
    parser.add_argument(
        "input_readme_template_path",
        type=str,
        help="Path to README template file.",
        default="data/vaccination.csv"
    )
    parser.add_argument(
        "output_readme_path",
        type=str,
        help="Path to to-be-generated README.",
        default="data/population.csv"
    )
    args = parser.parse_args()
    return parser


def update_readme(input_template, output_path, data_folder):
    files = [f for f in os.listdir(data_folder) if f.endswith(f".csv")]
    for f in files:
        df = pd.read_csv(os.path.join(data_folder, f)

# Tracking
update_country_tracking(
    country=country,
    country_iso=country_iso,
    url=data_url_reference,
    last_update=last_update,
    second_dose=second_dose
)

# Update readme
generate_readme(output_file=os.path.join(project_dir, "README.md"))
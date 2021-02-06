import pandas as pd


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
# Narada Class of 2026: University Destinations Dashboard

[View the Live Dashboard →](https://narada-university-dashboard.streamlit.app/)

## Project Overview

An interactive data analysis and visualization dashboard showcasing the post-graduation destinations of the Narada School Class of 2026.

This project collects destination and admissions data through a Google Form, processes and standardizes the responses using Python, and generates a dataset presented through an interactive Streamlit dashboard featuring maps, charts, and statistics.

## Features

- Automated data processing cleaning pipeline
- Configurable schema and value mappings
- Alias system for standardizing the names of institutions and majors
- Campus name normalization and inference
- Automated institution and geocoding data generation
- Manual geocoding overrides for ambiguous destinations
- Dataset validation
- Interactive and responsive Streamlit dashboard:
  - Interactive world map
  - University, country/region, and academic field charts and statistics
  - Admissions and scholarship charts and statistics

## Project Structure

```text
narada-university-dashboard/
│
├── aliases/                 # Alias generation and processing
├── cleaning/                # Data cleaning pipeline
├── common/                  # Shared pipeline and data utilities
├── config/                  # Project configuration and reference settings
├── dashboard/               # Streamlit dashboard
│   ├── assets/              # Dashboard styles
│   ├── data/                # Dashboard data loading and transformations
│   ├── pages/               # Dashboard pages
│   ├── ui/                  # Reusable UI components
│   └── visualization/       # Charts, maps, and visualization functions
├── data/                    # Project data
│   ├── processed/           # Processed datasets
│   ├── raw/                 # Google Forms export (not tracked)
│   └── reference/           # Reference and mapping data
├── geocoding/               # Institution geocoding pipeline
├── institutions/            # Institution data generation
├── scripts/                 # Command-line entry points
│
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

## Data Pipeline

```text
Google Forms
      │
      ▼
Raw CSV Export
      │
      ▼
Data Processing
      │
      ├── Schema and value normalization
      ├── Default values
      ├── Text and campus normalization
      ├── Academic field normalization
      ├── Alias application
      └── Dataset validation
      │
      ▼
Processed Dataset
      │
      ├── Institution data
      └── Student data
      │
      ▼
Geocoding
      │
      ▼
Streamlit Dashboard
```

## Installation

Clone the repository:

```bash
git clone https://github.com/devinlin89/narada-university-dashboard.git
cd narada-university-dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

### Windows (Powershell)

```powershell
.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Getting Started

> [!IMPORTANT]
> This repository intentionally **does not** include the original Google Forms export because it contains personally identifiable information.
>
> Contributors must obtain the latest survey export from a project maintainer or enter own survey data export before running the data cleaning pipeline.

### Step 1: Obtain the latest survey data

Request the latest Google Forms CSV export from a project maintainer.

Place the CSV file inside:

```text
data/raw/
```

The filename should match the one configured in:

```text
config/settings.yaml
```

### Step 2: Process the dataset

Run:

```bash
python -m scripts.process_data
```

The processing pipeline will:

- Load the raw survey export
- Apply the configured schema
- Normalize configured values
- Convert list responses
- Apply default values
- Normalize free-response text
- Normalize campus names
- Normalize academic fields
- Infer campus names where possible
- Apply existing aliases
- Sort the processed dataset
- Validate and export the processed data

The resulting datasets are written to:

```text
data/processed/
```

### 3. Review new aliases

When new institutions or other supported values appear in the dataset, they may need to be added to the project's alias tables.

After running the command in step 2, new aliases are written to:

```text
data/reference/todo/
```

Review each TODO file and provide the appropriate canonical value for each row.

For example:

| Alias | Canonical                             |
| ----- | ------------------------------------- |
| MIT   | Massachusetts Institute of Technology |
| ITB   | Institut Teknologi Bandung            |
| UI    | Universitas Indonesia                 |

### 4. Apply reviewed aliases

Once the TODO files have been reviewed, apply it to the main reference tables:

```bash
python -m scripts.apply_aliases
```

The process validates the TODO files, merges the aliases into the reference tables, sorts the resulting tables, and removes the processed TODO files.

### 5. Re-process the dataset

Run:

```bash
python -m scripts.process_data
```

This applies the newly added aliases to the dataset.

If additional aliases are discovered, repeat the alias review and processing steps until no new aliases remain.

## Geocoding

Institution destinations are geocoded using the project's geocoding pipeline.

Run:

```bash
python -m scripts.geocode
```

Known ambiguous or exceptional destinations can be handled through the manual overrides configured in:

```text
data/reference/geocoding/overrides.yaml
```

This allows specific institution and campus combinations to be assigned a known geographic destination without modifying the general geocoding logic.

## Running the Streamlit Dashboard

Once the processed and supporting datasets have been generated, launch the Streamlit dashboard with:

```bash
streamlit run dashboard/Overview.py
```

## Streamlit Dashboard

The dashboard is intended to provide an accessible overview of the destinations and academic pathways represented by the graduating class.

It presents the data through several complementary views, including geographic maps, university and country/region distributions, academic fields, and admissions statistics.

The dashboard currently includes:

- **Overview**: Summary statistics, destination distribution, and key insights
- **World Map**: Geographic visualization of university destinations
- **Universities**:  University and campus statistics
- **Countries/Regions**: Destination statistics by country/region
- **Majors**: Academic field and major statistics
- **Admissions**: Application, acceptance, and scholarship statistics
- **About**: Information about the dashboard, project, and technology used

## Technology

The project is built primarily with Python and uses:

- *Pandas*: Data processing and cleaning
- *Plotly*: Interactive charts and maps
- *Streamlit*: Dashboard interface
- *Geopy*: Geocoding
- *pycountry*: Country/region lists and flags
- *PyYAML*: Configuration and reference data
- *titlecase*: Text normalization

## Privacy

This repository intentionally excludes the original Google Forms export because it contains personally identifiable information.

The raw survey responses are not tracked or distributed with the project. The processed datasets included in the repository are intended to contain only the anonymized information necessary for the dashboard.

Contributors must obtain the latest survey export separately before running the data processing pipeline.

## Credits

### Developers

- **[Devin Lin](https://github.com/devinlin89)** - Lead Developer (Pandas data processing pipeline, dashboard design and development, data visualization, and project maintenance)

- **[Therius Aaron Chen](https://github.com/Aaronchenboy)** - Dashboard Developer (Streamlit frontend, map visualizations, and major-specific features)

### Special Thanks

- **Catherine Aurelia Wang**
- **Evelyn**
- **Justin Veda Dharmaja**
- **Kendric Keane**

### Acknowledgement

We would like to thank the **Narada School Class of 2026** for contributing their university destination and admissions information to this project. Their participation made this dashboard possible and allowed it to provide a collective snapshot of the destinations and academic pathways represented by our graduating class.

The data presented in this dashboard has been anonymized and processed for visualization and analysis. Original survey responses containing personally identifiable information are not distributed as part of this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

The original survey responses and any other personal data are **not** included in this license and are **not** distributed as part of this repository.
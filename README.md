# Narada Class of 2026: University Destinations Dashboard

## Project Overview

An interactive data analysis and visualization dashboard showcasing the post-graduation destinations of the Narada School Class of 2026.

This project collects destination data through a Google Form, cleans and standardizes the responses using Python, and generates a dataset presented through an interactive Streamlit dashboard featuring maps, charts, and statistics.

## Features

- Automated data cleaning pipeline
- Configurable schema and value mappings
- Alias system for standardizing universities, cities, and majors
- Campus name normalization
- Dataset validation
- Interactive dashboard (in development)

## Project Structure

```text
narada-university-dashboard/
│
├── config/                 # Project configuration
├── data/
│   ├── processed/          # Cleaned datasets
│   ├── raw/                # Google Forms export (not tracked)
│   └── reference/          # Alias tables
│       └── todo/           # Alias review files
│
├── scripts/               # ETL scripts
├── utils/                 # Shared helper functions
├── dashboard/             # Streamlit dashboard (future)
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
Data Cleaning
      │
      ▼
Processed Dataset
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
> This repository intentionally **does not include the original Google Forms export** because it contains personally identifiable information.
>
> Contributors must obtain the latest survey export from a project maintainer before running the data cleaning pipeline.

### Step 1: Obtain the latest survey data

Request the latest Google Forms CSV export from a project maintainer.

Place the CSV file inside:

```text
data/raw/
```

The filename should match the one configured in:

```text
config/paths.py
```

### Step 2: Run the data cleaning pipeline

Execute:

```bash
python -m scripts.clean_data
```

This initial run will:

- Load the raw survey export
- Apply all existing cleaning rules
- Apply the current alias tables
- Validate the dataset
- Export a cleaned dataset to `data/processed`

### Step 3: Generate alias TODO files

Run the alias generation script for each supported alias category:

```bash
python -m scripts.generate_aliases institution
```

Supported categories include:

- `institution`
- `city`
- `major`

If unknown values are found, TODO files will be created in:

```text
data/reference/todo/
```

### Step 4: Complete the TODO alias files

Open each generated TODO file in:

```text
data/reference/todo/
```

Each file contains newly discovered aliases that are not yet present in the project's reference alias table.

For every alias:

1. Determine the correct canonical value.
2. Enter the canonical value in the **canonical** column.
3. Verify that every alias maps to the intended canonical value.

For example:

| Alias | Canonical |
|--------|-----------|
| MIT | Massachusetts Institute of Technology |
| ITB | Institut Teknologi Bandung |
| UI | Universitas Indonesia |

Before proceeding, ensure that:

- Every row has a canonical value.
- Aliases are mapped consistently with the existing reference table.
- There are no duplicate or conflicting mappings.

### Step 5: Merge reviewed aliases

Once a TODO file has been reviewed, merge it into the reference alias table.

```bash
python -m scripts.apply_aliases institution
```

The script will automatically:

- Validate the TODO file
- Merge the aliases into the reference table
- Sort the alias table
- Delete the processed TODO file

Repeat this process for every alias category that contains a TODO file.

### Step 6: Re-run the data cleaning pipeline

Run the cleaning pipeline again.

```bash
python -m scripts.clean_data
```

This second run applies the newly added aliases, producing a fully standardized dataset.

If additional TODO alias files are generated, repeat **Steps 3-6** until no new aliases remain.

### Step 7: Verify the output

The data cleaning process is complete when:

- The cleaning script finishes without errors
- No TODO alias files remain
- The processed dataset has been exported successfully
- Dataset validation passes

## Streamlit Dashboard

The processed dataset serves as the data source for the interactive Streamlit dashboard.

Planned features include:

- University destination statistics
- Interactive world map
- Admission statistics

## Privacy

This repository intentionally excludes all raw survey responses because they contain personally identifiable information.

Only the source code, configuration files, processed datasets, and reference data are publicly available.

Contributors must obtain the latest Google Forms export separately before running the data cleaning pipeline.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

The original survey responses and any other personal data are **not** included in this license and are not distributed as part of this repository.
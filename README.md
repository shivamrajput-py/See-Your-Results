# See Your Results - DTU

A Streamlit-based academic dashboard for Delhi Technological University students.

Live app: [dturesults.streamlit.app](https://dturesults.streamlit.app/)

This project helps DTU students:
- check results using roll number
- view academic performance analysis
- compare university-wise and branch-wise ranks
- explore placement statistics
- access study resources
- calculate SGPA
- download a report-card style PDF summary

The goal of the project is simple: take scattered academic and placement data, structure it properly, and present it in a clean, usable, student-friendly interface.

## Why This Exists

This project was built to make DTU academic data easier to access and understand.

Instead of manually scanning PDFs or scattered sources, students can:
- search for their result quickly
- understand rank and percentile position
- see performance trends in a visual way
- explore placement outcomes branch-wise
- access study material from one place

Behind the scenes, the project parses official-style result PDFs, structures large CSV/JSON datasets, computes rankings and analysis, and exposes everything through a Streamlit app.

## Highlights

- Result check by roll number
- Detailed academic analysis with charts and metrics
- University-wise and branch-wise rankings
- Percentile and top-gainer insights
- Placement statistics for multiple years
- SGPA calculator
- Downloadable report card PDF
- Study material and previous-year-question access

## Scale And Context

This project was built around real DTU academic data workflows and has already been used by thousands of students.

The work behind it includes:
- parsing 80+ to 100+ result PDFs
- structuring tens of thousands of rows of academic data
- generating ranked CSV/JSON datasets
- computing CGPA, percentile, rank progression, and improvement metrics
- visualizing results using Streamlit and Plotly

## Tech Stack

### App Layer
- Python
- Streamlit
- Custom HTML/CSS inside Streamlit
- `streamlit-option-menu`
- `streamlit-lottie`

### Data And Analytics
- Pandas
- CSV / JSON
- Plotly Express
- Python standard library utilities

### Extraction And Preparation
- `pdfplumber` for parsing result PDFs
- Selenium for scraping rank and placement sources

### Export
- ReportLab for PDF report-card generation

## Architecture

The repository is organized in practical layers:

### 1. Application Layer
This is the Streamlit interface students use.

Main production entrypoint:
- [1_STUDENT_PROFILE.py](./1_STUDENT_PROFILE.py)

Responsibilities:
- search and display student result data
- render academic analysis and ranking insights
- render placement charts
- expose study-resource navigation
- generate and download report cards

Supporting files:
- [MainConstant.py](./MainConstant.py): branch mappings, grade-point maps, text templates, and fixed lookup dictionaries
- [style.css](./style.css): custom styling layered onto Streamlit
- [.streamlit/config.toml](./.streamlit/config.toml): theme and server configuration

### 2. Data Extraction And Analysis Layer
This layer prepares the data consumed by the app.

Folder:
- [Extracting_Result_Data](./Extracting_Result_Data/)

Core scripts:
- [ResultExtract_Formator.py](./Extracting_Result_Data/ResultExtract_Formator.py)
  - parses result PDFs using `pdfplumber`
  - extracts semester-wise student result records
  - merges semester data
  - writes structured CSV/JSON outputs

- [Rank&Analysis_Formator.py](./Extracting_Result_Data/Rank&Analysis_Formator.py)
  - creates university-wise ranked files
  - creates branch-wise ranked files
  - creates top-gainers files
  - prepares analysis-friendly ranking datasets

- [placementStats_Scrape.py](./Extracting_Result_Data/placementStats_Scrape.py)
  - scrapes placement-related data from external sources
  - stores yearly placement CSVs

- [scrape_2026.py](./Extracting_Result_Data/scrape_2026.py)
  - scrapes ranking/result views for 2026-specific data preparation

### 3. Data Assets
These are the prepared files the app reads directly.

Inside `Extracting_Result_Data`:
- `ranked_results_csv/`
  - university-wise ranked files
  - branch-wise ranked files
  - merged semester datasets
  - gainers datasets
  - intermediate JSON exports

- `placement_data/`
  - average package CSVs
  - highest package CSVs
  - placed percentage CSVs
  - placement spreadsheet files

- `result_data_pdf/`
  - source PDF result sheets used for extraction

- `StudyMaterialData/`
  - subject/semester/branch mappings
  - study material links
  - PYQ, notes, playlists, assignments, and books metadata

### 4. Assets And Workspace Support
- [animation](./animation/): Lottie animation JSON files used in UI
- [.devcontainer](./.devcontainer/): reproducible development container setup
- [SYR TEST](./SYR%20TEST/): supplemental development workspace with split-page experiments and local copies of app assets

## Repository Structure

```text
See-Your-Results/
├─ 1_STUDENT_PROFILE.py
├─ MainConstant.py
├─ style.css
├─ requirements.txt
├─ README.md
├─ .streamlit/
├─ .devcontainer/
├─ animation/
├─ Extracting_Result_Data/
│  ├─ placementStats_Scrape.py
│  ├─ Rank&Analysis_Formator.py
│  ├─ ResultExtract_Formator.py
│  ├─ scrape_2026.py
│  ├─ placement_data/
│  ├─ ranked_results_csv/
│  ├─ result_data_pdf/
│  └─ StudyMaterialData/
└─ SYR TEST/
```

## Important Files

### Production App
- [1_STUDENT_PROFILE.py](./1_STUDENT_PROFILE.py)
  - the main production Streamlit app
  - contains profile view, rankings, placements, study resources, SGPA calculator, about section, and report-card generation

### Constants And Mapping
- [MainConstant.py](./MainConstant.py)
  - grade-point mapping
  - branch code mappings for different batches
  - placement branch-name mapping
  - percentile/rank message templates
  - roll-number normalization support for 2028 data

### UI Styling
- [style.css](./style.css)
  - custom visual styling
  - button styling
  - spacing and layout adjustments
  - Streamlit chrome hiding

### Dependencies
- [requirements.txt](./requirements.txt)
  - Python packages required for the app and data pipeline

## How The Data Flow Works

1. Result PDFs are collected in `Extracting_Result_Data/result_data_pdf/`.
2. `ResultExtract_Formator.py` parses those PDFs into structured JSON/CSV.
3. `Rank&Analysis_Formator.py` computes university and branch rankings plus gainers.
4. Placement scripts prepare yearly placement CSVs.
5. Study material JSON files map branches, semesters, subjects, and resources.
6. The Streamlit app reads these prepared assets and renders the interface.

## Running Locally

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the app

```powershell
streamlit run 1_STUDENT_PROFILE.py
```

The app will usually open on:

```text
http://localhost:8501
```

## Dev Container

This repository includes a devcontainer setup:
- Python 3.11 base image
- dependency installation during setup
- Streamlit app launch after attach

Main file:
- [.devcontainer/devcontainer.json](./.devcontainer/devcontainer.json)

## Deployment

The project is deployed publicly on Streamlit:
- [dturesults.streamlit.app](https://dturesults.streamlit.app/)

Because the live app reads local structured files from the repository, production safety matters:
- data files should stay consistent with the app’s expected schema
- ranking CSV/JSON outputs should be regenerated carefully
- UI changes in the main app should be validated before deployment

## Notes On Maintenance

When updating academic data:
- add or update source PDFs
- run the extraction/formatting scripts
- verify ranked outputs and branch-wise files
- verify roll-number normalization for affected batches
- test search, rank, placement, and report-card flows in Streamlit

When updating placement data:
- refresh the scraped CSVs
- verify branch names and column names remain consistent
- check charts for all three supported placement years

When updating study material:
- update `DATA_MAIN1.json` for branch/semester/subject mapping
- update `DATA_MAIN2.json` for actual resource links

## Project Strengths

- solves a real student problem
- built end-to-end: data extraction, transformation, analytics, visualization, and delivery
- practical stack with low deployment friction
- already validated by real student usage
- easy to extend with more batches, semesters, and features

## Future Scope

Possible future improvements:
- deeper modularization of the production app
- automated validation checks for CSV/JSON schema changes
- better separation between UI, analysis logic, and file access
- more historical batches and semester data
- admin tooling for refreshing data
- improved tests for critical data and search flows

## Credits

Built and maintained by Shivam Rajput.

Feedback, fixes, and suggestions are welcome.


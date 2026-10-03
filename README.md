# Argentina Transport Data

I built this project to practice web scraping and data analysis with public vehicle registration data from Argentina.

The idea came from a freelance project related to freight transport. I started by exploring the available sources, then built a Python script to download a CSV, filter semitrailer registrations, and generate a summary by province.

## What it does

- Finds CSV download links on the source page using BeautifulSoup.
- Downloads the first CSV found using Requests.
- Filters semitrailer registrations with Pandas.
- Saves the filtered records in SQLite.
- Groups records by the holder's province.
- Checks that the summary total matches the filtered record count.
- Exports the summary to CSV.

The program also handles request errors and closes the database connection after the database operations.

## Tools used

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite

## Project files

- `scraper.py`: finds CSV links and downloads the data.
- `main.py`: runs the download, filtering, database queries, and report export.
- `requirements.txt`: lists the required Python packages.
- `.gitignore`: excludes the virtual environment and generated files.

## Installation

Clone the repository:

```bash
git clone https://github.com/aktechmx/argentina-transport-data.git
cd argentina-transport-data
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

SQLite is included with Python, so it does not need a separate installation.

## How to run

From the project folder, run:

```bash
python main.py
```

This downloads the CSV and runs the analysis.

To run only the download:

```bash
python scraper.py
```

An internet connection is required to access the source and download the file.

## Generated files

The program saves these files in the working directory:

- The downloaded CSV, keeping the filename from its URL.
- `transport_data.db`, with the `semitrailer_registrations` table.
- `semitrailer_registrations_by_province.csv`, with the province summary.

Each run replaces the analysis table. The summary CSV is overwritten when validation succeeds. A downloaded file with the same name is also overwritten.

## Filters

The analysis includes these vehicle types:

- `SEMIRREMOLQUE`
- `SEMIRREMOLQUE BITREN T`
- `SEMIRREMOLQUE BITREN D`

The province summary uses `titular_domicilio_provincia`, which describes the holder's address. It does not indicate where the vehicle operates.

## Results from the August 2026 file

The filtered data contained 721 records:

| Vehicle type | Records |
|---|---:|
| SEMIRREMOLQUE | 649 |
| SEMIRREMOLQUE BITREN T | 36 |
| SEMIRREMOLQUE BITREN D | 36 |
| **Total** | **721** |

These records were distributed across 23 provinces and jurisdictions. The largest counts were:

| Holder's province | Records |
|---|---:|
| C.AUTONOMA DE BS.AS | 160 |
| BUENOS AIRES | 129 |
| CORDOBA | 85 |
| SANTA FE | 62 |
| MENDOZA | 36 |

Results may change when the source publishes a different file.

## Data source and limitations

Source: [DNRPA initial vehicle registrations — Argentina Ministry of Justice](https://datos.jus.gob.ar/dataset/inscripciones-iniciales-de-autos).

The source lists the dataset under a Creative Commons Attribution 4.0 license.

This dataset contains initial registration records. It does not include license plates or CUIT identifiers, so this project cannot determine:

- The number of unique active semitrailers.
- The number of unique owners or CUITs.
- A holder's current tax status in ARCA.

During the initial review, I found 22 rows identical to earlier rows. I kept them because, without a unique vehicle identifier, matching fields are not enough to confirm that they represent the same vehicle.

The current scraper selects the first CSV link it finds. It does not compare dates to determine which file is the latest.

## What I practiced

This project helped me connect several steps into one workflow: finding a download link in HTML, downloading a file, filtering data with Pandas, querying SQLite, and exporting a validated report.

I also worked on separating the code into functions, passing results between modules, and handling request failures.
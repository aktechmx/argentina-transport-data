"""Find and download DNRPA vehicle registration data."""
import requests
from bs4 import BeautifulSoup


SOURCE_URL = (
    "https://datos.jus.gob.ar/dataset/"
    "inscripciones-iniciales-de-autos"
)


def download_csv(csv_url):
    """Download CSV and return its local filename."""

    csv_response = requests.get(csv_url, timeout=30)
    csv_response.raise_for_status()
    file_name = csv_url.rsplit("/", 1)[-1]

    with open(file_name, "wb") as file:
        file.write(csv_response.content)

    return file_name

def find_csv_links(source_url):
    """Find CSV Links on the source page."""

    request = requests.get(source_url, timeout=30)
    request.raise_for_status()
    soup = BeautifulSoup(request.text, "html.parser")
    links = soup.find_all("a", href=True)

    csv_links = []

    for link in links:
        href = link["href"]

        if href.lower().endswith(".csv"):
            csv_links.append(href)
    return csv_links


def main():
    """Find and download CSV files from the source page."""

    csv_links = find_csv_links(SOURCE_URL)

    if csv_links:
        csv_get_url = csv_links[0]
        print(f"CSV encontrado: {csv_get_url}")

        downloaded_file = download_csv(csv_get_url)
        print(f"Archivo guardado: {downloaded_file}")
    else:
        print("No se encontraron archivos CSV en la página fuente.")

if __name__ == "__main__":
    main()

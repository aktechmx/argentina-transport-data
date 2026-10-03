"""Analyze semitrailer registrations in Argentina."""
import sqlite3 as sql
import pandas as pd
import requests

from scraper import SOURCE_URL, find_csv_links, download_csv


def conn_db():
    """Return a connection to the SQLite database."""
    conn = sql.connect("transport_data.db")
    return conn


def load_vehicles(file_path):
    """Load vehicle registrations from a CSV file."""
    vehicles_df = pd.read_csv(file_path)
    return vehicles_df


def filter_semitrailers(vehicles_df):
    """Return semitrailer registration rows."""
    semitrailer_types = [
        "SEMIRREMOLQUE",
        "SEMIRREMOLQUE BITREN T",
        "SEMIRREMOLQUE BITREN D",
    ]

    semitrailer_df = vehicles_df[
        vehicles_df["automotor_tipo_descripcion"].isin(semitrailer_types)
    ]

    return semitrailer_df


def get_province_summary(connection):
    """Return registration counts by holder province."""
    rows = connection.execute("""
        SELECT titular_domicilio_provincia, COUNT(*) AS cantidad
        FROM semitrailer_registrations
        GROUP BY titular_domicilio_provincia
        ORDER BY cantidad DESC
    """).fetchall()

    return rows


def main():
    """Run the registration analysis."""
    try:
        links = find_csv_links(SOURCE_URL)
        if not links:
            print("No se encontraron archivos CSV en la página fuente.")
            return

        downloaded_file = download_csv(links[0])
    except requests.RequestException as e:
        print(f"Error al descargar el archivo CSV: {e}")
        return

    vehicles_df = load_vehicles(downloaded_file)
    semitrailer_df = filter_semitrailers(vehicles_df)

    connection = conn_db()

    try:
        semitrailer_df.to_sql(
            name="semitrailer_registrations",
            con=connection,
            if_exists="replace",
            index=False,
        )

        titular_dom_provincia = get_province_summary(connection)
    except sql.Error as e:
        print(f"Error al guardar los datos en la base de datos: {e}")
        return
    finally:
        connection.close()

    province_summary_df = pd.DataFrame(
        titular_dom_provincia,
        columns=["provincia", "cantidad"],
    )

    summary_total = province_summary_df["cantidad"].sum()

    if summary_total == len(semitrailer_df):
        province_summary_df.to_csv(
            "semitrailer_registrations_by_province.csv",
            encoding="utf-8",
            index=False,
        )
        print("Resumen validado y exportado")
    else:
        print(
            f"Error: el resumen suma {summary_total}, "
            f"pero se esperaban {len(semitrailer_df)} registros."
        )

    for provincia, cantidad in titular_dom_provincia:
        print(
            f"Provincia: {provincia}, "
            f"Cantidad de registros: {cantidad}"
        )


if __name__ == "__main__":
    main()

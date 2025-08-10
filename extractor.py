import csv
import logging
from collections.abc import Iterable
from pathlib import Path

from bs4 import BeautifulSoup

from settings import EXTRACT_DIR, RAW_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_header(soup: BeautifulSoup) -> list[str]:
    header = soup.find(id="booksHeader")
    return [th["alt"] for th in header.find_all("th")]


def extract_body(soup: BeautifulSoup) -> list[list[str]]:
    body = soup.find(id="booksBody")
    rows = []
    for tr in body.find_all("tr"):
        row = []
        for td in tr.find_all("td"):
            td.label.decompose()
            text = td.get_text(strip=True)
            row.append(text)
        rows.append(row)
    return rows


def write_csv(rows: Iterable, file: Path) -> None:
    """Write to CSV file.

    Create file and parent directories if they do not exist.
    """
    logger.info(f"Writing to {file}...")

    file.parent.mkdir(exist_ok=True, parents=True)

    with file.open(mode="w+") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def extract() -> None:
    files = RAW_DIR.iterdir()
    for input_file in files:
        logger.info(f"Extracting {input_file}...")
        html = input_file.read_text()
        soup = BeautifulSoup(html, "html.parser")
        header = extract_header(soup)
        body = extract_body(soup)
        output_file = EXTRACT_DIR / f"{input_file.stem}.csv"
        write_csv(rows=[header, *body], file=output_file)


if __name__ == "__main__":
    extract()

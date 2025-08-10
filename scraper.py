import logging
import os
import re
from pathlib import Path
from typing import Any

import yaml

# Need to set Chromium version before importing requests-html. Default version used by
# Pyppeteer is no longer available.
os.environ["PYPPETEER_CHROMIUM_REVISION"] = "1465706"

from requests_html import HTMLSession

READ_BOOKS_URL = "https://www.goodreads.com/review/list/{user_id}?shelf=read"

USERS_FILE = Path("goodreads_users.yml")

DATA_ROOT = Path("data")
RAW_DIR = DATA_ROOT / "raw"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_yaml(file: Path) -> Any:
    """Read contents of yaml file."""
    with file.open() as f:
        return yaml.safe_load(f)


def scrape_webpage(session: HTMLSession, url: str) -> str:
    """Scrape text from a webpage."""
    logger.info(f"Scraping {url}...")
    result = session.get(url)
    result.html.render()
    return result.text


def write(string: str, file: Path) -> None:
    """Write to file.

    Create file and parent directories if they do not exist.
    """
    logger.info(f"Writing to {file}...")

    file.parent.mkdir(exist_ok=True, parents=True)

    with file.open(mode="w+", encoding="utf-8") as f:
        f.write(string)


def scrape_read_books() -> None:
    """Scrape the "read" shelf for all users from config file."""
    users = read_yaml(USERS_FILE)

    session = HTMLSession()

    for user in users:
        url = READ_BOOKS_URL.format(user_id=user["id"])
        file_name = re.sub(pattern=r"\s+", repl="_", string=user["name"].lower())
        file = RAW_DIR / f"{file_name}.html"
        content = scrape_webpage(session=session, url=url)
        write(string=content, file=file)

    session.close()

    logger.info("Done!")


if __name__ == "__main__":
    scrape_read_books()

import os

# Need to set Chromium version before importing requests-html. Default version used by
# Pyppeteer is no longer available.
os.environ["PYPPETEER_CHROMIUM_REVISION"] = "1465706"

from dotenv import load_dotenv
from requests_html import HTMLSession

load_dotenv()

user = os.environ["GOODREADS_USERNAME"]
password = os.environ["GOODREADS_PASSWORD"]

session = HTMLSession()
result = session.get("https://www.goodreads.com/review/list/162626986?shelf=read")
result.html.render()
print(result.text)
session.close()

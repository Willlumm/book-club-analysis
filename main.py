import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

user = os.environ["GOODREADS_USERNAME"]
password = os.environ["GOODREADS_PASSWORD"]


print(user)
# raw = requests.get("https://www.goodreads.com/review/list/162626986?shelf=read")
# print(raw.status_code)
# print(raw.text)

# https://stackoverflow.com/questions/68697683/struggling-to-log-in-to-goodreads-using-requests-session-what-is-missing-in-my
if not os.path.exists("GoodReads"):
    os.makedirs("Goodreads")


# utf8 and n are other inputs I noticed while inspecting the log in form so I added them and the values in the case they affected anything... they do not seem to
payload = {"user[email]": user, "user[password]": password, "utf8": "✓", "n": "843936"}

with requests.Session() as sess:
    # The code for this is found here https://stackoverflow.com/a/57231791/5395546
    res = sess.get("https://www.goodreads.com/user/sign_in?source=home")
    signin = BeautifulSoup(res._content, "html.parser")
    payload["authenticity_token"] = signin.find(
        "input",
        attrs={"name": "authenticity_token", "type": "hidden"},
    )["value"]
    res = sess.post("https://www.goodreads.com/user/sign_in?source=home", data=payload)
    print(res.text)

    # This section is to print out the titles of the books on the page. It is printing the titles of the books on page 1, not 2, so I know it's not signing in properly.
    r = sess.get("https://www.goodreads.com/shelf/show/fantasy?page=2")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("a", class_="bookTitle")
    print(results)

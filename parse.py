import requests
from bs4 import BeautifulSoup

policyfile = open("policy.json", "r")
policy = policyfile.read()
policyfile.close()

allowedext = policy.replace("\n", '').replace(" ", '').replace('"', '').replace('[', '').replace(']', '').split(',')

parsedextensions = """# Allowed Extensions

|Name|Description|
|-|-|"""

for i in allowedext:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        response = requests.get(f"https://chromewebstore.google.com/detail/{i}", headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('title').get_text().replace(" - Chrome Web Store", "").replace("|", "\|")
        if title == "Chrome Web Store":
            title = "Not found"
        desc = soup.find('meta', property="og:description").get('content').replace("\n", "").replace("-", "").replace("*", "").replace("|", "\|").replace("Add new features to your browser and personalize your browsing experience.", "-")
        print(title,desc)
        parsedextensions=parsedextensions+f"\n|[{title}](https://chromewebstore.google.com/detail/{i})|{desc}|"
    except:
        parsedextensions=parsedextensions+f"\n|Doesn't exist||"

open("README.md", "w").write(parsedextensions)

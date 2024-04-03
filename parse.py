import requests
from bs4 import BeautifulSoup
from py_markdown_table.markdown_table import markdown_table

policyfile = open("policy.json", "r")
policy = policyfile.read()
policyfile.close()

allowedext = policy.replace("\n", '').replace(" ", '').replace('"', '').replace('[', '').replace(']', '').split(',')

parsedextensions = []

for i in allowedext:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }
        response = requests.get(f"https://chromewebstore.google.com/detail/{i}", headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('meta', property="og:title").get('content')
        desc = soup.find('meta', property="og:description").get('content')
        print(title,desc)
        parsedextensions.append({"Name": f"[{title}](https://chromewebstore.google.com/detail/{i})", "Description": desc})
    except:
        parsedextensions.append({"Name": f"Doesn't Exist", "Description": ""})

open("ALLOWEDEXTENSIONS.md", "w").write(markdown_table(parsedextensions).get_markdown().replace("```", ""))

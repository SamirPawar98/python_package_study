import requests
import os

repo = os.environ["REPO"]
token = os.environ["GH_TOKEN"]

headers = {"Authorization": f"Bearer {token}"}

releases = requests.get(
    f"https://api.github.com/repos/{repo}/releases",
    headers=headers,
).json()

os.makedirs("dist", exist_ok=True)

for rel in releases:
    for asset in rel.get("assets", []):
        if asset["name"].endswith(".whl"):
            url = asset["browser_download_url"]
            print("Downloading:", url)
            r = requests.get(url, headers=headers)
            with open(os.path.join("dist", asset["name"]), "wb") as f:
                f.write(r.content)

print("All wheels downloaded.")

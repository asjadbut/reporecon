import json
import re
import os

platform_files = {
    "bugcrowd": "bugcrowd_data.json",
    "hackerone": "hackerone_data.json",
    "intigriti": "intigriti_data.json",
    "yeswehack": "yeswehack_data.json"
}

# match github/gitlab repos even with extra paths
repo_regex = re.compile(
    r"(https?://)?(github\.com|gitlab\.com|bitbucket\.org|sr\.ht|gitea\.com)/([^/\s]+)/([^/\s]+)",
    re.I
)

results = []

for platform, file in platform_files.items():

    if not os.path.exists(file):
        continue

    with open(file) as f:
        data = json.load(f)

    for program in data:

        program_name = program.get("name")
        program_url = program.get("url") or program.get("program_url")

        for scope in program.get("scope", []):

            target = scope.get("target", "").strip()

            match = repo_regex.search(target)

            if match:

                repo_url = f"https://{match.group(2)}/{match.group(3)}/{match.group(4)}"

                results.append({
                    "platform": platform,
                    "program": program_name,
                    "program_url": program_url,
                    "repo": repo_url
                })

# remove duplicates
unique = {item["repo"]: item for item in results}

os.makedirs("data", exist_ok=True)

with open("data/repos.json", "w") as f:
    json.dump(list(unique.values()), f, indent=2)

print(f"Extracted {len(unique)} repositories")
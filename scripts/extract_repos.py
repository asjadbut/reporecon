import json
import re
import os

platform_files = {
    "bugcrowd": "bugcrowd_data.json",
    "hackerone": "hackerone_data.json",
    "intigriti": "intigriti_data.json",
    "yeswehack": "yeswehack_data.json"
}

repo_regex = re.compile(
    r"https?://(github\.com|gitlab\.com|bitbucket\.org|sr\.ht|gitea\.com)/[^/\s]+/[^/\s]+",
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

            target = scope.get("target", "")
            match = repo_regex.search(target)

            if match:

                results.append({
                    "platform": platform,
                    "program": program_name,
                    "program_url": program_url,
                    "repo": match.group()
                })

os.makedirs("data", exist_ok=True)

with open("data/repos.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Extracted {len(results)} repositories")
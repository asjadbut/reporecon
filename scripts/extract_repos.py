import json
import re
import os
from urllib.parse import urlparse

# -------------------------------
# Configuration
# -------------------------------
platform_files = {
    "bugcrowd": "bounty-targets-data/data/bugcrowd_data.json",
    "hackerone": "bounty-targets-data/data/hackerone_data.json",
    "intigriti": "bounty-targets-data/data/intigriti_data.json",
    "yeswehack": "bounty-targets-data/data/yeswehack_data.json"
}

# Regex to match GitHub, GitLab, Bitbucket, SourceHut, Gitea repos/orgs
repo_regex = re.compile(
    r"(https?://)?(github\.com|gitlab\.com|bitbucket\.org|sr\.ht|gitea\.com)/([^\s/]+)(/[^\s]+)?",
    re.I
)

results = []

# -------------------------------
# Main Extraction
# -------------------------------
for platform, file in platform_files.items():
    if not os.path.exists(file):
        print(f"File not found: {file}")
        continue

    with open(file, encoding="utf-8") as f:
        data = json.load(f)

    for program in data:
        program_name = program.get("name")
        program_url = program.get("url")

        targets_obj = program.get("targets", {})
        in_scope_list = targets_obj.get("in_scope", [])

        for scope in in_scope_list:
            # Universal field extraction
            target = (
                scope.get("target") or
                scope.get("asset_identifier") or
                scope.get("endpoint") or
                ""
            ).strip()

            if not target:
                continue

            match = repo_regex.search(target)
            if match:
                host = match.group(2).lower()
                org = match.group(3)
                repo_path = match.group(4) or ""
                # Clean repo name if present
                repo_name = repo_path.lstrip("/") if repo_path else ""

                repo_url = f"https://{host}/{org}{('/' + repo_name) if repo_name else ''}".rstrip("/")

                results.append({
                    "platform": platform,
                    "program": program_name,
                    "program_url": program_url,
                    "repo_url": repo_url,
                    "repo_host": host,
                    "org": org,
                    "repo_name": repo_name
                })

# -------------------------------
# Deduplicate by repo_url
# -------------------------------
unique = {item["repo_url"]: item for item in results}

os.makedirs("data", exist_ok=True)
with open("data/repos.json", "w", encoding="utf-8") as f:
    json.dump(list(unique.values()), f, indent=2, ensure_ascii=False)

print(f"✅ Extracted {len(unique)} repositories")
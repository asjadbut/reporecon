# RepoRecon

RepoRecon helps bug bounty hunters find open-source repositories that are in scope for bug bounty programs.

It pulls data from several platforms:
- HackerOne
- Bugcrowd
- Intigriti
- YesWeHack

The data is refreshed automatically from the bounty-targets-data project and turned into a simple website you can browse.

## How it works

- A GitHub Action runs on a schedule.
- It clones the bounty-targets-data repo.
- `scripts/extract_repos.py` parses the JSON files and writes `data/repos.json`.
- The static site in `index.html` reads `data/repos.json` and shows a table you can filter.

## Use it locally

1. Clone this repo.
2. Run `python scripts/extract_repos.py` to build `data/repos.json`.
3. Open `index.html` in your browser (or serve the folder with any static file server).

## Dataset source

The data comes from:

https://github.com/arkadiyt/bounty-targets-data

## License

MIT
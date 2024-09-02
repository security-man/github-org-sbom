# github-org-sbom
Small python script to check and configure an Org SBOM

steps to use:

1) download repo
2) gh auth login, gh auth token, export GITHUB_TOKEN=<token value>
3) run python script github_org_sbom.py
4) grep -Rnw . -l -e <library string to search for here>
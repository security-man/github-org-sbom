# github-org-sbom
A small python script and grep command to allow you to find a specific software dependency across an entire GitHub Organisation. At present, Software Bill of Materials (SBOM) files are available within any particular GitHub repository, provided dependency graph is enabled. However, a single SBOM for the entire GitHub Organisation is not a current feature of GitHub.

## Use case
Imagine a scenario whereby a critical vulnerability is announced in a particular software package, or you may simply want to check the presence of a particular software package version within your GitHub Organisation. Rather than manually checking each repository individually, this script can be used to download all the SBOMs for each respective repository to local storage - these can then be scanned via grep for the software package name.

## How to use

1) Clone this repository and install the requirements listed in 'requirements.txt' to a local python environment
2) Authenticate to GitHub via the GitHub CLI, using the following commands:

To authenticate to GitHub:
```bash
gh auth login
```

To obtain an access token for GitHub:
```bash
gh auth token
```

To set the access token as an environment variable
```bash
export GITHUB_TOKEN=<token value>
```
3) Run python script 'github_org_sbom.py' . This will produce a directory 'sbom/com.github.[GitHub-Organisation-Name]/' containing all of the SBOM files for each repository in .json format
4) Perform regular expression search for the name of the particular software package of interest:

```bash
grep -Rnw . -l -e 'sbom/com.github.{GitHub-Organisation-Name}/'
```
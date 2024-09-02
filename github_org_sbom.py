from ghapi.all import GhApi
import os

owner = os.environ['GH_ORG']
org = owner
username = os.environ['GH_USER']
token = os.environ['GITHUB_TOKEN']
gh_api = GhApi()
page_results = 100
page = 0
org_repos = []

# Get list of repos for an Org
# Entering dangerous while loop - beware of rate limit failures!
maxretries = 3
attempt = 0
while attempt < maxretries:
   try:
      print("Requesting GitHub repo data for org")
      while page_results == 100:
        next_page = (gh_api.repos.list_for_org(org=org,per_page=100,page=page,auth=(username,token)))
        org_repos.append(next_page)
        page_results = len(next_page)
        page = page + 1
   except:
      attempt += 1
   else:
      break

repos = []
repos_set = {}
for page in range(len(org_repos)):
    for repo in range(len(org_repos[page])):
        repos.append(org_repos[page][repo]["name"])

# Get SBOM data for list of repos within an Org
sbom_data = []
actual_sbom_data = []
def get_sbom_data(repo_name):
    try:
        sbom = gh_api('/repos/{owner}/{repo}/dependency-graph/sbom', 'GET', route=dict(
        owner=owner, repo=repo_name,auth=(username,token)))
        sbom_data.append(sbom)
        actual_sbom_data.append(sbom)
    except:
        sbom = "Unconfigured"
        sbom_data.append(sbom)

unique_repos = list(set(repos))
for repo in unique_repos:
   get_sbom_data(repo)

# List repos without an SBOM (404 returned) and therefore unconfigured in GitHub
def list_unconfigured_repos(sbom_data):
    sbom_indices = [i for i, j in enumerate(sbom_data) if j == "Unconfigured"]
    unconfigured_repos = []
    for i in sbom_indices:
        unconfigured_repos.append(repos[i])
    return unconfigured_repos

unconfigured = list_unconfigured_repos(sbom_data)

def write_sbom(sbom):
   print(sbom['sbom']['name'])
   name = str(sbom['sbom']['name'])
   filename = "sbom/"+name+".json"
   os.makedirs(os.path.dirname(filename), exist_ok=True)
   sbom_string = str(sbom)
   with open(filename,'w') as f:
      f.write(sbom_string)
   print("Creating SBOM for repo " + name)
   f.close()

for sbom in actual_sbom_data:
   write_sbom(sbom)
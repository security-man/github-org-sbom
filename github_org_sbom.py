from ghapi.all import GhApi
import os

owner = os.environ['GH_ORG']
org = owner
user = os.environ['GH_USER']

gh_api = GhApi()
page_results = 100
page = 1
org_repos = []
while page_results == 100:
    next_page = (gh_api.repos.list_for_org(org=org,per_page=100,page=page))
    org_repos.append(next_page)
    page_results = len(next_page)
    page = page + 1

print(len(org_repos))
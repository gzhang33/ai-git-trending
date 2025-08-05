import requests
from config.settings import GITHUB_API_TOKEN

def get_repo_details(repo_name):
    """
    Fetches detailed repository information from the GitHub API.
    """
    if not GITHUB_API_TOKEN:
        print("⚠️ GitHub API token not configured. Skipping detailed data fetching.")
        return None

    try:
        owner, repo = repo_name.split('/')
    except ValueError:
        print(f"❌ Invalid repo name format: {repo_name}. Expected 'owner/repo'.")
        return None

    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Fetch contributor count separately
        contrib_url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=1&anon=true"
        contrib_response = requests.get(contrib_url, headers=headers, timeout=10)
        contrib_count = 0
        if contrib_response.ok and 'Link' in contrib_response.headers:
            links = requests.utils.parse_header_links(contrib_response.headers['Link'])
            for link in links:
                if link.get('rel') == 'last':
                    last_page_url = link.get('url', '')
                    # Extract page number from the URL
                    try:
                        contrib_count = int(last_page_url.split('page=')[-1])
                    except (ValueError, IndexError):
                        pass
        elif contrib_response.ok:
             contrib_count = len(contrib_response.json())


        return {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "created_at": data.get("created_at", "").split("T")[0],
            "updated_at": data.get("updated_at", "").split("T")[0],
            "open_issues": data.get("open_issues_count", 0),
            "watchers": data.get("subscribers_count", 0),
            "description": data.get("description") or "No description provided.",
            "language": data.get("language", "N/A"),
            "contributor_count": contrib_count
        }
    except requests.RequestException as e:
        print(f"❌ Error fetching repo details for {repo_name} from GitHub API: {e}")
        return None

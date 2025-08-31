import requests
from config.settings import GITHUB_API_TOKEN
from config.logging_config import get_logger

# 创建日志记录器
logger = get_logger('github_api', 'INFO')

def get_repo_details(repo_name):
    """
    Fetches detailed repository information from the GitHub API.
    """
    if not GITHUB_API_TOKEN:
        logger.warning("⚠️ GitHub API token not configured. Skipping detailed data fetching.")
        return None

    try:
        owner, repo = repo_name.split('/')
    except ValueError:
        logger.error(f"❌ Invalid repo name format: {repo_name}. Expected 'owner/repo'.")
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

        readme_content = get_readme_content(repo_name)

        return {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "created_at": data.get("created_at", "").split("T")[0],
            "updated_at": data.get("updated_at", "").split("T")[0],
            "open_issues": data.get("open_issues_count", 0),
            "watchers": data.get("subscribers_count", 0),
            "description": data.get("description") or "No description provided.",
            "language": data.get("language", "N/A"),
            "tags": data.get("topics", []),  # Extract tags
            "contributor_count": contrib_count,
            "readme_content": readme_content
        }
    except requests.RequestException as e:
        logger.error(f"❌ Error fetching repo details for {repo_name} from GitHub API: {e}")
        return None
def get_readme_content(repo_name):
    """
    Fetches the content of the README.md file for a repository.
    """
    if not GITHUB_API_TOKEN:
        logger.warning(f"⚠️ GitHub API token not configured. Skipping README fetching for {repo_name}.")
        return "README content not available."

    try:
        owner, repo = repo_name.split('/')
    except ValueError:
        logger.error(f"❌ Invalid repo name format for README fetching: {repo_name}.")
        return "README content not available."

    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    headers = {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github.v3.raw", # 使用 .raw 格式直接获取原始 Markdown 内容
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 404:
            logger.warning(f"🤔 No README file found for {repo_name}.")
            return "No README file found for this project."
        
        response.raise_for_status()
        
        readme_text = response.text
        max_length = 100000 # 限制在 100000 个字符左右
        if len(readme_text) > max_length:
            readme_text = readme_text[:max_length] + "\n\n... (README content truncated)"
            logger.info(f"✂️ README for {repo_name} was truncated to {max_length} characters.")

        return readme_text

    except requests.RequestException as e:
        logger.error(f"❌ Error fetching README for {repo_name}: {e}")
        return f"Error fetching README: {e}"


def get_entity_details(owner):
    """
    Fetches detailed information about a GitHub user or organization.
    """
    if not GITHUB_API_TOKEN:
        logger.warning("GitHub API token not configured. Skipping entity details fetching.")
        return None

    url = f"https://api.github.com/users/{owner}"
    headers = {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "name": data.get("name") or data.get("login"),
            "type": data.get("type"),
            "created_at": data.get("created_at", "").split("T")[0],
            "followers": data.get("followers", 0),
            "public_repos": data.get("public_repos", 0),
            "bio": data.get("bio") or "No bio provided."
        }
    except requests.RequestException as e:
        logger.error(f"❌ Error fetching entity details for {owner}: {e}")
        return None

def get_entity_repos(owner, sort_by='stargazers_count', limit=5):
    """
    Fetches the top repositories for a GitHub user or organization.
    """
    if not GITHUB_API_TOKEN:
        logger.warning("GitHub API token not configured. Skipping entity repos fetching.")
        return []

    url = f"https://api.github.com/users/{owner}/repos?type=owner&sort=updated&per_page=100"
    headers = {
        "Authorization": f"Bearer {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        repos = response.json()
        
        # Sort by the desired key, e.g., 'stargazers_count'
        if sort_by in ['stargazers_count', 'forks_count', 'watchers_count']:
            repos.sort(key=lambda r: r.get(sort_by, 0), reverse=True)
        
        # Format and return the top N repos
        top_repos = [
            {
                "name": repo["full_name"],
                "stars": repo.get("stargazers_count", 0),
                "language": repo.get("language", "N/A")
            }
            for repo in repos[:limit]
        ]
        return top_repos
    except requests.RequestException as e:
        logger.error(f"❌ Error fetching repos for {owner}: {e}")
        return []
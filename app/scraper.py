import requests
from bs4 import BeautifulSoup
from config.settings import GITHUB_TRENDING_URL, MAX_PROJECTS_TO_SCRAPE

def scrape_github_trending():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    print(f"⏳ Fetching top {MAX_PROJECTS_TO_SCRAPE} projects from GitHub Trending...")
    try:
        response = requests.get(GITHUB_TRENDING_URL, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching GitHub page: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    repo_list = []
    for repo in soup.find_all('article', class_='Box-row')[:MAX_PROJECTS_TO_SCRAPE]:
        title_element = repo.find('h2', class_='h3')
        if not title_element:
            continue
            
        repo_name_raw = title_element.get_text(strip=True)
        repo_name = " ".join(repo_name_raw.split()).replace(" / ", "/")
        repo_url = "https://github.com" + title_element.find('a')['href']
        
        description_element = repo.find('p', class_='col-9')
        repo_description = description_element.get_text(strip=True) if description_element else "No description provided."
        
        language_element = repo.find('span', itemprop='programmingLanguage')
        repo_language = language_element.get_text(strip=True) if language_element else "N/A"
        
        star_element = repo.find('a', href=f"{repo_url.replace('https://github.com','').strip()}/stargazers")
        repo_stars = 0
        if star_element:
            try:
                repo_stars = int(star_element.get_text(strip=True).replace(',', ''))
            except (ValueError, TypeError):
                repo_stars = 0

        repo_list.append({
            "name": repo_name,
            "url": repo_url,
            "description": repo_description,
            "language": repo_language,
            "stars": repo_stars,
        })
            
    print(f"✅ Successfully scraped {len(repo_list)} repositories.")
    return repo_list
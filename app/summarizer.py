from openai import OpenAI
from config.settings import (
    LLM_API_KEY, LLM_BASE_URL, LLM_MODEL,
    SINGLE_PROJECT_PROMPT_TEMPLATE, OVERVIEW_PROMPT_TEMPLATE, ENTITY_PROMPT_TEMPLATE
)
from .github_api import get_entity_details, get_entity_repos
import re
import time
from collections import Counter

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

def call_llm_with_retry(prompt, model, temperature, max_retries=3, delay=5):
    """
    Calls the LLM API with a retry mechanism.
    """
    last_exception = None
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            # Clean up thinking tags if they exist
            pattern = r"^(.*?)</think>"
            clean_content = re.sub(pattern, "", response.choices[0].message.content, flags=re.DOTALL).strip()
            return clean_content
        except Exception as e:
            last_exception = e
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
    
    print(f"❌ All {max_retries} attempts failed. Last error: {last_exception}")
    return None

def get_entity_summary(owner):
    """
    Generates a summary for a GitHub user or organization.
    """
    print(f"👤 Fetching details for entity: {owner}")
    entity_details = get_entity_details(owner)
    if not entity_details:
        return ""

    top_repos = get_entity_repos(owner)
    
    languages = [repo['language'] for repo in top_repos if repo['language'] and repo['language'] != 'N/A']
    main_languages = ", ".join(dict.fromkeys(lang for lang, count in Counter(languages).most_common(3))) if languages else "多样化或未指定"

    top_repos_str = "\n".join([f"- {repo['name']} ({repo['stars']} stars, {repo['language']})" for repo in top_repos]) or "暂无其他知名仓库。"

    prompt = ENTITY_PROMPT_TEMPLATE.format(
        name=entity_details.get('name', owner),
        type=entity_details.get('type', 'N/A'),
        bio=entity_details.get('bio', '无'),
        created_at=entity_details.get('created_at', 'N/A'),
        followers=entity_details.get('followers', 0),
        public_repos=entity_details.get('public_repos', 0),
        top_repos=top_repos_str,
        main_languages=main_languages
    )

    summary = call_llm_with_retry(prompt, LLM_MODEL, 0.6)
    if summary:
        return f"\n\n---\n\n### 👨‍💻 开发者/组织速览\n\n{summary}"
    
    print(f"❌ Error generating entity summary for {owner}")
    return ""

def get_summary_for_single_project(project):
    print(f"🧠 Analyzing project: {project['name']}...")
    prompt = SINGLE_PROJECT_PROMPT_TEMPLATE.format(**project)
    
    project_summary = call_llm_with_retry(prompt, LLM_MODEL, 0.7)
    if not project_summary:
        print(f"❌ Error calling LLM API for {project['name']}: Failed after retries.")
        return None

    try:
        owner = project['name'].split('/')[0]
        entity_summary = get_entity_summary(owner)
    except (IndexError, AttributeError):
        entity_summary = ""

    return project_summary + entity_summary

def get_overview_intro(projects):
    print("🧠 Generating overview introduction...")
    project_details = "\n".join([f"- {p['name']}: {p.get('description', 'No description')}" for p in projects])
    prompt = OVERVIEW_PROMPT_TEMPLATE.format(project_details=project_details)
    
    overview = call_llm_with_retry(prompt, LLM_MODEL, 0.8)
    if overview:
        return overview
        
    print("❌ Error calling LLM API for overview: Failed after retries.")
    return "## 每日GitHub热点观察 🚀"

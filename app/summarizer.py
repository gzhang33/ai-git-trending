from openai import OpenAI
from config.settings import (
    LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, 
    SINGLE_PROJECT_PROMPT_TEMPLATE, OVERVIEW_PROMPT_TEMPLATE
)
import re

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

def get_summary_for_single_project(project):
    print(f"🧠 Analyzing project: {project['name']}...")
    prompt = SINGLE_PROJECT_PROMPT_TEMPLATE.format(**project)
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}}
        )

        pattern = r"^(.*?)</think>"
        clean_text = re.sub(pattern, "", response.choices[0].message.content, flags=re.DOTALL)

        return clean_text
    except Exception as e:
        print(f"❌ Error calling LLM API for {project['name']}: {e}")
        return None

def get_overview_intro(projects):
    print("🧠 Generating overview introduction...")
    project_names = "\n".join([f"- {p['name']}" for p in projects])
    prompt = OVERVIEW_PROMPT_TEMPLATE.format(project_names=project_names)
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        pattern = r"^(.*?)</think>"
        clean_text = re.sub(pattern, "", response.choices[0].message.content, flags=re.DOTALL)
        return clean_text
    except Exception as e:
        print(f"❌ Error calling LLM API for overview: {e}")
        return "## 每日GitHub热点观察 🚀"
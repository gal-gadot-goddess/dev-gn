"""
AI Metadata Generator for dev-gn via Pollinations AI
Focuses on DevOps, Cloud Infrastructure, Kubernetes, Docker, CI/CD, Terraform, SRE, and GitOps for @devopsgen.
Extracts context from visual HTML animations and generates high-converting viral hook titles,
SEO captions, and strictly 5 lowercase hashtags.
"""

import os
import sys
import re
import json
import html
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

def extract_html_context(html_path: Path) -> dict:
    """
    Extracts core DevOps/Cloud architecture concepts, headings, diagrams, and mechanics
    from the visual HTML animation file to provide rich context to the AI.
    """
    if not html_path:
        return {}
    
    path_obj = Path(html_path)
    if not path_obj.exists():
        return {}

    try:
        raw_text = path_obj.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}

    title_match = re.search(r'<title>(.*?)</title>', raw_text, re.IGNORECASE | re.DOTALL)
    page_title = html.unescape(title_match.group(1)).strip() if title_match else ""
    page_title = re.sub(r'^(?:VIZ\s*\d+\s*[·•\-\s—–]*|[·•\-\s—–]+)', '', page_title, flags=re.IGNORECASE).strip()

    # Strip styles & scripts
    clean = re.sub(r'<style.*?</style>', '', raw_text, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<script.*?</script>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', ' ', clean)
    clean = html.unescape(clean)

    lines = [l.strip() for l in clean.splitlines() if l.strip()]

    # UI controls & handles to exclude
    ignore_set = {"@yourhandle", "@devopsgen", "@cryptokregg", "@kreggscode", "replay", "replayed", "fit", "mute", "unmute", "speed", "1x", "2x", "safe zones", "sound", "music"}
    meaningful_lines = []
    for l in lines:
        if l.lower() in ignore_set:
            continue
        # Skip pure numbers/counters or single symbols
        if len(l) > 3 and not re.match(r'^[0-9\s:.\-→·]+$', l):
            meaningful_lines.append(l)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for m in meaningful_lines:
        m_lower = m.lower()
        if m_lower not in seen:
            seen.add(m_lower)
            deduped.append(m)

    return {
        "page_title": page_title,
        "content_snippets": deduped[:12]
    }

def clean_filename_to_title(filename: str) -> str:
    name = Path(filename).stem
    # Remove leading numbers like VIZ 08 —, VIZ_10_, 01-, etc.
    name = re.sub(r'^(?:VIZ\s*\d+\s*[—–\-_]*|\d+[—–\-_]*)', '', name, flags=re.IGNORECASE)
    name = name.replace("_", " ").replace("-", " ")
    return " ".join(name.split())

def clean_hashtags(raw_tags: list, topic: str = "") -> list:
    """
    Ensures strictly at most 5 relevant hashtags, ALL in lowercase small letters.
    """
    clean = []
    for tag in raw_tags:
        if not isinstance(tag, str):
            continue
        t = tag.strip().lower()
        if not t.startswith("#"):
            t = f"#{t}"
        # Keep only alphanumeric and underscore after #
        t = re.sub(r'[^#a-z0-9_]', '', t)
        if len(t) > 2 and t not in clean:
            clean.append(t)

    # Fallback to sensible DevOps defaults if too few
    default_fallbacks = [
        "#devops",
        "#kubernetes",
        "#docker",
        "#cloud",
        "#cicd"
    ]
    for d in default_fallbacks:
        d_clean = d.lower()
        if len(clean) >= 5:
            break
        if d_clean not in clean:
            clean.append(d_clean)

    return clean[:5]

def generate_ai_metadata(topic: str, html_file_path: Path = None) -> dict:
    """
    Generates SEO viral title, Instagram caption, Facebook caption, Threads caption,
    and exactly 5 lowercase hashtags from the HTML content and topic name.
    """
    if isinstance(topic, (str, Path)) and (str(topic).endswith(".html") or Path(topic).exists()):
        if not html_file_path:
            html_file_path = Path(topic)
        topic = clean_filename_to_title(str(topic))

    context = extract_html_context(html_file_path) if html_file_path else {}
    snippets = context.get("content_snippets", [])
    display_title = context.get("page_title") or topic

    topic_words = topic.split()
    lead_word = topic_words[0].lower() if topic_words else "devops"
    fallback_metadata = {
        "title": f"{display_title}: How It Works Under The Hood ⚙️",
        "ig_caption": f"⚙️ {display_title} Explained Visually!\n\n"
                      f"Mastering modern infrastructure and deployment workflows is essential for every DevOps engineer, SRE, and cloud developer.\n\n"
                      + ("\n".join([f"• {s}" for s in snippets[:6]]) if snippets else f"• Deep dive into {topic} architecture and reliability patterns.")
                      + f"\n\nHow do you handle this in your production environment? Drop your setup below! 👇\n\n"
                      f"Follow @devopsgen for daily visual breakdowns of DevOps & Cloud Architecture.",
        "fb_caption": f"Deep Dive: {display_title}.\n\n"
                      f"In modern cloud infrastructure and CI/CD pipelines, understanding the architectural trade-offs helps teams prevent downtime and deploy with confidence.\n\n"
                      + ("\n".join([f"- {s}" for s in snippets[:8]]) if snippets else f"Complete visual overview of {topic}.")
                      + f"\n\nWhat tools does your team use for this? Let's discuss in the comments below!",
        "threads_caption": f"{display_title} visualized in under 20s. What's your go-to DevOps tooling stack? #{lead_word} #devops #cloud",
        "hashtags": clean_hashtags([f"#{lead_word}", "#devops", "#kubernetes", "#docker", "#cloud"], topic)
    }

    api_key = os.environ.get("POLLINATIONS_API_KEY", "")
    endpoints = [
        "https://gen.pollinations.ai/v1/chat/completions",
        "https://text.pollinations.ai/openai"
    ]

    context_str = f"Topic: {topic}\n"
    if context.get("page_title"):
        context_str += f"Visual Reel Title: {context['page_title']}\n"
    if snippets:
        context_str += "Key Visual Mechanics & Storyline:\n- " + "\n- ".join(snippets[:10])

    prompt = f"""You are a principal cloud architect, staff DevOps engineer, and viral tech educator managing @devopsgen.
You create viral, high-retention, educational reels for software engineers, DevOps practitioners, SREs, and cloud architects.

We are publishing an animated technical concept reel based on this visual DevOps/Cloud animation:
{context_str}

REQUIREMENTS:
1. "title": Viral SEO hook title (max 65 chars) with an emoji. Make it punchy, insightful, and curious (e.g. "Kubernetes Self-Healing Explained ⚡", "Canary vs Blue-Green Deployments 🚀", "Docker Layer Caching Under The Hood 🐳").
2. "ig_caption": High-retention Instagram caption:
   - First 2 lines: Hook that stops the scroll.
   - Body: Clean bullet points explaining what happens under the hood based on the visual concepts provided.
   - Practical Takeaway: 1-2 sentence real-world production advice or best practice.
   - Call to Action: Ask a thought-provoking engineering question to drive comment engagement.
   - Sign-off: "Follow @devopsgen for daily visual breakdowns of DevOps & Cloud Architecture."
3. "fb_caption": In-depth professional DevOpsGen Facebook post explaining the architectural trade-offs, scalability, and production resilience.
4. "threads_caption": Short, punchy summary + debate question (max 280 chars).
5. "hashtags": STRICTLY EXACTLY 5 relevant hashtags, ALL in LOWERCASE small letters only (e.g. ["#devops", "#kubernetes", "#docker", "#cloud", "#cicd"]).

OUTPUT FORMAT:
Return strictly a valid JSON object with keys: "title", "ig_caption", "fb_caption", "threads_caption", "hashtags".
"""

    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": "You are a professional DevOps content strategist. You output strictly valid JSON without markdown wrapping."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    for ep in endpoints:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Antigravity-Agent"
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            req = urllib.request.Request(ep, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=25) as resp:
                raw_text = resp.read().decode("utf-8")
                res = json.loads(raw_text)
                content = res.get("choices", [{}])[0].get("message", {}).get("content", "")
                if not content:
                    content = raw_text

                raw_clean = re.sub(r"^```(?:json)?\s*", "", content.strip(), flags=re.MULTILINE)
                raw_clean = re.sub(r"\s*```$", "", raw_clean, flags=re.MULTILINE).strip()
                data = json.loads(raw_clean)

                data["hashtags"] = clean_hashtags(data.get("hashtags", []), topic)
                print(f"✅ Successfully generated viral DevOps AI metadata via Pollinations ({ep}).")
                return data
        except Exception as e:
            print(f"⚠️ Notice for Pollinations endpoint {ep}: {e}")

    print("ℹ️ Using curated context-aware fallback metadata.")
    return fallback_metadata

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "VIZ 11 — Kubernetes Self-Healing.html"
    p = Path(t)
    if p.exists():
        res = generate_ai_metadata(p.name, html_file_path=p)
    else:
        res = generate_ai_metadata(t)
    print(json.dumps(res, indent=2, ensure_ascii=False))

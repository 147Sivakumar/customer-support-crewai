
from datetime import datetime, date
import re

from crewai.tools import tool
from ddgs import DDGS


TECH_TERMS = [
    "technology",
    "technology news",
    "artificial intelligence",
    "machine learning",
    "generative ai",
    "software",
    "hardware",
    "semiconductor",
    "chip",
    "cybersecurity",
    "cyber security",
    "cloud computing",
    "robotics",
    "robot",
    "smartphone",
    "mobile phone",
    "laptop",
    "computer",
    "internet",
    "search engine",
    "google",
    "microsoft",
    "apple",
    "openai",
    "nvidia",
    "meta",
    "oracle",
    "amazon",
    "raspberry pi",
    "data center",
    "data centre",
]


def get_local_publication_date(date_value):
    """Convert a search result date into the computer's local date."""
    if not date_value:
        return None

    try:
        parsed = datetime.fromisoformat(
            str(date_value).replace("Z", "+00:00")
        )

        if parsed.tzinfo is not None:
            parsed = parsed.astimezone()

        return parsed.date()

    except (ValueError, TypeError):
        try:
            return date.fromisoformat(str(date_value)[:10])
        except (ValueError, TypeError):
            return None


def is_technology_related(title, body):
    """Check whether an article is related to technology."""
    content = f"{title} {body}".lower()

    for term in TECH_TERMS:
        if term in content:
            return True

    # Check short terms as complete words, not partial matches.
    return bool(re.search(r"\b(ai)\b", content))


@tool("Internet Search Tool")
def internet_search_tool(query: str) -> str:
    """
    Search the internet for customer support information.
    Today's news must have a verifiable local publication date.
    Technology news must also be relevant to technology.
    """
    try:
        query_lower = query.lower()

        news_keywords = [
            "latest", "recent", "current", "today",
            "news", "headlines", "this week", "this month"
        ]

        is_news_query = any(
            word in query_lower for word in news_keywords
        )

        is_today_query = "today" in query_lower

        is_technology_query = (
            "technology" in query_lower
            or "tech news" in query_lower
            or "tech headlines" in query_lower
        )

        ddgs = DDGS()

        if is_news_query:
            results = ddgs.news(
                query,
                timelimit="d",
                max_results=20
            )
        else:
            results = ddgs.text(
                query,
                max_results=5
            )

        if not results:
            return "No relevant internet search results found."

        today = datetime.now().astimezone().date()

        formatted_results = []
        seen_urls = set()

        for result in results:
            title = result.get("title") or "No title"
            body = result.get("body") or "No description"
            url = result.get("url") or result.get("href") or ""
            raw_date = result.get("date")
            source = result.get("source") or "Source not provided"

            if not url or url in seen_urls:
                continue

            publication_date = get_local_publication_date(raw_date)

            if is_today_query and publication_date != today:
                continue

            if is_technology_query and not is_technology_related(
                title, body
            ):
                continue

            seen_urls.add(url)

            date_text = (
                publication_date.strftime("%d %B %Y")
                if publication_date
                else "Publication date not provided"
            )

            formatted_results.append(
                f"Result {len(formatted_results) + 1}\n"
                f"Title: {title}\n"
                f"Source: {source}\n"
                f"Publication Date: {date_text}\n"
                f"Description: {body}\n"
                f"URL: {url}"
            )

            if len(formatted_results) >= 5:
                break

        if not formatted_results:
            return (
                f"No relevant articles with verifiable dates "
                f"were found for today's local date ({today}). "
                "Do not invent headlines or publication dates."
            )

        instructions = (
            "\n\nIMPORTANT RESEARCH INSTRUCTIONS:\n"
            "- Use only the articles listed below.\n"
            "- Copy publication dates exactly as provided.\n"
            "- Never invent or guess publication dates.\n"
            "- Do not include unrelated articles.\n"
            "- Include headline, source, date, description and URL.\n"
            "- If fewer than three relevant articles are found, "
            "show only the available relevant articles.\n"
        )

        return instructions + "\n\n".join(formatted_results)

    except Exception as error:
        return f"Internet search failed: {str(error)}"


print("Internet Search Tool is ready.")

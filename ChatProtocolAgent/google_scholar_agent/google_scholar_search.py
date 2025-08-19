from uagents import Agent, Context, Model
from scholarly import scholarly
#import json
#import openai
import google.generativeai as genai

# Define the input model class
class initRARequest(Model):
    query: str

# Define a common response model
class initRAResponse(Model):
    results: list

def extract_keywords_and_topic_gemini(text: str, 
                                      gemini_api_key: str = 'YOUR_GEMINI_API_KEY') -> tuple[list, str]:
    """
    Extracts the most important keywords and the main topic from a given text using Gemini Pro.

    Parameters:
        text (str): The input text.
        gemini_api_key (str): Gemini API key from https://makersuite.google.com/app/apikey

    Returns:
        tuple: (list of keywords, topic string)
    """
    try:
        # Configure API
        genai.configure(api_key=gemini_api_key)

        # Initialize Gemini Pro model
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Create prompt
        prompt = (
            f"Extract keywords and the main topic from the following text:\n{text}\n\n"
            "Respond ONLY in this format:\n"
            "Keywords:\nkeyword1\nkeyword2\nkeyword3\n"
            "Topic:\n<one short topic line>"
        )

        # Send prompt to Gemini
        response = model.generate_content(prompt)

        content = response.text.strip()

        # Parse output
        parts = content.split("Topic:\n")
        keywords = []
        topic = "Unknown"

        if len(parts) == 2:
            keyword_lines = parts[0].splitlines()
            for line in keyword_lines:
                line = line.strip()
                if line and not line.lower().startswith("keywords"):
                    keywords.append(line)
            topic = parts[1].strip()
        else:
            keywords = [word.strip() for word in content.splitlines() if word.strip()]
            topic = "Unknown"

        return keywords, topic

    except Exception as e:
        print(f"[ERROR] Gemini extraction failed: {e}")
        return [f"Error: {str(e)}"], "Unknown"


async def search_google_scholar(query: str, max_results: int = 5) -> str:
    """Search Google Scholar and return formatted markdown with top results."""
    print(f"[INFO] Searching for: {query}")
    keywords, topic = extract_keywords_and_topic_gemini(query)

    print(f"[INFO] Extracted Keywords: {keywords}")
    print(f"[INFO] Main Topic: {topic}")

    keyword_query = ' '.join(keywords)
    search_query = scholarly.search_pubs(keyword_query)

    result_string = ""
    for i in range(max_results):
        try:
            paper = next(search_query)
            title = paper["bib"]["title"]
            authors = paper["bib"].get("author", "Unknown")
            link = paper.get("pub_url", "No link available")
            year = paper["bib"].get("pub_year", "Unknown")

            formatted_entry = (
                f"### {title}\n"
                f"- **Authors:** {authors}\n"
                f"- **Year:** {year}\n"
                f"- **Link:** [{link}]({link})\n\n"
            )
            result_string += formatted_entry
        except StopIteration:
            break

    return result_string.strip()

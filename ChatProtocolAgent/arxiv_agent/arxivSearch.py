from uagents import Agent, Context, Model
import arxiv
import json
import google.generativeai as genai

# Define the input model for the search request
class initRARequest(Model):
    query: str

# Define a common response model
class initRAResponse(Model):
    results: str  # Changed from list to string

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

# Function to search ArXiv and return formatted string results
async def search_arxiv_papers(query, max_results=5):
    """Searches ArXiv for papers related to the given query and returns a formatted string."""
    keywords = extract_keywords_and_topic_gemini(query)
    keywords = ','.join([str(item) for sublist in keywords for item in (sublist if isinstance(sublist, list) else [sublist])])
    print(f'Keywords: {keywords}')
    search = arxiv.Search(
        query=keywords,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    result_string = ""
    for paper in search.results():
        formatted_entry = (
            f"### {paper.title}\n\n"
            f"- **Authors:** {', '.join(author.name for author in paper.authors)}\n"
            f"- **Link:** [{paper.entry_id}]({paper.entry_id})\n"
            f"- **Published Date:** {paper.published.strftime('%Y-%m-%d')}\n\n"
            "---\n\n"
        )
        result_string += formatted_entry

    return result_string.strip()

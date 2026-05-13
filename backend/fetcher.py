import os
import json
from parallel import Parallel
from dotenv import load_dotenv

load_dotenv()

def fetch_all_daily_content():
    """Uses Parallel AI to fetch all top AI news and research papers from the last 24 hours."""
    print("Starting Parallel AI web research...")

    api_key = os.getenv("PARALLEL_API_KEY")
    if not api_key:
        print("PARALLEL_API_KEY not configured. Returning empty content.")
        return []

    client = Parallel(api_key=api_key)

    output_schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "description": "A list of all the top AI announcements and research papers from the last 24 hours.",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "The name of the organization or publication (e.g., OpenAI, DeepMind, ArXiv)"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the announcement or paper"
                        },
                        "link": {
                            "type": "string",
                            "description": "The URL to the original article or paper"
                        },
                        "summary": {
                            "type": "string",
                            "description": "A 2-3 sentence summary of the announcement or paper"
                        }
                    },
                    "required": ["source", "title", "link", "summary"]
                }
            }
        },
        "required": ["items"]
    }

    try:
        task_run = client.task_run.create(
            input="Find ALL the top AI announcements, product releases, and research papers from the last 24 hours. Search official blogs of OpenAI, Google DeepMind, Anthropic, Hugging Face, Mistral, Meta AI, top VC firms like a16z, and ArXiv. Return every significant announcement you find, do not limit to just 5.",
            output_schema=output_schema
        )

        print(f"Parallel task started (ID: {task_run.run_id}). Waiting for autonomous agent to finish research...")

        run_result = client.task_run.result(task_run.run_id, api_timeout=600)

        # Extract the items from the result
        output = run_result.output
        if hasattr(output, 'content'):
            data = output.content
        elif isinstance(output, dict):
            data = output
        else:
            data = {}

        items = data.get("items", [])
        print(f"Parallel AI found {len(items)} items.")
        return items

    except Exception as e:
        print(f"Error fetching content from Parallel AI: {e}")
        return []

if __name__ == "__main__":
    content = fetch_all_daily_content()
    for item in content:
        print(f"[{item['source']}] {item['title']}")

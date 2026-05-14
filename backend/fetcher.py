import os
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
                "description": "A comprehensive list of all major AI announcements, product releases, and research papers from the last 24 hours.",
                "items": {
                    "type": "object",
                    "properties": {
                        "source": {
                            "type": "string",
                            "description": "The organization or publication (e.g., OpenAI, Google DeepMind, ArXiv)"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the announcement or paper"
                        },
                        "link": {
                            "type": "string",
                            "description": "The URL to the original article or paper"
                        },
                        "detailed_analysis": {
                            "type": "string",
                            "description": "A deep-dive analysis (at least 3-4 paragraphs) covering: 1. What it is. 2. Key technical details and innovations. 3. Why it matters to the AI industry. 4. Potential real-world applications or implications."
                        }
                    },
                    "required": ["source", "title", "link", "detailed_analysis"]
                }
            }
        },
        "required": ["items"]
    }

    try:
        task_run = client.task_run.create(
            input="Find ALL the top AI announcements, product releases, and research papers from the exact last 24 hours. Search official blogs of OpenAI, Google DeepMind, Anthropic, Hugging Face, Mistral, Meta AI, top VC firms like a16z, and ArXiv. You must extract deep, highly detailed information about each announcement, not just a surface-level summary. Focus on technical depth and industry impact.",
            processor="pro",
            task_spec={
                "output_schema": {
                    "type": "json",
                    "json_schema": output_schema
                }
            }
        )

        print(f"Parallel task started (ID: {task_run.run_id}). Waiting for autonomous agent to finish research...")

        run_result = client.task_run.result(task_run.run_id, api_timeout=600)

        # Extract the items from the result — handle all possible output types
        output = run_result.output
        data = {}

        if hasattr(output, 'content') and isinstance(output.content, dict):
            # Object with a 'content' dict attribute
            data = output.content
        elif hasattr(output, 'model_dump'):
            # Pydantic model — convert to dict
            data = output.model_dump()
        elif isinstance(output, dict):
            # Already a plain dict
            data = output
        else:
            # Last resort: try converting to dict
            try:
                data = dict(output)
            except Exception:
                print("Warning: Could not parse Parallel AI output format.")
                data = {}

        items = data.get("items", [])
        if not items:
            print("Warning: Parallel AI returned no items. Raw output:", output)
        else:
            print(f"Parallel AI found {len(items)} items.")
        return items

    except Exception as e:
        print(f"Error fetching content from Parallel AI: {e}")
        return []

if __name__ == "__main__":
    content = fetch_all_daily_content()
    for item in content:
        print(f"[{item['source']}] {item['title']}")

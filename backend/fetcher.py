# pyrefly: ignore [missing-import]
import feedparser
import requests
from datetime import datetime, timedelta
import urllib.parse
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup

# Define sources
RSS_FEEDS = {
    "OpenAI": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/feed.xml", # They don't have a standard RSS, might need to scrape if feedparser fails, but let's try generic
    "a16z AI": "https://a16z.com/category/ai/feed/",
    "Google AI": "https://blog.research.google/feeds/posts/default?alt=rss"
}

def get_recent_rss_entries(feed_url, source_name, days_back=1):
    """Fetch entries from an RSS feed from the last `days_back` days."""
    try:
        feed = feedparser.parse(feed_url)
        recent_entries = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for entry in feed.entries:
            # Try to parse published date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                published = datetime(*entry.updated_parsed[:6])
            
            if published and published >= cutoff_date:
                # Clean HTML from summary
                summary = BeautifulSoup(entry.summary if hasattr(entry, 'summary') else entry.description, 'html.parser').get_text() if hasattr(entry, 'summary') or hasattr(entry, 'description') else ""
                
                recent_entries.append({
                    "source": source_name,
                    "title": entry.title,
                    "link": entry.link,
                    "summary": summary[:500] + "..." if len(summary) > 500 else summary
                })
        return recent_entries
    except Exception as e:
        print(f"Error fetching RSS for {source_name}: {e}")
        return []

def get_recent_arxiv_papers(days_back=1, max_results=5):
    """Fetch recent AI papers from ArXiv."""
    print("Fetching ArXiv papers...")
    base_url = 'http://export.arxiv.org/api/query?'
    query = 'cat:cs.AI OR cat:cs.CL OR cat:cs.CV OR cat:cs.LG'
    params = {
        'search_query': query,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
        'max_results': max_results
    }
    
    url = base_url + urllib.parse.urlencode(params)
    try:
        response = requests.get(url)
        feed = feedparser.parse(response.content)
        papers = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for entry in feed.entries:
            published = datetime(*entry.published_parsed[:6])
            if published >= cutoff_date:
                papers.append({
                    "source": "ArXiv",
                    "title": entry.title.replace('\n', ' '),
                    "link": entry.link,
                    "summary": entry.summary.replace('\n', ' ')[:500] + "..."
                })
        return papers
    except Exception as e:
        print(f"Error fetching ArXiv: {e}")
        return []

def fetch_all_daily_content():
    """Aggregates all content from the last 24 hours."""
    print("Starting content fetch...")
    all_content = []
    
    # Fetch from RSS
    for source, url in RSS_FEEDS.items():
        print(f"Fetching from {source}...")
        entries = get_recent_rss_entries(url, source)
        all_content.extend(entries)
        
    # Fetch from ArXiv
    papers = get_recent_arxiv_papers(max_results=5) # Limit to top 5 to avoid overwhelming the podcast
    all_content.extend(papers)
    
    print(f"Found {len(all_content)} items from the last 24 hours.")
    return all_content

if __name__ == "__main__":
    content = fetch_all_daily_content()
    for item in content:
        print(f"[{item['source']}] {item['title']}")

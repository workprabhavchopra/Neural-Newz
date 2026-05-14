import os
from datetime import datetime
from email.utils import formatdate
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_rss_feed(episodes_data, output_file="../frontend/public/feed.xml"):
    """
    Generates or updates the podcast RSS feed for Spotify.
    episodes_data is a list of dicts: {'title': '...', 'description': '...', 'audio_url': '...', 'length': '12345', 'pub_date': '...'}
    """
    print(f"Generating RSS feed at {output_file}...")
    
    BASE_URL = os.getenv("BASE_URL", "https://neural-newz.netlify.app")
    
    rss = ET.Element("rss", version="2.0", attrib={
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/"
    })
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Neural Newz Daily"
    ET.SubElement(channel, "link").text = BASE_URL
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "description").text = "Your daily deep-dive into AI. Neural Newz covers the latest breakthroughs, product launches, and research from the world's top AI labs — explained clearly for anyone who wants to stay ahead."
    
    # Spotify-required channel metadata
    ET.SubElement(channel, "itunes:author").text = "Neural Newz"
    ET.SubElement(channel, "itunes:explicit").text = "false"
    ET.SubElement(channel, "itunes:type").text = "episodic"
    ET.SubElement(channel, "itunes:image", href=f"{BASE_URL}/cover.jpg")
    ET.SubElement(channel, "itunes:category", text="Technology")
    ET.SubElement(channel, "itunes:category", text="Education")
    
    for ep in episodes_data:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep['title']
        ET.SubElement(item, "description").text = ep['description']
        ET.SubElement(item, "itunes:summary").text = ep['description']
        ET.SubElement(item, "itunes:explicit").text = "false"
        ET.SubElement(item, "itunes:episodeType").text = "full"
        
        enclosure_url = ep['audio_url']
        if not enclosure_url.startswith("http"):
            enclosure_url = f"{BASE_URL}/{enclosure_url}"
            
        ET.SubElement(item, "enclosure", url=enclosure_url, type="audio/mpeg", length=str(ep.get('length', '0')))
        ET.SubElement(item, "pubDate").text = ep.get('pub_date', formatdate(timeval=None, localtime=False, usegmt=True))
        ET.SubElement(item, "guid", isPermaLink="false").text = enclosure_url
        
    xmlstr = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xmlstr)
        
    print("RSS feed generated successfully.")

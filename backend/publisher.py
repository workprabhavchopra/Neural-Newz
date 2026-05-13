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
    
    rss = ET.Element("rss", version="2.0", attrib={"xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Neural Newz Daily"
    ET.SubElement(channel, "link").text = BASE_URL
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "description").text = "Daily AI news and research papers curated from top labs and VC firms."
    
    itunes_author = ET.SubElement(channel, "itunes:author")
    itunes_author.text = "Neural Newz"
    
    ET.SubElement(channel, "itunes:category", text="Technology")
    
    for ep in episodes_data:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep['title']
        ET.SubElement(item, "description").text = ep['description']
        
        enclosure_url = ep['audio_url']
        if not enclosure_url.startswith("http"):
            enclosure_url = f"{BASE_URL}/{enclosure_url}"
            
        ET.SubElement(item, "enclosure", url=enclosure_url, type="audio/mpeg", length=str(ep.get('length', '0')))
        ET.SubElement(item, "pubDate").text = ep.get('pub_date', formatdate(timeval=None, localtime=False, usegmt=True))
        ET.SubElement(item, "guid").text = enclosure_url
        
    xmlstr = minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xmlstr)
        
    print("RSS feed generated successfully.")

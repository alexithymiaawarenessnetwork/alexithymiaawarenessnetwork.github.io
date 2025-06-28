#!/usr/bin/env python3
"""
Link Generation Script for AAN Citations
Demonstrates how to dynamically compose affiliate links from separated data.
"""

import json
import urllib.parse

def load_config():
    """Load affiliate configuration."""
    with open('affiliate_config.json', 'r') as f:
        return json.load(f)

def load_citations():
    """Load citation database."""
    with open('aan/docs/citations.json', 'r') as f:
        return json.load(f)

def generate_bookshop_link(citation, config):
    """Generate Bookshop.org affiliate link."""
    affiliate_id = config['affiliate_ids']['bookshop_org']
    if not affiliate_id:
        return None
    
    retailers = citation.get('retailers', {})
    bookshop_data = retailers.get('bookshop_org', {})
    
    if 'url' in bookshop_data:
        # Use the specific product URL with affiliate parameter
        base_url = bookshop_data['url']
        if 'ean' in bookshop_data:
            return f"{base_url}?ean={bookshop_data['ean']}&affiliate={affiliate_id}"
        else:
            return f"{base_url}?affiliate={affiliate_id}"
    elif 'isbn' in bookshop_data:
        template = config['url_templates']['bookshop_org']['isbn_format']
        return template.format(affiliate_id=affiliate_id, isbn=bookshop_data['isbn'])
    elif 'search' in bookshop_data:
        template = config['url_templates']['bookshop_org']['search_format']
        return template.format(affiliate_id=affiliate_id, search=bookshop_data['search'])
    
    return None

def generate_barnes_noble_link(citation, config):
    """Generate Barnes & Noble link."""
    retailers = citation.get('retailers', {})
    bn_data = retailers.get('barnes_noble', {})
    
    if 'slug' in bn_data:
        template = config['url_templates']['barnes_noble']['slug_format']
        return template.format(slug=bn_data['slug'])
    elif 'isbn' in citation:
        template = config['url_templates']['barnes_noble']['isbn_format']
        return template.format(isbn=citation['isbn'])
    
    return None

def generate_amazon_link(citation, config):
    """Generate Amazon link (with or without affiliate)."""
    affiliate_id = config['affiliate_ids']['amazon']
    retailers = citation.get('retailers', {})
    amazon_data = retailers.get('amazon', {})
    
    if 'asin' in amazon_data:
        if affiliate_id:
            template = config['url_templates']['amazon']['affiliate_format']
            return template.format(asin=amazon_data['asin'], affiliate_id=affiliate_id)
        else:
            template = config['url_templates']['amazon']['asin_format']
            return template.format(asin=amazon_data['asin'])
    elif 'isbn' in citation:
        template = config['url_templates']['amazon']['isbn_format']
        return template.format(isbn=citation['isbn'])
    
    return None

def generate_all_links(citation_id):
    """Generate all available purchase links for a citation."""
    config = load_config()
    citations = load_citations()
    
    # Find the citation
    citation = None
    for c in citations['citations']:
        if c['id'] == citation_id:
            citation = c
            break
    
    if not citation:
        print(f"Citation '{citation_id}' not found")
        return
    
    print(f"\n=== {citation['title']} ===")
    print(f"Authors: {', '.join(citation['authors'])}")
    print(f"Year: {citation['year']}")
    print(f"Type: {citation['type']}")
    
    if citation['type'] == 'book':
        print(f"\nPurchase Links:")
        
        # Bookshop.org (priority)
        bookshop_link = generate_bookshop_link(citation, config)
        if bookshop_link:
            print(f"📚 Bookshop.org: {bookshop_link}")
        
        # Barnes & Noble
        bn_link = generate_barnes_noble_link(citation, config)
        if bn_link:
            print(f"📖 Barnes & Noble: {bn_link}")
        
        # Amazon
        amazon_link = generate_amazon_link(citation, config)
        if amazon_link:
            print(f"📦 Amazon: {amazon_link}")
    
    # Free sources
    if 'free_sources' in citation:
        print(f"\nFree Sources:")
        for source, url in citation['free_sources'].items():
            print(f"🆓 {source.replace('_', ' ').title()}: {url}")
    
    # Direct URL (for papers, tools, etc.)
    if 'url' in citation:
        print(f"\nDirect Link: {citation['url']}")

def generate_markdown_links(citation_id):
    """Generate markdown-formatted links for use in documentation."""
    config = load_config()
    citations = load_citations()
    
    citation = None
    for c in citations['citations']:
        if c['id'] == citation_id:
            citation = c
            break
    
    if not citation or citation['type'] != 'book':
        return
    
    links = []
    
    # Bookshop.org
    bookshop_link = generate_bookshop_link(citation, config)
    if bookshop_link:
        links.append(f"[Buy at Bookshop.org]({bookshop_link})")
    
    # Barnes & Noble
    bn_link = generate_barnes_noble_link(citation, config)
    if bn_link:
        links.append(f"[Barnes & Noble]({bn_link})")
    
    # Amazon
    amazon_link = generate_amazon_link(citation, config)
    if amazon_link:
        links.append(f"[Amazon]({amazon_link})")
    
    return " | ".join(links)

if __name__ == "__main__":
    # Example usage
    print("=== AAN Citation Link Generator ===")
    
    # Generate links for a few key books
    examples = [
        "plutchik_1980_emotions",
        "taylor_bagby_parker_1997", 
        "brown_2012_daring_greatly",
        "spinoza_1677_ethics"
    ]
    
    for citation_id in examples:
        generate_all_links(citation_id)
        print(f"\nMarkdown: {generate_markdown_links(citation_id)}")
        print("-" * 60)

#!/usr/bin/env python3
"""
Test script to verify Bookshop.org affiliate links
"""

import json
import requests
import time

def load_config():
    """Load affiliate configuration."""
    with open('affiliate_config.json', 'r') as f:
        return json.load(f)

def load_citations():
    """Load citation database."""
    with open('aan/docs/citations.json', 'r') as f:
        return json.load(f)

def test_bookshop_link(url, title):
    """Test if a Bookshop.org URL is valid."""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            return True, "OK"
        elif response.status_code == 404:
            return False, "404 Not Found"
        else:
            return False, f"Status {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    config = load_config()
    citations = load_citations()
    
    print("=== Testing Bookshop.org Affiliate Links ===\n")
    
    books = [c for c in citations['citations'] if c['type'] == 'book' and 'retailers' in c and 'bookshop_org' in c['retailers']]
    
    for book in books:
        print(f"📚 {book['title']}")
        print(f"   Authors: {', '.join(book['authors'])}")
        
        bookshop_data = book['retailers']['bookshop_org']
        affiliate_id = config['affiliate_ids']['bookshop_org']
        
        if 'isbn' in bookshop_data:
            url = f"https://bookshop.org/a/{affiliate_id}/{bookshop_data['isbn']}"
            print(f"   ISBN: {bookshop_data['isbn']}")
        elif 'search' in bookshop_data:
            url = f"https://bookshop.org/search?keywords={bookshop_data['search']}&affiliate={affiliate_id}"
            print(f"   Search: {bookshop_data['search']}")
        else:
            print("   ❌ No ISBN or search term found")
            continue
            
        print(f"   URL: {url}")
        
        # Test the link
        is_valid, status = test_bookshop_link(url, book['title'])
        if is_valid:
            print(f"   ✅ {status}")
        else:
            print(f"   ❌ {status}")
        
        print()
        time.sleep(1)  # Be nice to the server

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify Bookshop.org affiliate links using curl
"""

import json
import subprocess
import time

def load_config():
    """Load affiliate configuration."""
    with open('affiliate_config.json', 'r') as f:
        return json.load(f)

def load_citations():
    """Load citation database."""
    with open('aan/docs/citations.json', 'r') as f:
        return json.load(f)

def test_bookshop_link_curl(url):
    """Test if a Bookshop.org URL is valid using curl."""
    try:
        result = subprocess.run([
            'curl', '-I', '-s', '-L', '--max-time', '10', url
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Check the first line for status code
            first_line = result.stdout.split('\n')[0]
            if '200 OK' in first_line:
                return True, "200 OK"
            elif '404' in first_line:
                return False, "404 Not Found"
            else:
                return False, f"Status: {first_line.strip()}"
        else:
            return False, f"Curl error: {result.returncode}"
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
        is_valid, status = test_bookshop_link_curl(url)
        if is_valid:
            print(f"   ✅ {status}")
        else:
            print(f"   ❌ {status}")
        
        print()
        time.sleep(1)  # Be nice to the server

if __name__ == "__main__":
    main()

#!/bin/bash

# Local Test Script for Alexithymia Awareness Network
# This script starts a local development server to test the site before deploying

echo "🚀 Starting local development server for AAN site..."
echo "📁 Changing to aan directory..."

cd aan

echo "🔧 Building site with current configuration..."
mkdocs build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "🌐 Starting development server..."
    echo ""
    echo "📋 Local server will be available at:"
    echo "   http://localhost:8000"
    echo ""
    echo "💡 Tips:"
    echo "   - The server will auto-reload when you make changes"
    echo "   - Press Ctrl+C to stop the server"
    echo "   - Check browser developer tools to verify GTM is loading"
    echo ""
    echo "🔍 To verify Google Analytics:"
    echo "   1. Open browser developer tools (F12)"
    echo "   2. Go to Network tab"
    echo "   3. Look for requests to googletagmanager.com"
    echo "   4. Check Console for any GTM-related messages"
    echo ""
    
    # Start the development server
    mkdocs serve
else
    echo "❌ Build failed! Please check the errors above."
    echo "💡 Common issues:"
    echo "   - Check mkdocs.yml syntax"
    echo "   - Verify all referenced files exist"
    echo "   - Ensure theme files are properly formatted"
    exit 1
fi
